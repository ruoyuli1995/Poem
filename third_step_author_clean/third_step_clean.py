#coding=utf-8
import os
import json
import codecs
import re

"""
First, authors with same names
"""

"""
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
"""

"""
Second, check
"""

ids = set()
with codecs.open("author.json", "r", "utf-8") as fauthor:
    for idx, line in enumerate(fauthor):
        line = json.loads(line)
        temp = []
        if isinstance(line["id"], list):
            temp += line["id"]
        else:
            temp.append(line["id"])
        for i in temp:
            if i in ids:
                print("Error", i)
            ids.add(i)

print(len(ids))
print(set(range(max(list(ids)) + 1)) - ids)
assert(len(ids) == max(list(ids)) + 1)

"""
Third, authors with same descriptions
"""

"""
authors = {}
with codecs.open("author.json", "r", "utf-8") as fauthor:
    for line in fauthor:
        line = json.loads(line)
        if u"人物简介" not in line or not line[u"人物简介"]:
            continue
        if line[u"人物简介"] not in authors:
            authors[line[u"人物简介"]] = []
        authors[line[u"人物简介"]].append(line)

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
"""