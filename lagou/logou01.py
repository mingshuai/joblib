# -*- coding:utf-8 -*- 
import requests
from bs4 import BeautifulSoup

#获取拉勾网的公司和职位信息
class Lagou(object):
	base_json_url="http://www.lagou.com/gongsi/searchPosition.json?companyId=%d&pageNo=%d&pageSize=%d"
	base_company_url="http://www.lagou.com/gongsi/%d.html"
	base_job_url="http://www.lagou.com/jobs/%d.html?source=pl&i=pl-0"
	base_comment_url="http://www.lagou.com/gongsi/searchInterviewExperiences.json?companyId=%d&pageNo=%d&pageSize=%d"
	
	headers={
		'Host':'www.lagou.com',
		'Origin':'http://www.lagou.com',
		'Referer':'http://www.lagou.com/gongsi/j7254.html',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)',
		'X-Requested-With':'XMLHttpRequest'
	}
	def __init__(self, comid,pageSize):
		super(Lagou, self).__init__()
		self.comid = comid
		self.pageSize=pageSize
		#print Lagou.base_json_url % (comid,1,pageSize)


	#获取公司的相信信息
	#获取公司创始人的相关信息
	# self.companyDetail
	# self.managerLIst=list()
	def getCompanyDetails(self):
		
		url=self.base_company_url % (self.comid)
		print url
		
		response=requests.get(url,headers=Lagou.headers)
		if response.status_code != 200:
			return
		print response.status_code
		print '******'

		html=response.text
		soup=BeautifulSoup(html,"lxml")
		
		product_desc=soup.find(class_="product_profile")
		product_img=soup.find("img",alt="产品图片")
		product_name=soup.find(class_="url_valid")
		company_desc=soup.find(class_="company_intro_text")
		manager_list=soup.find(class_="manager_list")
		company_info=soup.find(class_="company_info")
		company_name=company_info.find(class_="company_main").find("h1").find("a")["title"].encode("utf-8")
		company_auth=company_info.find(class_="identification").encode("utf-8")
		company_word=company_info.find(class_="company_word").encode("utf-8")
		company_others=company_info.find_all("strong")
		company_active_job=company_others[0].text.encode("utf-8").strip()
		company_job_7day_deal=company_others[1].text.encode("utf-8").strip()
		company_job_deal_day=company_others[2].text.encode("utf-8").strip()
		company_job_comments=company_others[3].text.encode("utf-8").strip()
		company_last_login=company_others[4].text.encode("utf-8").strip()
		# print company_active_job,company_job_7day_deal,company_job_deal_day,company_job_comments,company_last_login
		# for tmp in company_others:
		# 	print tmp.text.encode("utf-8").strip()
		#print manager_list
		self.companyDetail=dict()
		self.companyDetail["companyId"]=self.comid
		self.companyDetail["companyUrl"]=url
		self.companyDetail["productDesc"]=product_desc.text.encode("utf-8")
		self.companyDetail["productDescHtml"]=product_desc
		self.companyDetail["productUrl"]=product_name["href"]
		self.companyDetail["productImgUrl"]=product_img.src
		self.companyDetail["productName"]=product_name.text.encode("utf-8").strip()
		self.companyDetail["companyDescHtml"]=company_desc
		self.companyDetail["companyDesc"]=company_desc.text.encode("utf-8")
		self.companyDetail["companyActiveJob"]=company_active_job
		self.companyDetail["companyJob7dayDeal"]=company_job_7day_deal
		self.companyDetail["companyJobDealDay"]=company_job_deal_day
		self.companyDetail["companyJobComments"]=company_job_comments
		self.companyDetail["companyLastLogin"]=company_last_login
		#公司管理层人员信息
		self.managerLIst=list()
		for t_leader in manager_list.find_all("li"):
			# print t_leader
			leader=dict()
			manager_photo_url=t_leader.find(class_="item_manger_photo_show")["src"]
			manager_name=t_leader.find(class_="item_manager_name").text.encode("utf-8").strip()
			manager_content_url=t_leader.find(class_="item_manager_name").find("a")["href"]
			manager_title=t_leader.find(class_="item_manager_title").text.encode("utf-8").strip()
			manager_desc=t_leader.find(class_="item_manager_content").text.encode("utf-8").strip()
			manager_desc_html=t_leader.find(class_="item_manager_content")
			leader["manager_photo_url"]=manager_photo_url
			leader["manager_name"]=manager_name
			leader["manager_content_url"]=manager_content_url
			leader["manager_title"]=manager_title
			leader["manager_desc"]=manager_desc
			leader["manager_desc_html"]=manager_desc_html
			# print leader
			self.managerLIst.append(leader)
			# print "1------------"
		
	#根据暴露出来的json串
	#获取基本的公司信息
	#获取公司招聘列表
	#生成公司，工作基本信息
	# self.company=dict()
	# self.jobs=list()
	def getJobsInfo(self):
		readCompanyFlag=0
		#生成公司，工作基本信息
		self.company=dict()
		self.jobs=list()
		for i in range(1,100):
			url=Lagou.base_json_url % (self.comid,i,self.pageSize)
			print url
			#Lagou
			jobs_json=requests.get(url,headers=Lagou.headers).json()

			joblist=jobs_json["content"]["data"]["page"]["result"]
			if len(joblist)>0:
				for t_job in joblist:
					#解析公司数据
					if readCompanyFlag==0:
						self.company["companyId"]=t_job["companyId"]
						self.company["financeStage"]=t_job["financeStage"]
						self.company["companyName"]=t_job["companyName"]
						self.company["companySize"]=t_job["companySize"]
						self.company["industryField"]=t_job["industryField"]
						self.company["leaderName"]=t_job["leaderName"]
						self.company["companyLabels"]=t_job["companyLabels"]
						self.company["companyLabelList"]=t_job["companyLabelList"]
						self.company["companyLogo"]=t_job["companyLogo"]
					readCompanyFlag=1
					#解析职位信息
					job=dict()

					job["jobId"]=t_job["positionId"]
					job["companyId"]=t_job["companyId"]
					job["companyName"]=t_job["companyName"].encode("utf-8")
					job["jobNature"]=t_job["jobNature"].encode("utf-8")
					job["jobName"]=t_job["positionName"].encode("utf-8")
					job["city"]=t_job["city"].encode("utf-8")
					job["education"]=t_job["education"].encode("utf-8")
					job["haveDeliver"]=t_job["haveDeliver"]
					job["keyWords"]=t_job["keyWords"].encode("utf-8")
					job["orderBy"]=t_job["orderBy"]
					job["positionAdvantage"]=t_job["positionAdvantage"].encode("utf-8")
					job["positionFirstType"]=t_job["positionFirstType"].encode("utf-8")
					job["rewardMoney"]=t_job["rewardMoney"]
					job["salary"]=t_job["salary"]
					job["score"]=t_job["score"]
					job["searchScore"]=t_job["searchScore"]
					job["workYear"]=t_job["workYear"].encode("utf-8")
					job["bornTime"]=t_job["bornTime"]
					job["adStartTime"]=t_job["adStartTime"]
					job["adEndTime"]=t_job["adEndTime"]
					job["pubTime"]=t_job["createTime"]

					#添加job的详细信息
					jobDetail=self.getJobDetailsByJobId(t_job["positionId"])
					jobInfo=dict(job, **jobDetail)
					self.jobs.append(jobInfo)
				# print type(joblist)
				# print joblist[0]["orderBy"]
				# print joblist[0]["positionName"].encode("utf-8")
				# print joblist[0]["positionName"].encode("utf-8")
			else:
				print "no jobs.."
				break
		pass
		
		#print self.jobs
		#print self.company

	# 获取公司的评论列表
	def getCompanyComment(self):
		self.commentList=list()
		for i in range(1,100):
			url=self.base_comment_url % (self.comid,i,self.pageSize)
			print "now deal with ",url
			comment_json=requests.get(url,headers=self.headers).json()["content"]["data"]["page"]["result"]
			if len(comment_json)<=0:
				break
			j=0
			for t_comment in comment_json:
				comment=dict()
				comment["companyId"]=t_comment["companyId"]
				comment["companyName"]=t_comment["companyName"].encode("utf-8")
				comment["companyScore"]=t_comment["companyScore"]
				comment["comprehensiveScore"]=t_comment["comprehensiveScore"]
				comment["content"]=t_comment["content"].encode("utf-8")
				comment["createTime"]=t_comment["createTime"]
				comment["describeScore"]=t_comment["describeScore"]
				comment["evaluation"]=t_comment["evaluation"]
				comment["hrId"]=t_comment["hrId"]
				comment["id"]=t_comment["id"]
				comment["interviewerScore"]=t_comment["interviewerScore"]
				comment["isAllowReply"]=t_comment["isAllowReply"]
				comment["isAnonymous"]=t_comment["isAnonymous"]
				comment["isInterview"]=t_comment["isInterview"]
				comment["noInterviewReason"]=t_comment["noInterviewReason"]
				comment["noInterviewType"]=t_comment["noInterviewType"]
				comment["orderId"]=t_comment["orderId"]
				comment["portrait"]=t_comment["portrait"]
				comment["positionId"]=t_comment["positionId"]
				comment["positionName"]=t_comment["positionName"].encode("utf-8")
				comment["positionType"]=t_comment["positionType"].encode("utf-8")
				comment["replyCount"]=t_comment["replyCount"]
				comment["source"]=t_comment["source"]
				comment["status"]=t_comment["status"]
				comment["tags"]=t_comment["tags"].encode("utf-8")
				comment["type"]=t_comment["type"]
				comment["usefulCount"]=t_comment["usefulCount"]
				comment["userId"]=t_comment["userId"]
				comment["username"]=t_comment["username"].encode("utf-8")
				self.commentList.append(comment)
				# print comment["content"].encode("utf-8")
				# j=j+1
				# print j

			#print comment_json
		pass

	# 根据jobid(position_id)获取该工作打详细信息。
	# 1768496
	def getJobDetailsByJobId(self,jobid):
		url=base_job_url="http://www.lagou.com/jobs/%d.html?source=pl&i=pl-0" % (jobid)
		print url
		html=requests.get(url,headers=self.headers).text
		soup=BeautifulSoup(html,"lxml")
		jobDesc=soup.find(class_="job_bt").text.encode("utf-8").strip()
		jobDescHtml=soup.find(class_="job_bt").encode("utf-8").strip()
		hrInfo=soup.find(class_="jd_publisher")
		hrImg=hrInfo.find("img")["src"]
		hrName=hrInfo.find(class_="name").text.encode("utf-8").strip()
		hrPos=hrInfo.find(class_="pos").text.encode("utf-8").strip()
		job7dayDeal=hrInfo.find_all(class_="data")[0].text.encode("utf-8").strip()
		JobDealDay=hrInfo.find_all(class_="data")[1].text.encode("utf-8").strip()
		#print jobDesc
		jobDetail=dict()
		jobDetail["jobId"]=jobid
		jobDetail["jobDesc"]=jobDesc
		jobDetail["jobDescHtml"]=jobDescHtml
		jobDetail["hrImg"]=hrImg
		jobDetail["hrName"]=hrName
		jobDetail["hrPos"]=hrPos
		jobDetail["job7dayDeal"]=job7dayDeal
		jobDetail["JobDealDay"]=JobDealDay

		return jobDetail
		# jobDetail[""]=
		#print soup 

		pass
		


if __name__ == '__main__':
	lagou1=Lagou(23177,30)
	lagou1.getJobsInfo()



	# job=lagou1.getJobDetailsByJobId(1768496)
	# for k,v in job.iteritems():
	# 	print k,v
	# lagou1.getJobDetails(1768496)
	# j=0
	# for tmp in lagou1.commentList:
	# 	print '**************************'
	# 	j=j+1
	# 	print j
	# 	for k,v in tmp.iteritems():
	# 		try:

	# 			print k,v
	# 		except:
	# 			pass
	i=0
	for tmp in lagou1.jobs:
		print i
		i=i+1
		print "************************************************"
		for k,v in tmp.iteritems():
			print k,v
	# for key in lagou1.companyDetail.keys():
	# 	print key
	# print "^^^^^^^^^^^^^^^^"
	# for k,v in lagou1.companyDetail.iteritems():
	# 	print k,v
	# print '******************************************'
	# i=0
	# for job in lagou1.jobs:
	# 	print i
	# 	i=i+1
	# 	print job["jobNature"].encode("utf-8")
	# 	print job["jobName"].encode("utf-8")
	# 	print job["keyWords"].encode("utf-8")
	# 	print job["salary"]
	# print lagou1.company
	# print lagou1.company["companyName"].encode("utf-8")
	# print lagou1.company["companyLabelList"]
	# print dbools.desc
	# lagou1.fetchToMysql()