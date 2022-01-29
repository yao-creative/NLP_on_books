import pickle
import os
import classes
SAVE_PDF_PATH = "../books_pdf"
SAVE_VAR_PATH = "../books_var"
SAVE_TEXT_PATH = "../books_txt"
for title in os.listdir(SAVE_VAR_PATH):
    if f"{SAVE_TEXT_PATH}/{title}.txt" in os.listdir(SAVE_TEXT_PATH):
        continue
    book = pickle.load(open(f"{SAVE_VAR_PATH}/{title}", "rb"))
    print(f"book: {title} \n link: {book.link}")
    book.save_text()
    #pickle.load(SAVE_VAR_PATH)