import requests
from bs4 import BeautifulSoup
from lxml import etree

Hostreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://www.mzitu.com'
}
Picreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://i.meizitu.net'
    }
def get_page(url):
    response = requests.get(url,headers=Hostreferer)
    try:
        if response.status_code == 200 :
            html = response.text
            html = etree.HTML(html)   #用xpath解析数据
            print(response.url,response)
            return html
    except requests.ConnectionError:
        print('请求失败')

#获取最大页码
def get_max_page(html):
    max_page = html.xpath("//div[@class='pagenavi']//a[last()-1]//text()")
    return max_page

def parse_page(html):
    image_url = html.xpath("//div[@class='main-image']//img/@src")
    title = html.xpath('//h2/text()')[0]
    return image_url,title


def save_image(image_url,title):
    req = requests.get(image_url[0],headers=Picreferer)
    with open(title+'.jpg','wb') as f:
        f.write(req.content)
        print('保存'+title)

def main(url):
    html = get_page(url)
    max_page = get_max_page(html)
    for i in range(1,int(max_page[0])+1):
        url = base_url +'/'+ str(i)
        html = get_page(url)
        image_url,title = parse_page(html)
        save_image(image_url,title)

url = base_url = 'https://www.mzitu.com/179574' #start_url
if __name__ == '__main__':
    main(url)
