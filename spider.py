import requests
from bs4 import BeautifulSoup
from lxml import etree

Hostreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://www.mzitu.com'
}
def get_page(url = 'https://www.mzitu.com/120485/',headers=Hostreferer):
    response = requests.get(url)
    try:
        if response.status_code == 200 :
            html = response.text
            html = etree.HTML(html)
            print(response.url,response)
            return html
    except requests.ConnectionError:
        print('请求失败')


def get_max_page(html):
    max_page = html.xpath("//div[@class='pagenavi']//a[last()-1]//text()")
    return max_page

def parse_page(html):
    image_url = html.xpath("//div[@class='main-image']//img/@src")
    title = html.xpath('//h2/text()')[0]
    return image_url,title


def save_image(image_url,title):
    Picreferer = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Referer': 'http://i.meizitu.net'
    }
    req = requests.get(image_url[0],headers=Picreferer)
    with open(title+'.jpg','wb') as f:
        f.write(req.content)
        print('保存'+title)

def main():
    html = get_page()
    base_url = 'https://www.mzitu.com/120485/'
    max_page = get_max_page(html)
    for i in range(1,int(max_page[0])+1):
        url = base_url +'/'+ str(i)
        html = get_page(url)
        image_url,title = parse_page(html)
        save_image(image_url,title)


if __name__ == '__main__':
    main()