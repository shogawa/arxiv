#! /usr/bin/env python
#-*- coding: utf-8 -*-
from datetime import datetime
import os
import pickle
import re
import urllib.request

#QUERY = "(cat:astro-ph.HE)+AND+(abs:AGN)"
QUERY = "(cat:astro-ph.*)+AND+(abs:AGN)+OR+(abs:blackhole)"



def parse(data, tag):
    pattern = "<" + tag + ">([\s\S]*?)<\/" + tag + ">"
    if all:
        obj = re.findall(pattern, data)
    return obj


def search(query, start, ids):
    while True:
        counter = 0

#        url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=' + str(
#            start) + '&max_results=100&sortBy=lastUpdatedDate&sortOrder=descending'

        url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=' + str(
            start) + '&max_results=20&sortBy=submittedDate&sortOrder=descending'

        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = res.read().decode()

        entries = parse(data, "entry")
        for entry in entries:

            url = parse(entry, "id")[0]
            if not (url in ids):

                title = parse(entry, "title")[0]
                abstract = parse(entry, "summary")[0]
                date = parse(entry, "published")[0]
                author = parse(entry, "name")
                abstract = abstract.replace('\n', ' ')

                with open('README.md', 'a') as file:
                   file.write(title + '  \n')
                   file.write(", ".join(author) + '  \n')
                   file.write('URL: ' + url + '  \n')
                   file.write('Published: ' + date + '  \n')
                   file.write(abstract + '  \n\n')
                ids.append(url)
            counter = counter + 1
            if counter == 20:
                return ids
        if counter == 0 and len(entries) < 100:
            with open('README.md', 'a') as file:
                file.write('Currently, there is no available papers' + '\n')
            return ids
        elif counter == 0 and len(entries) == 100:
            start = start + 100


if __name__ == "__main__":
    if os.path.exists("published.pkl"):
        ids = pickle.load(open("published.pkl", 'rb'))
    else:
        ids = []

    query = QUERY

    start = 0

    dt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    with open('README.md', 'w') as file:
        file.write(dt + '  \n\n')

    ids = search(query, start, ids)
    ids = ids[-100:]

    pickle.dump(ids, open("published.pkl", "wb"))
