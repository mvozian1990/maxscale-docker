import pymysql

host = "127.0.0.1"
port = 4000
user = "maxuser"
password = "maxpwd"


def print_result(res):
    for r in res:
        print(r)


db = pymysql.connect(host=host, port=port, user=user, passwd=password)

print('Last 10 rows from zipcodes_one')

cursor = db.cursor()
cursor.execute("select * from zipcodes_one.zipcodes_one limit 9990,10;")
results = cursor.fetchall()
print_result(results)

print('First 10 rows from zipcodes_two')

cursor = db.cursor()
cursor.execute("select * from zipcodes_two.zipcodes_two limit 10")
results = cursor.fetchall()
print_result(results)

print('Largest zipcode in zipcodes_one')

cursor = db.cursor()
cursor.execute("select Zipcode from zipcodes_one.zipcodes_one order by Zipcode desc limit 1;")
results = cursor.fetchall()
print_result(results)

print('Smallest zipcode in zipcodes_two')

cursor = db.cursor()
cursor.execute("select Zipcode from zipcodes_two.zipcodes_two order by Zipcode limit 1")
results = cursor.fetchall()
print_result(results)

