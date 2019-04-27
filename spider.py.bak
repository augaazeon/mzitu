import requests
from bs4 import BeautifulSoup
Hostreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://www.mzitu.com'}
Picreferer = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Referer': 'http://i.meizitu.net'
    }

base_url = 'https://www.mzitu.com/179978/'
max_page = 26
for page in range(1,max_page+1):
    url = base_url + str(page)
    req = requests.get(url,headers=Hostreferer)
    print(req,req.url)
    html = req.text
    soup = BeautifulSoup(html,'lxml')
    name = soup.select('.main-title')[0].get_text()
    image_url = soup.select('.main-image img')[0]['src']

    req = requests.get(image_url, headers=Picreferer)
    with open(str(name) + '.jpg', 'wb') as f:
        f.write(req.content)
        print('保存' + name)
