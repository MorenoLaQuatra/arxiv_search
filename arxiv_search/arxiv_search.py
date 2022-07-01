"""
A python program to retreive recrods from ArXiv.org in given
categories and specific date range.

Author: Mahdi Sadjadi (sadjadi.seyedmahdi[AT]gmail[DOT]com).
"""
from __future__ import print_function
import xml.etree.ElementTree as ET
import datetime
import time
import sys
from typing import Dict, List
import xmltodict
import datetime
from tqdm import tqdm

PYTHON3 = sys.version_info[0] == 3
if PYTHON3:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import HTTPError
else:
    from urllib import urlencode
    from urllib2 import HTTPError, urlopen

from arxiv_search.constants import OAI, ARXIV, BASE

import logging
from arxiv_search.paper import Paper

class Scraper(object):

    def __init__(
        self,
        search_term: str = None,
        author_string: str = None,
        lookup_title: bool = True,
        lookup_abstract: bool = True,
        category: str = None,
        date_from: str = None,
        date_until: str = None,
        use_publish_date: bool = True, #if false use update date
        sortBy: str = "relevance",
        sortOrder: str = "descending",
        t: int = 30,
        timeout: int = 300,
        fetching_number_per_iter : int = 1000,
        max_res : int = None,
    ):

        self.t = t
        self.timeout = timeout
        self.use_publish_date = use_publish_date
        self.max_res = max_res

        self.url = BASE + f"?sortBy={sortBy}&sortOrder={sortOrder}&search_query="

        if category is None:
            logging.warning("category is not explictly set.")
            self.cat = None
        else:
            self.url += f"cat:{category}"
            self.cat = category

        if search_term is not None:
            if lookup_title:
                self.url += f"+AND+ti:{search_term}"

            if lookup_abstract:
                self.url += f"+AND+abs:{search_term}"
        
        if author_string is not None:
            self.url += f"+AND+au:{author_string}"

        if date_from is not None:
            self.date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        else:
            self.date_from = datetime.datetime.strptime("1970-01-01", '%Y-%m-%d')
            

        if date_until is not None:
            self.date_until = datetime.datetime.strptime(date_until, '%Y-%m-%d')
        else:
            self.date_until = datetime.date.today() + datetime.timedelta(days=1)
            self.date_until = datetime.datetime(self.date_until.year, self.date_until.month, self.date_until.day)

        self.fetching_number_per_iter = fetching_number_per_iter

    def get_results(self) -> List[Dict]:
        
        start_res = 0
        pending_results = True
        iter_number = 1
        list_papers = []
        pbar = tqdm()
        while pending_results:
            
            logging.info(f"fetching {start_res} -> {start_res+self.fetching_number_per_iter}")
            current_url = f"{self.url}&start={start_res}&max_results={self.fetching_number_per_iter}"

            try:
                response = urlopen(current_url)
            except HTTPError as e:
                if e.code == 503:
                    to = int(e.hdrs.get("retry-after", 30))
                    logging.warning("Got 503. Retrying after {0:d} seconds.".format(self.t))
                    time.sleep(self.t)
                    continue
                else:
                    raise

            # parsing XML
            try:
                xml = response.read()
                d_res = xmltodict.parse(xml)
                list_pubs = d_res["feed"]["entry"]
                for dict_info in list_pubs:
                    paper = Paper(dict_info)
                    if self.use_publish_date:
                        if paper.published >= self.date_from and paper.published <= self.date_until:
                            list_papers.append(paper)
                    else:
                        if paper.updated >= self.date_from and paper.updated <= self.date_until:
                            list_papers.append(paper)
                    if self.max_res is not None:
                        if len(list_papers) >= self.max_res:
                            pending_results =  False
                            break
            except KeyError as e:
                pending_results = False
                break


            # Update for next iteration
            start_res += self.fetching_number_per_iter
            iter_number += 1

            pbar.update(self.fetching_number_per_iter)

        return list_papers
