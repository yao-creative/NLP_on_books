import book_scraper
import time
import os
    


def main():
    start = time.time()
    original_num_books= len(os.listdir('../books_var'))
    url ="https://www.gutenberg.org/ebooks/bookshelf/102"  
    gutenberg_crawler = book_scraper.Book_Crawler(url, ftypes= ["pdf", "txt"])
    gutenberg_crawler.run("link", href_not_contains = "bookshelf")
    scrape = True
    i = 1
    while scrape:
        try:
            index = i*25 +1
            url = f"{url}?start_index={index}"
            gutenberg_crawler = book_scraper.Book_Crawler(url, ftypes= ["pdf", "txt"])
            gutenberg_crawler.run("link", href_not_contains = "bookshelf")
        except:
            scrape = False
    print(f"Books scraped {len(os.listdir('../books_var'))}")
    print(f"Time take: {time.time()- start}")






    
if __name__ == "__main__":
    main()