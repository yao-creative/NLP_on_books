import PyPDF4
import pickle
import threading
import logging
import os
import requests

#Paths to save where the books are
SAVE_PDF_PATH = "../books_pdf"
SAVE_VAR_PATH = "../books_var"
SAVE_TEXT_PATH = "../books_txt"
class Library(): #collection of books
    
    #one day will automate "fill library" where it will fill it self with web scrapped books for processing
    
    def __init__(self):
        self.books = dict()
        
        
    def add_books(self,books_list):
        """Add a list of book objects to the library dictionary"""
        for book in books_list:
            if (book.title,book.path) not in self.books: #store the books in the dictionary
                self.books[(book.title,book.path)] = book
            
            
            
class Book(): #book contains processable texts
    
    def __init__(self, title, link):
        """title = title of the book save file (better to have underscores), path is path to book pdf"""
        
        try:
            self.title = title
            self.link = link
            self.pdfReader = None # create a dictionary of text where each key is page and value is text on a page
            self.possible_formats={"pdf_possible": True,
                "var_possible": True,
                "txt_possible": True}
        except:
            return -1
                       
    def save(self):
        #check if files are already existing, else save.
        
        try:
            self.save_pdf()
        except:
            self.possible_formats["pdf_possible"] =False
        try: 
            self.save_text()
        except:
            self.possible_formats["txt_possible"] =False
        try: 
            self.save_var()
        except:
            self.possible_formats["var_possible"] =False
        
        for possible in self.possible_formats:
            print(f"Saved {possible}: {self.possible_formats[possible]}", end=" ")
        print("")
        
    def create_pdfReader(self):
        
        pdfFileObj = open(f"{SAVE_PDF_PATH}/{self.title}.pdf", "rb")
        self.pdfReader = PyPDF4.PdfFileReader(pdfFileObj,strict=False)
        
        
    def save_var(self): #Save the variable version
        if "{self.title}.var" not in os.listdir(SAVE_VAR_PATH):    
            with open(f"{SAVE_VAR_PATH}/{self.title}.var", "wb") as outfile1:
                pickle.dump(self.pdfReader, outfile1)
                outfile1.close()

                
    def save_text(self): #Save the text
        if "{self.title}.txt" not in os.listdir(SAVE_TEXT_PATH):
            if self.possible_formats["pdf_possible"]: #If file has pdf form save using pdf form
                with open(f"{SAVE_TEXT_PATH}/{self.title}.txt", "w") as outfile2:
                    outfile2.write("\n\n\n".join(self.text.values()))
                    outfile2.close()
            elif self.link[-3:] == "txt":
                r = requests.get(self.link)
                with open(f"{SAVE_TEXT_PATH}/{self.title}.txt", "w") as outfile2:
                    outfile2.write(bytes.decode(r.content))
                    outfile2.close()
                logging.info(f"File Saved, Title: \033[35m {self.title}")
        
    def save_pdf(self):
        """Write the pdf into the a file"""
        
        logging.info(f"Writing: {self.title} as pdf")
        r = requests.get(self.link) #use the link and write content
        if "{self.title}.txt" not in os.listdir(SAVE_PDF_PATH): 
            pdf = open(f"{SAVE_PDF_PATH}/{self.title}.pdf", "wb")
            pdf.write(r.content)
            pdf.close()
        
        self.create_pdfReader()