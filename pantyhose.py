import requests
from lxml import etree
import os

headers = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}

def GetLastPageIndex(stHtml):
	LastpageUrl = stHtml.xpath('//a[@class="last"]/@href')
	try:
		sIndex = LastpageUrl[0].split('/')[-2]
		return int(sIndex)
	except BaseException as e:
		print(e)
		return None

def create_file(filename):
    path = filename[0:filename.rfind("\\")]
    if not os.path.isdir(path):  # 无文件夹时创建
        os.makedirs(path)
        if not os.path.isfile(filename):  # 无文件时创建
            fd = open(filename, mode="w", encoding="utf-8")
            fd.close()


if __name__ == "__main__":
	save_path_Pre = "D:\\pachong"
	Tag = "Pantyhose"
	savePath = os.path.join(save_path_Pre,Tag,"url.txt")
	HantaiManiUrl = "https://hentai-cosplay.com/"
	HantaiTagUrl = "https://hentai-cosplay.com/search/tag/"
	TagUrl = HantaiTagUrl+Tag
	TagContentUrlList = []

	TagReq = requests.get(TagUrl,headers=headers)
	TagHtml = etree.HTML(TagReq.text)
	PageNum = GetLastPageIndex(TagHtml)
	if(PageNum == None):
		print("Not get PageNum\n")
		quit()

	print("PageNum:",PageNum)
	TagSession = requests.Session()
	#TagSession.headers.update(headers)
	for index in list(range(1,PageNum+1)):
		print("iter",index)
		TagPageUrl = HantaiTagUrl+Tag+'/'+str(index)
		try:
			TagReq = TagSession.get(TagPageUrl,headers = headers,timeout=5)
		except BaseException as e:
			print(e)
			continue
		TagHtml = etree.HTML(TagReq.text)
		TagContentUrlList.extend(TagHtml.xpath('//div[@class="image-list-item-image"]/a/@href'))

	print("find item :",len(TagContentUrlList))
	create_file(savePath)
	with open(savePath,"w") as f:
		for url in TagContentUrlList:
			f.write(url)
			f.write('\n')




