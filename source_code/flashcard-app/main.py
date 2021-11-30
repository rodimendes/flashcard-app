from tkinter import *
import pandas
import random

BG_COLOR = "#3A3A3A"
TITLE_FONT = "Arial", 60, "bold"
WORD_FONT = "Arial", 50, "italic"

current_card = {}  # Criou o dicionário como variável global VER NEXT_CARD()

try:
    data = pandas.read_csv("card/english_words.csv")
except FileNotFoundError:
    data = pandas.read_csv("english_words.csv")

data_dict = data.to_dict(orient="records")  # Transforma o DataFrame em Dicinário e ajusta a sequencia para Coluna > valor

learned_words = {
            "English": [],
            "Portugues": [],
        }


def next_card():
    global current_card, flip_card_timer  # Acessa a variável global
    my_canvas.after_cancel(id=flip_card_timer)
    current_card = random.choice(data_dict)  # Altera a variável global. Assim, a outra função utiliza o valor atualizado
    my_canvas.itemconfig(canvas_front_card, image=front_card_img)
    my_canvas.itemconfig(title_canvas_card, text="English", fill="black")
    my_canvas.itemconfig(word_canvas_card, text=current_card["English"], fill="black")
    flip_card_timer = my_canvas.after(3000, func=flip_card)


def flip_card():
    my_canvas.itemconfig(canvas_front_card, image=back_card_img)
    my_canvas.itemconfig(title_canvas_card, text="Português", fill="white")
    my_canvas.itemconfig(word_canvas_card, text=current_card["Portugues"], fill="white")
    my_canvas.after_cancel(flip_card)


def i_know():
    learned_words["English"].append(current_card["English"])
    learned_words["Portugues"].append(current_card["Portugues"])
    learned_words_df = pandas.DataFrame(learned_words)
    learned_words["English"] = []
    learned_words["Portugues"] = []
    try:
        with open("card/learned_words.csv") as lw:
            learned_words_df.to_csv("card/learned_words.csv", index=False, mode="a", header=False)
    except FileNotFoundError:
        learned_words_df.to_csv("card/learned_words.csv", index=False)
    data_dict.remove(current_card)
    to_learn = pandas.DataFrame(data_dict)
    to_learn.to_csv("card/english_words.csv", index=False)
    next_card()


my_window = Tk()
my_window.title("FlashCard do Angelo")
my_window.config(padx=20, pady=20, bg="#A7D8C0")
# my_window.minsize(1000, 700)
# my_window.config(bg=BG_COLOR)

my_canvas = Canvas(my_window, width=800, height=526, borderwidth=0, highlightthickness=0)  # highlightthickness=0 e borderwidth=0
front_card_img = PhotoImage(file="card/card_front.gif")
back_card_img = PhotoImage(file="card/card_back.gif")
canvas_front_card = my_canvas.create_image(400, 263, image=front_card_img)
title_canvas_card = my_canvas.create_text(400, 100, font=TITLE_FONT)  # Texto deve ser colocado após a criação da imagem
word_canvas_card = my_canvas.create_text(400, 250, font=WORD_FONT)
flip_card_timer = my_canvas.after(3000, func=flip_card)
my_canvas.grid(column=0, row=0, columnspan=2)

known_button = Button(borderwidth=0, highlightthickness=0)
know_button_image = PhotoImage(file="card/right.gif")
known_button.config(image=know_button_image, borderwidth=0, command=i_know)
known_button.grid_propagate(False)
known_button.grid(column=0, row=1)
unknown_button = Button()
unknown_button_image = PhotoImage(file="card/wrong.gif")
unknown_button.config(image=unknown_button_image, borderwidth=0, command=next_card)
unknown_button.grid(column=1, row=1)

next_card()

my_window.mainloop()
