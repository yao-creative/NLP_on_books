import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import classes
import pickle

url = "https://open.umn.edu/opentextbooks/subjects/computer-science-information-systems"
domain = "https://open.umn.edu"
MAXDEPTH = 4
def main():
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml') 
    buttons = soup.find_all("a",  {"class": "primary with-arrows"})
    to_visit = list()

    for button in buttons: #get all of the downloadable textbook links
        path = button["href"]
        if path and path.startswith('/'):
            path = urljoin(domain, path)
        to_visit.append((path,1))
        
    p = Pool()
    result = p.map(crawl,to_visit)
    p.close()
    p.join()
    logging.info("All sites reached")
    # print(f"to_visit: {to_visit}")
    # while len(to_visit) > 0:
    #     link = to_visit.pop()
    #     extract_save_pdf(link)
def parse_title(soup_title_text):
    
    index = soup_title_text.find("-")
    return soup_title_text[:index]

def crawl(link, depth, maxdepth = MAXDEPTH):
    """Go the textbook link site, click on download button and save to a books_pdf the file"""
    
    if depth > maxdepth: #If we've searched too far stop searching
        return 
    
    r = requests.get(link) 
    soup = BeautifulSoup(r.content, 'lxml') 
    links = soup.find_all('a')
    i = 0
    
    for link in links:
        if ('.pdf' in link.get('href', [])): #find if the book pdf link is in there.
            i += 1
            response = requests.get(link.get('href'))
            title=parse_title(soup.title.text)
            book = 
            return 
    buttons = soup.find_all("a", string = "PDF")
    
    
    try:
        path = buttons[0]["href"]
        if path and path.startswith('/'):
            path = urljoin(domain, path)
        r2 = requests.get(path)
        soup2 = BeautifulSoup(r2.content, 'lxml')#get the link to the pdf copy itself then click on download
        
        #print(f"dir: {dir(soup.title)}")
        
        print(f"Book title: {soup.title.text}")
        #find some way to save to books_pdf
    except:
        print(f"No pdf found on site: {soup.title.text}")
    #print(f"buttons 0: {buttons[0]['href']}")
    #for button in buttons:
        
    #print(f"buttons: {dir(buttons)}")
if __name__ == "__main__":
    main()
    