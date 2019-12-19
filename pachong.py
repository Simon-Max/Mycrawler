import requests
from lxml import etree
import os

save_path = "D:\\hentai"
headers = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
	}

def photo_save(url):
	photo = requests.get(url,headers=headers)
	file_name = url.split('/')[-1]
	with open(os.path.join(save_path,file_name), 'wb') as f:
		f.write(photo.content)


if __name__  == '__main__':
	print("pachong begin")
	
	page_url  = "https://hentai-cosplay.com"
	low_url = "/image/makise-nippori-paypal-theres-exciting-images/"
	page = requests.get(page_url+low_url,headers=headers)
	html = etree.HTML(page.text)
	photos_url = html.xpath('//div[@id="display_image_detail"]/div[@class="icon-overlay"]/a/img/@src')
	photo_num_url = html.xpath('//span/a[contains(text(),"last>>")]/@href')
	last_url = page_url+photo_num_url[0]
	last_page = requests.get(last_url,headers=headers)
	last_html = etree.HTML(last_page.text)
	last_photo_url = last_html.xpath('//div[@id="display_image_detail"]/div[@class="icon-overlay"]/a/img/@src')[-1]






