from gevent import monkey
monkey.patch_all()
import sys
sys.path = ['C:/BLGCONSOLE/'] + sys.path
import bottle
import sitecustomize
from core.api import *
from core.console import *
from core.apis import *
from beaker.middleware import SessionMiddleware
from core.apis import *
from core.coin_console import *

session_opts = {
    'session.type': 'ext:database',
    'session.url': 'mysql+mysqldb://root:%s@localhost/poker?charset=utf8' % DB_PWD,
    'session.cookie_expires': 60000,
    'session.auto': True,
}

os.chdir(os.path.dirname(__file__))
application = SessionMiddleware(bottle.default_app(), session_opts)
