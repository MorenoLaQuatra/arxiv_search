from setuptools import setup, find_packages

version = open('VERSION').read().strip()
license = open('LICENSE').read().strip()

setup(
    version = version,
    license = license,
    name = "arxiv_search",
    author = "Moreno La Quatra",
    author_email = "moreno.laquatra@gmail.com",
    url = "https://github.com/MorenoLaQuatra/arxiv_search",
    description = 'A python interface to scrape arXiv.org',
    long_description = open('README.md').read().strip(),
    packages = find_packages(),
    keywords = ["arxiv", "text-mining", "search"],
    install_requires=[
        # put packages here
        'xmltodict',
        'tqdm',
    ],
    test_suite = 'tests',
    entry_points = {
	    'console_scripts': [
	        'packagename = packagename.__main__:main',
	    ]
	}
)