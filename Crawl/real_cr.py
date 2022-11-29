from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from csv import writer
import pandas as pd
a = 1
news_items = []
for id in range(1,131):
    print(id)
    myurl = f"https://vtc.vn/the-thao-34/trang-{id}.html"
    html = urlopen(myurl).read()
    soupified = BeautifulSoup(html, "html.parser")
    container = soupified.select(".ar1.clearfix")
    for i in range(len(container)):
        post = container[i]
        link =f"https://vtc.vn{post.find('a').get('href')}"
        print(link)
        html2 = urlopen(link).read()
        soup = BeautifulSoup(html2, "html.parser")
        contain = soup.select(".content-wrapper")
        for j in range(len(contain)):
            body = contain[j].select(".content-wrapper .edittor-content > p")
            bare_body = re.sub(r'<[^>]*>', '', str(body))
            s_rmpunct = re.sub('[,;%{}$*+]', '', bare_body.strip('[').strip(']'))
            s_rmSpace = re.sub(r'[\s]+', ' ', s_rmpunct)
            if len(s_rmSpace) > 5:
                print(a)
                a = a + 1
                news_items.append([s_rmSpace, 0])

data_header = ['data','label']
with open('../Data/real_news.csv', 'w',encoding='utf-8') as f:
    writer_object = writer(f)
    writer_object.writerow(data_header)
    writer_object.writerows(news_items)