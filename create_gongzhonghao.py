import MySQLdb as mdb
from util.wx_algorithms import *
import sys
from dao.server_config import ServerConfigDao
from cron.flush_token import flush_token_name

reload(sys)
exec("sys.setdefaultencoding('utf-8')")

con = mdb.connect('127.0.0.1', 'xiaob', 'skdfjkasdf', 'xunhui')
con.set_character_set('utf8')
cur = con.cursor()
cur.execute("SET NAMES utf8")
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
con.commit()

namespace = raw_input('namespace,create which gong zhong hao?:')
cur.execute('Select * from server_config WHERE name_space=%s',[namespace])
data = cur.fetchall()
if len(data) == 0:
    print 'no this gong zhong hao, now to create it'
    cur.execute('Insert into server_config(name_space, k,v) VALUE (%s,%s,%s)', (namespace, 'access_token', ''))
    cur.execute('Insert into server_config(name_space, k,v) VALUE (%s,%s,%s)', (namespace, 'jsapi_ticket', ''))
    app_id = raw_input('app_id:')
    cur.execute('Insert into server_config(name_space, k,v) VALUE (%s,%s,%s)',(namespace,'app_id',app_id))
    app_secret = raw_input('app_secret:')
    cur.execute('Insert into server_config(name_space, k,v) VALUE (%s,%s,%s)',(namespace,'app_secret',app_secret))
    original_id = raw_input('original_id:')
    cur.execute('Insert into server_config(name_space, k,v) VALUE (%s,%s,%s)',(namespace,'original_id',original_id))
    con.commit()
    flush_token_name(namespace)

