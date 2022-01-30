import book_scraper
import time
import os
    
LIMIT = 10

def main():
    start = time.time()
    original_num_books= len(os.listdir('../books_var'))
    url ="https://www.gutenberg.org/ebooks/bookshelf/68"  
    gutenberg_crawler = book_scraper.Book_Crawler(url, ftypes= ["pdf", "txt"])
    gutenberg_crawler.run("link", href_not_contains = "bookshelf")
    scrape = True
    i = 1
    
    while scrape and i < LIMIT:
        try:
            index = i*25 +1
            #print(f"index: {index}")
            new_url = f"{url}?start_index={index}"
            print(f"url: {new_url}")
            gutenberg_crawler = book_scraper.Book_Crawler(new_url, ftypes= ["pdf", "txt", "utf-8"])
            gutenberg_crawler.run("link", href_not_contains = "bookshelf")
        except:
            scrape = False
        i+=1
    print(f"Books scraped {len(os.listdir('../books_var')) -original_num_books}")
    print(f"Time taken: {time.time()- start}")






    
if __name__ == "__main__":
    main()