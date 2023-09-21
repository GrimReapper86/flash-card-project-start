from tkinter import *
from random import choice
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
# ---------------------------- Read cvs ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ----------------------- choose random word -------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    card_front.itemconfig(canvas_image, image=card_front_image)
    card_front.itemconfig(card_title, text="French", fill="black")
    card_front.itemconfig(card_word, text=current_card['French'], fill="black")
    flip_timer = window.after(3000, flip_card)


# ---------------------------- Flip card------------------------------- #
def flip_card():
    card_front.itemconfig(canvas_image, image=card_back_image)
    card_front.itemconfig(card_title, text="English", fill="white")
    card_front.itemconfig(card_word, text=current_card['English'], fill="white")


# ------------------- Remove known word and save to file ------------------ #
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)
# Canvas
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_front = Canvas(width=800, height=526)
canvas_image = card_front.create_image(400, 263, image=card_front_image)
card_front.config(highlightthickness=0, bg=BACKGROUND_COLOR)
card_title = card_front.create_text(400, 150, text="", font=('Ariel', 40, "italic"))
card_word = card_front.create_text(400, 263, text="", font=('Ariel', 60, "bold"))
card_front.grid(row=0, column=0, columnspan=2)

# Button


right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, borderwidth=0, command=is_known)
right_button.grid(row=1, column=1)
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, borderwidth=0, command=next_card)
wrong_button.grid(row=1, column=0)
next_card()
window.mainloop()
