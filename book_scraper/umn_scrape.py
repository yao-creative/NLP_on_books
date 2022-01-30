import book_scraper


    
        
def main():
    url ="https://open.umn.edu/opentextbooks/subjects/computer-science-information-systems"
    umn_crawler = book_scraper.Book_Crawler(url, ftypes= ["pdf", "txt"])
    umn_crawler.run("primary with-arrows", href_not_contains = "bookshelf")



    
if __name__ == "__main__":
    main()