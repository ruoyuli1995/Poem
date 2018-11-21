#coding=utf-8
import os
import json
import codecs
import re
from bs4 import BeautifulSoup

dynasties = ["XianQin", "Qin", "Han", "WeiJin", "NanBei", "Sui", "Tang",
    "Song", "Liao", "Jin", "Yuan", "Ming", "Qing", "Jindai", "Dangdai"]

dynasties_zh = [u"先秦", u"秦", u"汉", u"魏晋", u"南北朝", u"隋", u"唐",
    u"宋", u"辽", u"金", u"元", u"明", u"清", u"近现代", u"当代"]

dynasties_dic = dict([(i, j) for i, j in zip(dynasties, dynasties_zh)])
dynasties = dict([(i, idx) for idx, i in enumerate(dynasties)])

with codecs.open("dynasties.json", "w", "utf-8") as fout:
    for i in dynasties:
        fout.write(json.dumps({"id": dynasties[i], u"朝代": i, u"朝代-中文": dynasties_dic[i]}, ensure_ascii=False) + "\n")

author_id = 0
pre_title = "" # for type of 其一/其二/...
with codecs.open("author.json", "w", "utf-8") as fauthor, codecs.open("poem.json", "w", "utf-8") as fpoem:
    for dynasty in dynasties:
        dynasty_zh = dynasties_dic[dynasty]
        url = "origin/" + dynasty
        for author in os.listdir(url):
            author_url = url + "/" + author
            author = author.decode("utf-8")
            author_info = {}
            author_info["id"] = author_id
            author_info[u"作者"] = author
            author_info[u"朝代"] = dynasties[dynasty]
            for idx in xrange(len(os.listdir(author_url))):
                poem_type = ""
                idx = str(idx)
                with codecs.open(author_url + "/" + idx, "r", "utf-8") as fin:
                    content = fin.read()
                content = BeautifulSoup(content, "html.parser")
                poem = content(class_="poem")
                if not poem:
                    print("-------Error: Empty Page-------" + "\t" + dynasty + "\t" + author + "\t" + idx)
                    continue
                if len(poem) != 1:
                    print("-------Error: Poem Length not 1-------" + "\t" + dynasty + "\t" + author + "\t" + idx)
                poem = poem[0]
                for div in poem("div", recursive=False):
                    if "referImages" in str(div):
                        images = div.script.get_text()
                        images = re.findall(r"'[^']+'", images)
                        if len(images) % 2:
                            print("-------Error: Refer Images Length not Even-------" + "\t" + dynasty + "\t" + author + "\t" + idx)
                        poem_info[u"《词学图录》图片"] = [(images[i * 2], images[i * 2 + 1]) for i in xrange(len(images) / 2)]
                    elif "label1" in str(div):
                        poem_type = re.sub(u"（续上）", "", div.get_text())
                    elif "leadChar" in str(div):
                        if idx != "0":
                            print("-------Error: Author Page Index not 0-------" + "\t" + dynasty + "\t" + author + "\t" + idx)
                        if div(class_="leadChar")[0].get_text() != author:
                            print("-------Error: Author Mismatch-------" + "\t" + dynasty + "\t" + author + "\t" + idx)
                        temp_dyn = re.findall(ur"朝代[^>]+>[^<]+", str(div).decode("utf-8"))[0].split(">")[-1]
                        if temp_dyn != dynasty_zh:
                            print("-------Error: Dynasty Mismatch-------" + "\t" + dynasty + "\t" + author + "\t" + idx + "\t" + temp_dyn + "\t" + dynasty_zh)
                        if len(div(class_="squareLabel")) != len(div(class_="pageContent")):
                            print("-------Error: Square Lable and Page Content Length Mismatch-------" + "\t" + dynasty + "\t" + author + "\t" + idx)
                        for label, page_content in zip(div(class_="squareLabel"), div(class_="pageContent")):
                            label = label.get_text()
                            if label == "Null":
                                label = u"诗词集小序"
                            temp = []
                            for l, q in zip(page_content(class_="label", recursive=False), page_content(class_="quote1", recursive=False)):
                                temp.append((l.get_text(), q.get_text()))
                            if temp:
                                author_info[u"分条" + label] = temp
                            author_info[label] = page_content.get_text()
                    elif "id=\"item_" in str(div):
                        poem_info = {}
                        poem_info[u"类型"] = poem_type
                        poem_info[u"搜韵id"] = div["id"]
                        poem_info[u"作者"] = author_id
                        title = div(class_="title")
                        if title:
                            title = title[0].get_text()
                            yun = re.findall(ur"押.韵", title)
                            if yun:
                                poem_info[u"韵"] = yun[0][1]
                            typ = re.findall(ur"　.言绝句|　.言律诗|　.言排律", title)
                            if typ:
                                if not (typ[0][1 : ] == poem_type or poem_type in typ[0]):
                                    print("-------Error: Poem type Mismatch-------" + "\t" + dynasty + "\t" + author + "\t" + idx + "\t" + title + "\t" + typ[0] + "\t" + poem_type)
                            title = re.sub(ur"押.韵|显示自动注释|　|　.言绝句|　.言律诗|　.言排律", "", title)
                            title = re.sub(ur"（[^）]+·" + author + u"）", "", title)
                            if title and title[0] == u"其" and (i in u"一二三四五六七八九十〇○" for i in title[1 : ]):
                                title = re.split(ur" 其[一二三四五六七八九十〇○]", pre_title)[0] + " " + title
                            poem_info[u"题目"] = title
                            pre_title = title
                        title_note = div(class_="titleNote")
                        if title_note:
                            poem_info[u"题目小注"] = title_note[0].get_text()
                        allusion_note = div(class_="allusionNote")
                        if allusion_note:
                            temp = re.split(u"　", re.sub(u"引用典故：", "", allusion_note[0].get_text()))
                            poem_info[u"引用典故"] = [i for i in temp if i]
                        content = div(class_="content")
                        if content:
                            if len(content) != 1:
                                print("-------Error: Content Length not 1-------" + "\t" + dynasty + "\t" + author + "\t" + idx)
                            content = content[0]
                            pic_comment = content(class_="picComment")
                            if pic_comment:
                                poem_info[u"楚辞图片"] = [i.img["src"] for i in pic_comment]
                            poem_info[u"内容"] = content.get_text()
                            poem_info[u"内容（清理后）"] = re.sub(ur"[\(（][一二三四五六七八九十〇○]+章[\)）]|[\(（]\d+[\)）]|[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇]", "", poem_info[u"内容"])
                        footer = div(class_="footer")
                        if footer:
                            poem_info[u"脚注"] = footer[0].get_text()
                        comment = div("div", class_="comment")
                        if comment:
                            if len(comment) != 1:
                                print("-------Error: Comment Length not 1-------" + "\t" + dynasty + "\t" + author + "\t" + idx)
                            comment = comment[0]
                            poem_info[u"搜韵评论id"] = comment["id"]
                            temp = []
                            for l, q in zip(comment(class_="label", recursive=False), comment(class_="pageContent", recursive=False)):
                                temp.append((l.get_text(), q.get_text()))
                            if temp:
                                poem_info[u"分条评论"] = temp
                            poem_info[u"评论"] = comment.get_text()
                        shijing_images = div(class_="picSSLeft")
                        if shijing_images:
                            shijing_images = shijing_images[0]
                            poem_info[u"诗经图片"] = [(i["src"], i["title"]) for i in shijing_images("img")]
                        if len(poem_info) <= 3:
                            print("-------Error: Empty Page for Poem-------" + "\t" + dynasty + "\t" + author + "\t" + idx + "\t" + div)
                        fpoem.write(json.dumps(poem_info, ensure_ascii=False) + "\n")
                    else:
                        print("-------Warning: Extra Information for Div-------" + "\t" + dynasty + "\t" + author + "\t" + idx + "\t" + div)
            fauthor.write(json.dumps(author_info, ensure_ascii=False) + "\n")
            author_id += 1
