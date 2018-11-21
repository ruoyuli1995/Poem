#coding=utf-8
import os
import json
import codecs
import re

authors = {}
with codecs.open("author.json", "r", "utf-8") as fauthor:
    for line in fauthor:
        line = json.loads(line)
        if line[u"作者"] not in authors:
            authors[line[u"作者"]] = []
        authors[line[u"作者"]].append(line)

with codecs.open("temp", "w", "utf-8") as fout:
    for i in authors:
        if len(authors[i]) > 1:
            fout.write(i + "\n\n")
            for j in authors[i]:
                for k in j:
                    if u"分条" in k:
                        continue
                    fout.write(k + "\n")
                    try:
                        fout.write(j[k].replace("\n", " ") + "\n")
                    except:
                        fout.write(str(j[k]) + "\n")
                fout.write("\n")
            fout.write("----------------------------------" + "\n")
