from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from csv import writer

news_items = []
links = []
for id in range(1,6):
    myurl = f"https://tingia.gov.vn/ket-qua-tiep-nhan-va-xu-ly/page/{id}/"
    html = urlopen(myurl).read()
    soupified = BeautifulSoup(html, "html.parser")
    container = soupified.select(".posts-items.posts-list-container .post-item")
    for i in range(len(container)):
        post = container[i]
        link = post.find('a').get('href')
        links.append(link)

linksRmD = [*set(links)]
print(len(linksRmD))

for l in linksRmD:
    html2 = urlopen(l).read()
    soup = BeautifulSoup(html2, "html.parser")
    contain = soup.select(".main-content")
    for j in range(len(contain)):
        body = contain[j].select(".container-wrapper.post-content .entry-content.entry.clearfix > p")
        bare_body = re.sub(r'<[^>]*>', '', str(body))
        s_rmpunct = re.sub('[,;%{}$*+]', '', bare_body.strip('[').strip(']'))
        s_rmSpace = re.sub(r'[\s]+', ' ', s_rmpunct)
        if len(s_rmSpace) > 5:
            news_items.append([s_rmSpace, 1])

data_header = ['data','label']
with open('../Data/fake_news.csv', 'w',encoding='utf-8') as f:
    writer_object = writer(f)
    writer_object.writerow(data_header)
    writer_object.writerows(news_items)


