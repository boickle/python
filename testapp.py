#!/usr/bin/python
import MySQLdb
import ftplib

db = MySQLdb.connect(host="10.0.0.105",    # your host, usually localhost
                     user="weewx",         # your username
                     passwd="weewx123!",  # your password
                     db="weewx")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("select dateTime, outTemp from archive order by dateTime desc limit 1")

# print all the first cell of all the rows
for row in cur.fetchall():
    outTemp = row[1]

db.close()

f = open('outtemp.html','w')

message = """<html>
<head></head>
<body><p>%s</p></body>
</html>""" %outTemp

print message

f.write(message)
f.close()

session = ftplib.FTP('10.0.0.105','weewx','Br00k1es')
file = open('outtemp.html','rb')                  # file to send
session.storbinary('STOR outtemp.html', file)     # send the file
file.close()                                    # close file and FTP
session.quit()
