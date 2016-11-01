#!/usr/bin/python
import MySQLdb
import ftplib
import smtplib
import config as cfg

from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText

db = MySQLdb.connect(host=cfg.mysql['host'],    # your host, usually localhost
                     user=cfg.mysql['user'],         # your username
                     passwd=cfg.mysql['passwd'],  # your password
                     db=cfg.mysql['db'])        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("select DATE_FORMAT(CONVERT_TZ(from_unixtime(a.dateTime), '+00:00', 'US/Eastern'),'%h:%i %p') as dateTime, outTemp from archive as a where CONVERT_TZ(from_unixtime(a.dateTime),'+00:00', 'US/Eastern') > NOW() - INTERVAL 1 DAY order by outTemp limit 1;")

# print all the first cell of all the rows
for row in cur.fetchall():
    outTempMin = row[1]
    dateTimeMin = row[0]

cur.execute("select DATE_FORMAT(CONVERT_TZ(from_unixtime(a.dateTime), '+00:00', 'US/Eastern'),'%h:%i %p') as dateTime, outTemp from archive as a where CONVERT_TZ(from_unixtime(a.dateTime),'+00:00', 'US/Eastern') > NOW() - INTERVAL 1 DAY order by outTemp desc limit 1;")

# print all the first cell of all the rows
for row in cur.fetchall():
    outTempMax = row[1]
    dateTimeMax = row[0]

db.close()


fromaddr = cfg.email['fromaddr']
toaddr = cfg.email['toaddr']
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = cfg.email['subject']

body = "Low Temperature: " + str(outTempMin) + " at " + str(dateTimeMin) + "\r\n"
body += "High Temperature: " + str(outTempMax) + " at " + str(dateTimeMax) + "\r\n"

msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP(cfg.email['server'], 587)
server.starttls()
server.login(fromaddr, cfg.email['passwd'])
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
