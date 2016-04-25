import getpass
import pymysql

conn_host = ''
conn_port = 0
conn_user = ''
conn_pass = ''
conn_sock = ''
conn_db   = ''
conn_chrs = 'utf8'


db_connection = input('Would you like to use Adam\'s, David\'s, or Ned\'s database connection \n' +
                      'or enter your own custom connection? \n' + 
                      'Type a for Adam, d for David, n for Ned, or c for custom: ').strip().lower()

if db_connection=='d':
    conn_host = 'localhost'
    conn_port = 3306
    conn_user = 'root'
    conn_pass = 'lenneth6'
elif db_connection=='a':
    conn_host = '127.0.0.1'
    conn_user = 'dbproject'
    conn_pass = 'cs327e'
    conn_sock = '/tmp/mysql.sock'
    conn_db   = 'mysql'
    conn_chrs = 'utf8'
elif db_connection=='n':
    conn_host = '127.0.0.1'
    conn_user = 'dbproject'
    conn_pass = 'cs327e'
    conn_sock = '/tmp/mysql.sock'
    conn_db   = 'mysql'
    conn_chrs = 'utf8'
# default to custom
else:
    mp = input('Do you have a Mac or PC? (m/p): ').strip().lower()
    if mp=='m':
        conn_host = '127.0.0.1'
        conn_user = input('Please enter your username: ').strip()
        conn_pass = getpass.getpass(prompt='Please enter your password: ')
        conn_sock = input('Please enter your unix socket string: ').strip()
        conn_db   = 'mysql'
        conn_chrs = 'utf8'
    # default to pc
    else:
        conn_host = input('Please enter your host: ').strip()
        conn_port = int (input ('Please enter your port: ').strip() )
        conn_user = input('Please enter your username: ').strip()
        conn_pass = getpass.getpass(prompt='Please enter your password: ')

conn = 0
if db_connection in ('a','n') or mp=='m':
    conn = pymysql.connect(host=conn_host, unix_socket=conn_sock, user=conn_user, passwd=conn_pass, db=conn_db, charset=conn_chrs)
else:
    conn = pymysql.connect(host=conn_host, port=conn_port, user=conn_user, passwd=conn_pass)


print (conn_host)
print(conn_port)
print(conn_user)
print(conn_pass) 
print(conn_sock)
print(conn_db)  
print(conn_chrs)
