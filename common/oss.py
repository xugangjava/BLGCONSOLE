# coding=utf-8
import os, base64
from PIL import Image

from server_conf import BASE_DIR

BUCKET = "zrbjl"
USERNAME = 'boffqpadmin'
PASSWORD = 'RkOFlbwfasoKr7fynvBSV6rniIlwEn0T'
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
FORM_API_KEY = "WDjIt1zjV0yP1iPEBAhd67BmW1Q="

import os.path


def file_extension(path):
    return os.path.splitext(path)[1]


# avastar.billionocean.cn
def approve_avastar(uid, image_url):
    import upyun
    try:
        up = upyun.UpYun(BUCKET, USERNAME, PASSWORD, timeout=30, endpoint=upyun.ED_AUTO)
        local_path = os.path.join(BASE_DIR, 'media/' + image_url)
        with open(local_path, 'wb') as f:
            up.get(image_url, f)
        to_temp_path = os.path.join(BASE_DIR, 'media/' + str(uid) + '.png')
        circle(local_path, to_image=to_temp_path)
        with open(to_temp_path, 'rb') as f:
            res = up.put('/avastar/' + str(uid) + '.png', f, checksum=True, form=True)
        if res['message'] == 'ok':
            # up.delete(image_url)
            os.remove(local_path)
        purge_avastart(image_url)
        return True
    except:
        return False


def circle(image_url, to_image=None):
    ima = Image.open(image_url).convert("RGBA")
    size = ima.size
    # 因为是要圆形，所以需要正方形的图片
    r2 = min(size[0], size[1])
    if size[0] != size[1]:
        ima = ima.resize((r2, r2), Image.ANTIALIAS)
    imb = Image.new('RGBA', (r2, r2), (255, 255, 255, 0))
    pima = ima.load()
    pimb = imb.load()
    r = float(r2 / 2)  # 圆心横坐标
    for i in range(r2):
        for j in range(r2):
            lx = abs(i - r + 0.5)  # 到圆心距离的横坐标
            ly = abs(j - r + 0.5)  # 到圆心距离的纵坐标
            l = pow(lx, 2) + pow(ly, 2)
            if l <= pow(r, 2):
                pimb[i, j] = pima[i, j]
    imb.resize((162, 162))
    imb.save(image_url if not to_image else to_image)


def purge_avastart(url):
    import upyun
    up = upyun.UpYun(BUCKET, USERNAME, PASSWORD, timeout=30, endpoint=upyun.ED_AUTO)
    up.purge([url], domain='ffqp.billionocean.cn')


def trans_net_image_url(uid, url):
   
        import upyun
        import requests
    #    url = base64.decodestring(url)
        up = upyun.UpYun(BUCKET, USERNAME, PASSWORD, timeout=30, endpoint=upyun.ED_AUTO)
        local_path = os.path.join(BASE_DIR, 'media/src_' + str(uid) + '.png')
        to_temp_path = os.path.join(BASE_DIR, 'media/dest_' + str(uid) + '.png')
        pic = requests.get(url)
        with open(local_path, 'wb') as f:
            f.write(pic.content)
        circle(local_path, to_image=to_temp_path)
        result_image = '/cimage/' + str(uid) + '.png'
        with open(to_temp_path, 'rb') as f:
            res = up.put(result_image, f, checksum=True, form=True)
        if res['message'] == 'ok':
            os.remove(to_temp_path)
            os.remove(local_path)
        return 'http://zrbjl.billionocean.cn' + result_image
   


if __name__ == '__main__':
    fbimag = 'https://lookaside.facebook.com/platform/profilepic/?asid=607951736224556&height=50&width=50&ext=1524317800&hash=AeQcAus4Wf5cNRs6'
    # purge_avastart('/approve/14550.png')
    trans_net_image_url(1000, base64.encodestring(fbimag))
