from arxiv_search.arxiv_search import Scraper

scraper = Scraper(category='cs.CL', fetching_number_per_iter=1000, sortBy="submittedDate", sortOrder="descending") # sortBy = ["lastUpdatedDate", "submittedDate", "relevance"]
papers = scraper.get_results()

for p in papers:
    print(p.id_url, p.title)
    #p.download_source("temp.tar.gz")

print(f"Len papers: {len(papers)}")