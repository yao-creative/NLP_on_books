import PyPDF4
import pickle
import threading
import logging


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
    
    def __init__(self, title, path):
        """title = title of the book save file (better to have underscores), path is path to book pdf"""
        
        try:
            if path[-3:] != "pdf":
                print(f"title: {title} was not a pdf file")
                return -1
            self.title = title
            self.path = path
            self.pdfReader = None # create a dictionary of text where each key is page and value is text on a page
        except:
            return -1
        
    def retrieve_text(self, auto_save=True):
        """Given the book with the title and path properties auto save set to true"""
        
        try:

            pdfFileObj = open(self.path, 'rb')  #select file
            self.pdfReader = PyPDF4.PdfFileReader(pdfFileObj,strict=False)
            numberPages = self.pdfReader.numPages
    
            logging.info(f"Retrieved: \033[92m {self.title}")
            logging.info(f"Number of Pages: \033[92m {self.pdfReader.numPages}")
            
            
            if auto_save: #save the books
                self.save()
                
                
        except:
            print(f"Could not find: {self.path}")
            
            
    def save(self):
        with open(f"books_txt/{self.title}.var", "wb") as outfile1:
            pickle.dump(self.pdfReader, outfile1)
        with open(f"books_var/{self.title}.txt", "w") as outfile2:
            outfile2.write("\n_____________________________________________\n".join(self.text.values()))
        logging.info(f"File Saved, Title: \033[35m {self.title}")