

# arxiv-search
A python interface to scrape arXiv.org

## Crawling arXiv.org

From [arxiv website](https://arxiv.org/help/bulk_data):

There are many users who want to make use of our data, and millions of distinct URLs behind our site. If everyone were to crawl the site at once without regard to a reasonable request rate, the site could be dragged down and unusable. For these purposes we suggest that a reasonable rate to be bursts at 4 requests per second with a 1 second sleep, per burst.

If you are using this library for mining purposes, please **consider the statement above**.

## Install

Coming once stable!

## Examples

- Without any search term

```python
from arxiv_search.arxiv_search import Scraper

scraper = Scraper(category='cs.CL', fetching_number_per_iter=1000, sortBy="submittedDate", sortOrder="descending", max_res=150) # sortBy = ["lastUpdatedDate", "submittedDate", "relevance"]
papers = scraper.get_results()

for p in papers:
    print(p.id, p.title)
    
print(f"Len papers: {len(papers)}")
```

Will be updated once stable!


# Original repository
This repository is a substantial modification of the original work by:

* **Mahdi Sadjadi**, 2017.
* Website: [mahdisadjadi.com](http://mahdisadjadi.com)
* Twitter: [@mahdisadjadi](http://twitter.com/MahdiSadjadi)

Original repo: [arxivscraper](https://github.com/mahdisadjadi/arxivscraper)


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.889853.svg)](https://doi.org/10.5281/zenodo.889853)
![](https://github.com/mahdisadjadi/arxivscraper/workflows/CI/badge.svg)
![](https://github.com/mahdisadjadi/arxivscraper/workflows/Publish%20to%20PyPi/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)