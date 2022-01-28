import book_scraper


    
        
def main():
    url ="https://www.gutenberg.org/ebooks/bookshelf/102"
    gutenberg_crawler = book_scraper.Book_Crawler(url, ftypes= ["pdf", "txt"])
    gutenberg_crawler.run("link", href_not_contains = "bookshelf")







    
if __name__ == "__main__":
    main()