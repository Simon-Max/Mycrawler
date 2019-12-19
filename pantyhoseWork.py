import requests
from lxml import etree
import os
from queue import Queue
from threading import Thread
import threading

headers = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}
HantaiManiUrl = "https://hentai-cosplay.com"
savePathPre = "D:\\pachong\\Pantyhose"
saveFlag = False

class HenTaiTask(object):
	def __init__(self,url):
		self.url = url
		self.photoList = []
		self.Session = requests.Session()
		urlPartList = url.split('/')
		if len(urlPartList)>2:
			self.TaskName = urlPartList[-2]

	def getPhotoUrlPreAndNum(self):
		try:
			TaskReq = self.Session.get(self.url,headers = headers,timeout = 10)
		except Exception as e:
			print(e,"Cant get TaskMainHtml!!!")
			return None,None
		TaskMainHtml = etree.HTML(TaskReq.text)
		PhotoUrlFst = TaskMainHtml.xpath('//div[@id="display_image_detail"]/div[@class="icon-overlay"]/a/img/@src')[0]
		PhotoUrlPre = PhotoUrlFst[0:PhotoUrlFst.rfind('/')]
		lastPageUrl = HantaiManiUrl+TaskMainHtml.xpath('//span/a[contains(text(),"last>>")]/@href')[0]

		try:
			TaskReq = self.Session.get(lastPageUrl,headers = headers,timeout = 10)
		except Exception as e:
			print(e,"Cant get lastPage!!!")
			return None,None

		LastPageHtml = etree.HTML(TaskReq.text)
		LastJpgUrl = LastPageHtml.xpath('//div[@id="display_image_detail"]/div[@class="icon-overlay"]/a/img/@src')[-1]
		LastJpgIndex = int(LastJpgUrl.split('/')[-1].split('.')[0])
		return PhotoUrlPre,LastJpgIndex

	def downloadAllPicture(self):
		print("Task ",self.TaskName)
		PhotoUrlPre,LastJpgIndex = self.getPhotoUrlPreAndNum()
		if(LastJpgIndex == None):
			return
		for index in range(1,LastJpgIndex+1):
			PhotoUrl = PhotoUrlPre+'/'+str(index)+'.jpg'
			try:
				TaskReq = self.Session.get(PhotoUrl,headers = headers,timeout = 30) 
				self.photoList.append(TaskReq.content)
			except Exception as e:
				print(e,"Cant get photo!!!")
			

def DownloadTaskWorker(workerIndex,inQ,outQ):
	print("worker ",workerIndex,"begin")
	index = 1
	while(inQ.empty() is not True):
		url = inQ.get()
		Task = HenTaiTask(url)
		Task.downloadAllPicture()
		outQ.put(Task)
		print("worker",workerIndex," finish work",index)
		index += 1
		#if(outQ.qsize() > 3):
			#SavePicture(False)
	print("worker ",workerIndex,"end")

def SavePicture(joinFlag):
	global saveLock
	global saveFlag
	saveLock.acquire()
	if(saveFlag == False):
		saveFlag = True
		saveLock.release()
		saveWork = Thread(target=SavePictureWorker, args=(saveQueue,))
		saveWork.daemon = True
		saveWork.start()
		if(joinFlag == True):
			saveWork.join()
	else:
		saveLock.release()

def SavePictureWorker(outQ):
	global saveLock
	global saveFlag
	print("save worker begin")
	while(outQ.empty() is not True):
		Task = outQ.get()
		saveDir = os.path.join(savePathPre,Task.TaskName)
		os.makedirs(saveDir)
		for index in range(0,len(Task.photoList)):
			fileName = str(index) + ".jpg"
			with open(os.path.join(saveDir,fileName),"wb") as f:
				f.write(Task.photoList[index])
	saveLock.acquire()
	saveFlag = False
	saveLock.release()
	print("save worker end")




	
if __name__ == "__main__":
	TaskQueue = Queue()
	saveQueue = Queue()
	saveLock = threading.Lock()

	with open(os.path.join(savePathPre,"url.txt")) as f:
		for i in range(10):
			TaskQueue.put(HantaiManiUrl+f.readline().strip('\n'))

	TaskWork1 = Thread(target=DownloadTaskWorker, args=(1, TaskQueue, saveQueue))
	TaskWork1.daemon = True
	TaskWork1.start()
	TaskWork2 = Thread(target=DownloadTaskWorker, args=(2, TaskQueue, saveQueue))
	TaskWork2.daemon = True
	TaskWork2.start()

	TaskWork1.join()
	TaskWork2.join()
	SavePicture(True)



