#coding=utf-8
import urllib2
import os
import re
import codecs
import time

count = 0
for dynasty in ["XianQin", "Qin", "Han", "WeiJin", "NanBei", "Sui", "Tang",
    "Song", "Liao", "Jin", "Yuan", "Ming", "Qing", "Jindai", "Dangdai"]:
    if not os.path.exists(dynasty):
        os.mkdir(dynasty)
    url = "https://sou-yun.com/PoemIndex.aspx?dynasty=" + dynasty + "&lang=s"
    content = urllib2.urlopen(url).read()
    for author in re.findall(r"<a href='[^']*'>", content):
        if "author" in author:
            author_url = "https://sou-yun.com" + author.split("'")[1] + "&lang=s"
            author = urllib2.unquote(author.split("=")[-1][ : -2])

            if not os.path.exists(dynasty + "/" + author):
                os.mkdir(dynasty + "/" + author)
            else:
                continue
                
            author_content = urllib2.urlopen(author_url).read().decode("utf-8")
            count += 1
            if count % 1000 == 0:
                time.sleep(200)
            temp_author_content = re.sub(r"\s", "", author_content)
            
            with codecs.open(dynasty + "/" + author + "/0", "w", "utf-8") as fout:
                fout.write(author_content + "\n")
            flag = False
            if u"页显示" in temp_author_content:
                number = int(re.findall(ur"\d+页显示", temp_author_content)[0][:-3])
                flag = True
            if u"頁顯示" in temp_author_content:
                number = int(re.findall(ur"\d+頁顯示", temp_author_content)[0][:-3])
                flag = True
            if flag:
                for i in xrange(1, number):
                    with codecs.open(dynasty + "/" + author + "/" + str(i), "w", "utf-8") as fout:
                        author_url_page = author_url + "&type=All&page=" + str(i)
                        author_content_page = urllib2.urlopen(author_url_page).read().decode("utf-8")
                        count += 1
                        if count % 1000 == 0:
                            time.sleep(200)
                        fout.write(author_content_page + "\n")
