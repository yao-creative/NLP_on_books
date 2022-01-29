import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import classes
import os
from urllib.parse import urlparse
# import selenium

# from selenium import webdriver



MAXDEPTH = 3
SAVE_PDF_PATH = "../books_pdf"
SAVE_VAR_PATH = "../books_var"
SAVE_TEXT_PATH = "../books_txt" #change to relative save path

# url = "https://open.umn.edu/opentextbooks/subjects/computer-science-information-systems"
# #url = "https://open.umn.edu/opentextbooks/textbooks/deleting-dystopia-re-asserting-human-priorities-in-the-age-of-surveillance-capitalism"
# domain = "https://open.umn.edu"
# options = webdriver.FirefoxOptions()
# options.headless= True
# options.add_argument('--disable-gpu')
# driver = webdriver.Firefox(options = options)
# link_class = "primary with-arrows"
class Book_Crawler():
    
    def __init__(self,url,maxdepth= 4,ftypes=["pdf"]):
        """url str(): start url; maxdepth int(): max crawling depth; ftype list(str): pdf, epub, text"""
        self.url = url
        parsed = urlparse(url)
        self.domain = f"{parsed.scheme}://{parsed.netloc}"
        #print(f"domain: {self.domain}")
        self.ftypes = ftypes
        self.maxdepth = maxdepth
        
    def run(self, link_class, href_contains="", href_not_contains=None):
        """link_class: the class of links the crawler should go into, crawl the links for pdfs
        Optional field: href_contains making sure the potential link crawled has a certain keyword
        Optional field: href_not_contains making sure the potential link crawled does not have a certain keyword"""
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'lxml') 
        buttons = soup.find_all("a",  {"class": link_class})
        to_visit = list()
        
        for button in buttons: #get all of the downloadable textbook links
            path = button["href"]
            if href_contains not in path: #Potentially different links might have same classes but not lead to ebooks.
                #In the 
                #print(f"{href_contains} not in {path}, skip")
                continue
            if href_not_contains is not None and href_not_contains in path:
                #print(f"path: {path} has keyword, skip")
                continue
            if path and path.startswith('/'):
                
                path = urljoin(self.domain, path)
            
            to_visit.append((path, 1, self.domain, self.ftypes, self.maxdepth))
        # print(f"first link: {to_visit[0][0]}")
        # crawl(to_visit[0])
        p = Pool()
        result = p.map(crawl, to_visit)
        p.close()
        p.join()
    
    logging.info("All sites reached")
    
def parse_title(soup_title_text):
    "Parse the title into useable inputs"
    index = soup_title_text.find("-")
    out = soup_title_text[:index-1].replace(" ", "_")
    return out


        
def crawl(quintuple):
    """Go the textbook link site, click on download button and save to a books_pdf the file
    If there is no textbook download link follow the trail until there is
    Quadruple = link, depth, domain, ftypes
    Link: is the link to the page to crawl
    Depth: is the current depth crawled
    ftypes: list of file types to download
    """
    
    (link, depth, domain, ftypes, maxdepth) = quintuple #unpack elements
    if depth > maxdepth: #If we've searched too far stop searching
        return -1
    
    #print(f"Crawling: {link}")
    
    r = requests.get(link) #parse current link
    soup = BeautifulSoup(r.content, 'lxml') 
    title = parse_title(soup.title.text)
    
    
    if "{title}.var" in os.listdir(SAVE_TEXT_PATH): #If the book is already in the library 
        #print(f"Book {title}.var already in library")
        return 1
    
    pdf_path = f"{SAVE_PDF_PATH}/{title}.pdf" #add save path
    
    links = soup.find_all('a')
    hrefs = list()
    for link in links:
        hrefs.append(link.get('href'))
    
    i = 0
    try:
        for link in links:
            link_text = (link.text).lower()
            ftype_downloadable = False #if the link is a file type we want to download
            found_ftype = False #if the link might potentially lead to another link with the file download
            href = link.get('href')
            if href == "/" or href == None:
                continue
            max_ftype_len  =max(len(e) for e in ftypes)
            
            if href and href.startswith('/'): #fix the href
                href = urljoin(domain, href)
                    
            for ftype in ftypes: 
                if ftype in link_text:  
                    found_ftype = True
                if ftype in href.lower():
                    ftype_downloadable = True
                if found_ftype and ftype_downloadable:
                    break
                
            if (ftype_downloadable): #find if link is downloadable file type
                i += 1
                
                #print(f"Retrieving PDF for: {title}")
                book = classes.Book(title, href)
                book.save()
                return 1
            
            # if the pdf link isn't there look for indicators for where it might be and follow them
                
            if found_ftype or ('download' in link_text and 'downloaded' not in link_text) or "read more" in link_text: 
                crawl((href, depth+1, domain, ftypes, maxdepth)) #crawl again increasing max depth

    except:
        logging.warning(f"No links found on page: {link.text}")

    
   
    #print(f"buttons: {dir(buttons)}")

    