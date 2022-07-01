import logging
import datetime
import sys
import re

PYTHON3 = sys.version_info[0] == 3
if PYTHON3:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import HTTPError
else:
    from urllib import urlencode
    from urllib2 import HTTPError, urlopen

from arxiv_search.constants import BASE_URL_DOWNLOAD_SOURCE

class Paper(object):
    """
    A class that contains all the information of a single publication parsed from arxiv.
    """

    def __init__(self, dict_info):
        super(Paper, self).__init__()
        self.id, self.id_url = self.get_ids(dict_info)
        self.categories = self.get_categories(dict_info)
        self.authors = self.get_authors(dict_info)
        self.comment = self.get_comment(dict_info)
        self.abstract = self.get_key(dict_info, "summary")
        self.abstract = self.abstract.replace("\n", " ")
        self.abstract = re.sub('\s+',' ',self.abstract)
        self.title = self.get_key(dict_info, "title")
        self.title = self.title.replace("\n", " ")
        self.title = re.sub('\s+',' ',self.title)
        self.updated = self.get_key(dict_info, "updated")
        self.updated = datetime.datetime.strptime(self.updated[:10], '%Y-%m-%d')
        self.published = self.get_key(dict_info, "published")
        self.published = datetime.datetime.strptime(self.published[:10], '%Y-%m-%d')


    def get_key(self, dict_info, key):
        try:
            return dict_info[key]
        except Exception as e:
            logging.error(f"{key} not found in paper info, {e}")
            return None

    def get_ids(self, dict_info, key="id"):
        try:
            return dict_info[key].split("/")[-1], dict_info[key]
        except Exception as e:
            logging.error(f"{key} not found in paper info, {e}")
            return None

    def get_comment(self, dict_info, key="arxiv:comment"):
        if key in dict_info.keys():
            if "#text" in dict_info[key].keys():
                return dict_info[key]["#text"]
            else: return None
        else: return None

    def get_authors(self, dict_info, key="author"):
        try:
            if isinstance(dict_info[key], list):
                authors_list = []
                for e in dict_info[key]:
                    authors_list.append(e["name"])
                return authors_list
            else: #only one author
                return [dict_info[key]["name"]]

        except Exception as e:
            print (dict_info)
            logging.error(f"{key} not found in paper info, {e}")
            return None


    def get_categories(self, dict_info, key="category"):
        try:
            if isinstance(dict_info[key], list):
                cat_list = []
                for e in dict_info[key]:
                    cat_list.append(e["@term"])
                return cat_list
            else: #only one category
                return [dict_info[key]["@term"]]
        except Exception as e:
            logging.error(f"{key} not found in paper info, {e}")
            return None

    def __repr__(self):
        return "Paper()"
    
    def get_dict(self):
        d = {}
        d["id"] = self.id
        d["id_url"] = self.id_url
        d["categories"] = self.categories
        d["authors"] = self.authors
        d["comment"] = self.comment
        d["abstract"] = self.abstract
        d["title"] = self.title
        d["updated"] = self.updated
        d["published"] = self.published
        return d

    def __str__(self):
        return str(self.get_dict())

    def download(self, download_url, path_to_file):
        response = urlopen(download_url)
        file = open(path_to_file, 'wb')
        file.write(response.read())
        file.close()

    def download_pdf(self, path_to_file):
        download_url = self.id_url.replace("abs", "pdf")
        self.download(download_url, path_to_file)
        

    def download_source(self, path_to_file):
        download_url = BASE_URL_DOWNLOAD_SOURCE + self.id
        self.download(download_url, path_to_file)
