import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

url = "https://open.umn.edu/opentextbooks/subjects/computer-science-information-systems"
domain = "https://open.umn.edu"
def main():
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml') 
    buttons = soup.find_all("a",  {"class": "primary with-arrows"})
    to_visit = list()

    for button in buttons: #get all of the downloadable textbook links
        path = button["href"]
        
        if path and path.startswith('/'):
            path = urljoin(domain, path)
        to_visit.append(path)
        
    print(f"to_visit: {to_visit}")
    while len(to_visit) > 0:
        link = to_visit.pop()
        extract_save_pdf(link)
    
def extract_save_pdf(link):
    """Go the textbook link site, click on download button and save to a books_pdf the file"""
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml') 
    buttons = soup.find_all("a", string = "PDF")
    try:
        path = buttons[0]["href"]
        if path and path.startswith('/'):
            path = urljoin(domain, path)
        r2 = requests.get(path)
        soup2 = BeautifulSoup(r2.content, 'lxml') 
    except:
        print(f"No pdf found on site: {soup.title}")
    #print(f"buttons 0: {buttons[0]['href']}")
    #for button in buttons:
        
    #print(f"buttons: {dir(buttons)}")
if __name__ == "__main__":
    main()
    