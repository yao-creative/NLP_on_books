from googlesearch import search
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool
import requests
import urllib.error
import urllib.request
import urllib.parse
import pickle
import time
import ssl
from urllib.parse import urlparse
import qwant

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


genericUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

#maybe use an alternative to google
# def search_ddg(keyword):
#     print(f"key word: {keyword}")
#     req = "https://duckduckgo.com/?q=" +  urllib.parse.quote(keyword)
#     print(f"req: {req}")
#     c = requests.get(req, verify=False)                        #try open website
#     #print(f"dir(c): {dir(c)}, dir(c.content): {dir(c.content)}")
    
#     soup = BeautifulSoup(c.content, "lxml")
#     with open("temp.html", "w", encoding = 'utf-8') as file:
#         file.write(str(soup.prettify()))
#     res = soup.find_all("a", {"class": "js-result-title-link"})
#     print(f"res: {res}")
#     return res #return all links 

def search_qwant(keyword):
    # print(f"key word: {keyword}")
    # req = "https://duckduckgo.com/?q=" +  urllib.parse.quote(keyword)
    # print(f"req: {req}")
    # c = requests.get(req, verify=False)                        #try open website
    # #print(f"dir(c): {dir(c)}, dir(c.content): {dir(c.content)}")
    
    # soup = BeautifulSoup(c.content, "lxml")
    # with open("temp.html", "w", encoding = 'utf-8') as file:
    #     file.write(str(soup.prettify()))
    # res = soup.find_all("a", {"class": "js-result-title-link"})
    search = qwant.search(keyword)
    print(f"search: {search}")
    res = qwant.items(keyword, count = 30)
    print(f"res: {res}")
    return res #return all links 



SAVE_PDF_PATH = "../books_pdf"
SAVE_SUM_PATH = "../summary_txt" #path to summary saves.
MAXDEPTH = 4


def perform_search(title):
    """Perform search for the title summaries and save it's texts into files
    return quadruples of (url, domain, starting depth = 0 , maxdepth) used for crawl"""
    
    dir_path =f"{SAVE_SUM_PATH}/{title}"
    
    try:
        os.mkdir(dir_path) #create a directory if needed
    except:
        pass
    
    query = title + " summary"
    print(f"query: {query}")
    search_results = list()
    
    time.sleep(1)
    search_results = search_qwant(query)
    return search_results


def save(title, dir_path, text):
    
    with open(f"{dir_path}/{title}", "w") as infile:
        infile.write(text)
        infile.close()
        
def find_summaries(tup): 
    """Go the summary link site, search for headers or sections with summaries and extract their text
    quintuple = link, depth, domain, dir_path, maxdepth 
    Link: is the link to the page to crawl
    Depth: is the current depth crawled
    """
    #link, domain, dir_path, depth, maxdepth = quintuple #unpack quintuple
    # if depth > maxdepth: #If we've searched too far stop searching
    #     return -1
    title, list_url = tup
    dir_path =f"{SAVE_SUM_PATH}/{title}"
    
    for url in list_url:
        parsed = urlparse(url)
        site = parsed.netloc
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        paragraphs = soup.find_all("p")
        with open(f"{dir_path}/{site}.txt") as infile:
            for p in paragraphs:
                infile.writelines(p.text)
            infile.close()
            
def dump_var(variable, filename):
    """Dumps search search_results into a var file"""
    with open(filename, "wb") as infile:
        pickle.dump(variable, infile)
def read_search():
    try:
        with open("search_results.var", "wb") as infile:
            search_results = pickle.load(infile)   
            return search_results
    except: 
        print("resutls.var was not found")
        return []
    
def main():
    
    titles = list()
    #if "search_results.txt" not in os.listdir("."):
    
    for title in os.listdir(SAVE_PDF_PATH): #find all books to search
        titles.append(title[:-4])
    search_results = list()
    
    for title in titles: #perform queries
        found = perform_search(title)
        if len(found) == 0:
            break
        search_results.append(found) #trying not to angry the almighty google search webmaster
        print(f"search results: {search_results}")
    #very naive way to 
    try:
        prev_results = read_search()
        if len(search_results)> len(prev_results):
            dump_var(search_results, "search_results.var") 
    except: pass 
    
    search_results = read_search()
    searched_titles = [titles[i] for i in range(len(titles)) if len(search_results[i]) > 0]
    dump_var(searched_titles, "searched_titles.var")
    if len(search_results) > 0 and len(titles) > 0:
        list_tup = [(titles[i],search_results[i]) for i in range(len(titles))]
        p2 = Pool()
        summaries = p2.map(find_summaries, list_tup)
        p2.close()
        p2.join()
        
    print("Done")

if __name__ == "__main__":
    search_qwant("the bible")
    # main()