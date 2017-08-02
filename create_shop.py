#this file is used for admin charge user money
import MySQLdb as mdb
from util.wx_algorithms import *
import sys
from dao.server_config import ServerConfigDao

reload(sys)
exec("sys.setdefaultencoding('utf-8')")

con = mdb.connect('127.0.0.1', 'xiaob', 'skdfjkasdf', 'xunhui')
con.set_character_set('utf8')
cur = con.cursor()
cur.execute("SET NAMES utf8")
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
con.commit()

namespace = raw_input('namespace,use which gong zhong hao?:')
cur.execute('Select * from server_config WHERE name_space=%s',(namespace))
data = cur.fetchall()
if len(data) == 0:
    print 'no this gong zhong hao, now to create it'
    app_id = raw_input('app_id:')
    cur.execute('Insert into server_config(name_space, k,v) VALUE (%s,%s,%s)',(namespace,'app_id',app_id))
    app_secret = raw_input('app_secret:')
    cur.execute('Insert into server_config(name_space, k,v) VALUE (%s,%s,%s)',(namespace,'app_secret',app_secret))
    original_id = raw_input('original_id:')
    cur.execute('Insert into server_config(name_space, k,v) VALUE (%s,%s,%s)',(namespace,'original_id',original_id))

print 'start create shop setting...'
shop_id = int(raw_input('shop_id: '))
shop_name = raw_input('shop_name(chinese): ')


cur.execute('Insert into shop_setting(shop_id, name,namespace,filter_orderid_flag) VALUES (%s,%s,%s,1)',(shop_id,shop_name,namespace))
con.commit()
print 'finished!'
print 'start create shop admin user...'
user_name = raw_input('user name: ')
cur.execute('Insert into shop_user(shop_id, user_name,password) VALUES (%s,%s,%s)',
            (shop_id,user_name,'e10adc3949ba59abbe56e057f20f883e'))
con.commit()
print 'finished! default password is 123456'

print 'start create balance...'
cur.execute('Insert into shop_account(shop_id, balance) VALUES (%s,0)',(shop_id,))
con.commit()
print 'finished! balance is 0'


print 'start create lucky money amount...'
money = int(raw_input('lucky money amount(yuan): '))
money = money * 100
cur.execute('Insert into log_change_money(shop_id,money ) VALUES (%s,%s)',(shop_id,money))
con.commit()
print 'finished!'

# print 'start create tag...'
# tagid = createTag('shop_%d'%shop_id)
# print 'finished! tag id : %d'%tagid
#
# print 'save tag id'
# cur.execute('Update shop_setting set wx_tag_id=%s where shop_id=%s',(tagid,shop_id))
# con.commit()
# con.close()
#
# access_token = ServerConfigDao()['access_token']
# print access_token