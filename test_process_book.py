import os.path
import process_book


'''with open(os.path.join(os.path.split(os.path.dirname(__file__))[0], "/books_txt/A_Pail_of_Air_by_Fritz_Leiber.txt")) as f:
for i in range(100):
        print(f.readline())
with open("books_txt/A_Pail_of_Air_by_Fritz_Leiber.txt") as f:
    lines = ''.join([line.strip() for line in f])'''
    
print(process_book.split_sentence("books_txt/Youth_by_Isaac_Asimov.txt"))