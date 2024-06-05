from TextSplitter import TextSplitter
from TextClassifier import TextClassifier
from CaptionCreator import CaptionCreator
from WordPrompterCreator import WordPrompterCreator
from PPTCreator import PPTCreator
from Setting import PPT_SONG
from GUI import GUI
import tkinter as tk


def handle_prompter_song(text_content):
    splitted_texts = text_splitter.split_text(text_content)
    classified_texts = text_classifier.classify_text(splitted_texts)
    texts = text_splitter.split_long_texts(classified_texts)
    ppt = PPTCreator(PPT_SONG.back_color)
    ppt.create_slide(texts)


def handle_caption_song(text_content):
    splitted_texts = text_splitter.split_text(text_content)
    classified_texts = text_classifier.classify_text(splitted_texts)
    caption_creator.create_caption(classified_texts)


def handle_prompter_word(file_content, person):
    word_prompter_creator = WordPrompterCreator(person)
    word_prompter_creator.prompter_make(file_content)


text_splitter = TextSplitter()
text_classifier = TextClassifier()
caption_creator = CaptionCreator()

root = tk.Tk()
gui = GUI(root)
gui.show()
gui.callback_prompter_song = handle_prompter_song
gui.callback_caption_song = handle_caption_song
gui.callback_prompter_word = handle_prompter_word


gui.root.mainloop()
