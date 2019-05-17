import requests
from lxml import etree
import os
from bs4 import BeautifulSoup
import time

Picreferer = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Referer': 'http://i.meizitu.net'
    }



def get_items_page(page):
    base_url = 'https://www.mzitu.com/taiwan/page/'
    url = base_url + str(page)
    try:
        response = requests.get(url)
        if response.status_code == 200 :
            print(response.url)
            return response.text
    except requests.ConnectionError:
        print("item请求失败")

def parse_items(html):                                                              #item页的每个链接
    soup = BeautifulSoup(html,'lxml')
    for item_url in soup.select('#pins li > a'):
        yield item_url['href']                                                      #图册的start_url

def get_images(item_url):                                                           #保存一个图册
    try:
        response = requests.get(item_url)
        if response.status_code ==200 :
            html = response.text
            soup = BeautifulSoup(html,'lxml')
            image_url = soup.select('.main-image img')[0]['src']                    #获取图册的单个图像的URL
            title = soup.select('.currentpath')[0].get_text().split('»')[-1]        #每个图册的名字
            save_image(title=title, image_url=image_url)                            #保存图像save

            if soup.select('.pagenavi a')[-1].get_text() == '下一页»':                 #还要判断最后的按钮是下一页还是下一组，
                next_url = soup.select('.pagenavi a')[-1]['href']
                return get_images(next_url)                                             #回调=====翻页
    except requests.ConnectionError:
        print('内容页请求失败')



def save_image(title,image_url):                                                    #保存图像函数
    if not os.path.exists(title):
        os.mkdir(title)
    try:
        response = requests.get(image_url,headers = Picreferer,timeout=(7,20))                         # i.meizitu.net   加headers
        if response.status_code == 200:
            # print(response.url,':',response.status_code)                                # 检查网址是否正确
            file_path = title+'/'+image_url.split('/')[-1]
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
                    print(title+'/'+image_url.split('/')[-1]+'：已保存')
            else:
                print(title + '/' + image_url.split('/')[-1] + '：已存在')
    except requests.ConnectionError:
        print('False to save image')


def main(max_page):
    for i in range(1,max_page+1):
        html = get_items_page(i)
        time.sleep(2)
        print('正在保存第{0}页'.format(i))
        for b,item_url in enumerate(parse_items(html)):
            print('正在保存第{0}图册'.format(b+1))
            print(item_url)
            get_images(item_url)
        print('第{0}页已全部保存'.format(i))
    print('已经全部保存成功')

if __name__ == '__main__':
    main(12)




