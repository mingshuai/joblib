# -*- coding:utf-8 -*- 
import time
import MySQLdb

class DBTools(object):
	desc="mingshuai"
	"""docstring for DBTools"""
	def __init__(self):
		super(DBTools, self).__init__()

	def getMysqlConn(self):
		conn=MySQLdb.connect(host="localhost",user="root",passwd="mingshuai",db="mings",charset="utf8")
		print 'mysql database connect successfull'
		return conn

	def getAliYunMysqlConn(self):
		conn=MySQLdb.connect(host="121.43.164.41",user="root",passwd="mingshuai",db="company_job",charset="utf8")
		print 'connect to aliyun successfull'
		return conn
if __name__ == '__main__':
	db=DBTools()
	print db.desc
	db.getMysqlConn()
	db.getAliYunMysqlConn()
