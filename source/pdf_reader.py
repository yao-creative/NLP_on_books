import classes

    
        
def main():
    L1 = classes.Library()
    b1 = classes.Book("Automata_and_Computability","../books_pdf/Automata_and_Computability.pdf")
    b1.retrieve_text()
    L1.add_book(b1)
    







    
if __name__ == "__main__":
    main()