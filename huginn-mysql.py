#!/usr/bin/python

import MySQLdb

db = MySQLdb.connect('localhost','root','123','huginn_production')
cursor = db.cursor()
cursor.execute("replace mydaily(id,agent_id,payload,created_at) select id,agent_id,payload,created_at from events where agent_id in (10,19,22,25,26,32,35,28,46,49,69,71,75,13,14,41,78,81,84,87,90,93,96,99,102,105,56);")
#print "database version : %s" % data
db.close()
