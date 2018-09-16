# coding=utf-8
#
#
# if __name__=='__main__':
#     from common.core import *
#     with DB() as db:
#         rs=db.sql_dict_array("SELECT usrid from usr where regtime<'2018-05-10' and regtime>'2018-04-01';")
#         for r in rs:
#             receiverid = r['usrid']
#             print r
#             db.sql_exec("""
#                           INSERT INTO
#                              poker.mail(
#                                sendername
#                               ,senderid
#                               ,receiverid
#                               ,title
#                               ,content
#                               ,sendtim
#                               ,attachmenttype
#                               ,attachmentnum
#                               ,isread
#                               ,mailtype
#                               ,isgetattachment)
#                           VALUES
#                              (
#                                   'System Mail'
#                                   ,1000
#                                   ,%d
#                                   ,'%s'
#                                   ,'%s'
#                                   ,now()
#                                   ,%d
#                                   ,%d
#                                   ,0
#                                   ,0
#                                   ,0
#                               );
#                     """,receiverid, "游戏补偿", "因服务器故障，导致游戏部分玩家无法登陆，现将筹码补偿发放与您，请查收。", 1, 100000)
#         db.commit()
