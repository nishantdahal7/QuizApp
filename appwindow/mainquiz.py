from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import random  #this will be used to present the questions in a random manner
import sqlite3  #this will retain data like given player names and scores, questtions within the game etc
import pickle

start_score = 0
your_name = ""
first_attempt = 1
qualification = 3
errors = None


#timer start
total_quiz_time = 60 #time per question

def timer():
    global total_quiz_time, mylabel, button, myoptionlabel
    if (total_quiz_time>0):
        minutes, seconds = divmod(total_quiz_time, 60)
        time_left = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        timer_label.config(text= time_left)
        total_quiz_time -= 1
        timer_label.after(1000, timer)
    else:
        mylabel.destroy()
        button.destroy()
        myoptionlabel.destroy()
        session_complete()


#timer end

#database

conn = sqlite3.connect("database.db")

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS yourdataforquiz(
        name text
        score number
        )
        ''')






