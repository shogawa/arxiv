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
    # parse atom file
    # e.g. Input :<tag>XYZ </tag> -> Output: XYZ

    pattern = "<" + tag + ">([\s\S]*?)<\/" + tag + ">"
    if all:
        obj = re.findall(pattern, data)
    return obj


def search(query, start, ids):
    ids1 = []
    while True:
        counter = 0

#        url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=' + str(
#            start) + '&max_results=100&sortBy=lastUpdatedDate&sortOrder=descending'

        url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=' + str(
            start) + '&max_results=10&sortBy=submittedDate&sortOrder=descending'

        # Get returned value from arXiv API
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = res.read().decode()
        # Parse the returned value
        entries = parse(data, "entry")
        for entry in entries:
            # Parse each entry
            url = parse(entry, "id")[0]
            if not (url in ids):
                # parse
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
                ids1.append(url)
                counter = counter + 1
                if counter == 10:
                    return ids1
        if counter == 0 and len(entries) < 100:
            with open('README.md', 'a') as file:
                file.write('Currently, there is no available papers' + '\n')
            return ids1
        elif counter == 0 and len(entries) == 100:
            # When there is no available paper and full query
            start = start + 100


if __name__ == "__main__":
    # Load log of published data
    if os.path.exists("published.pkl"):
        ids = pickle.load(open("published.pkl", 'rb'))
    else:
        ids = []

    # Query for arXiv API
    query = QUERY

    start = 0

    dt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    with open('README.md', 'w') as file:
        file.write(dt + '  \n\n')

    # Call function
    ids = search(query, start, ids)

    # Update log of published data
    pickle.dump(ids, open("published.pkl", "wb"))
