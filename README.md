## Purpose
Scrape books: do stuff with them

## Installing Requirements:
Type ```pip install -r requirements.txt```
## How to use book scraper:
### About:
   The book scraper is an easy way to scrape any ".txt", ".pdf," ".utf-8," etc... type files from a webpage.
If no initial link to a targeted file type is found on the page it will look for the keywords: "read more," "pdf," and "download"
and follow the links to potentially find the targeted file before reaching a max crawl limit. All files found will be saved to pdf and txt.
### __Similar to the Gutenberg_scrape.py__: 
You just need to 
1) Change your pdf, text paths in class.py and book_scraper.py
SAVE_PDF_PATH 
SAVE_TEXT_PATH

2) Change MAXDEPTH to the depth of crawl if the crawler can't find the target file type.
4) Create new folder
Code:
```
Import classes
Import book_scraper

book_crawler = book_scraper.Book_Crawler(url, ftypes = filetypes)
book_crawler.run(link_class, href_contains = "", href_not_contains = None)

```
__url__: is the page full of urls which might potentially lead to the files you want to download. 
__ftypes__: a list of strings, file types endings of files you want to download.
__link_class__: obtained from inspecting element of individual listing urls in the url page, the class of the '<a>' type element.
__href_contains__: when searching for links which might potentially lead to the targeted file type, __href_contains__ states the necessary substring within the link.
__href_not_contains__: when searching for links which might potentially lead to the targeted file type, __href_contains__ states the substring which shouldn't be in the link.

## Ideas:
### 1) Make Summaries
### 2) Generate Adequate book titles
### 3) Give More Book Recommendations based on NLP?
### 4) Create mini-course using resources from different books
### 5) Auto generate key concepts quiz after summarizing
### 6) Auto generate review quiz
### 7) Read Problem Sets and Guess the main topics covered
### 8) Create a book chat bot
### 9) Write sentences in the style of the book
### 10) Thematic analysis?
   
