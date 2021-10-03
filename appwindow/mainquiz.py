from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import random  #this will be used to present the questions in a random manner
import sqlite3  #this will retain data like given player names and scores, questtions within the game etc
import pickle

initial_score = 0
your_name = ""
first_attempt = 1
win_requirement = 3
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

conn = sqlite3.connect("Database.db")

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Quizdata(
         name text
         score number
         )''')



#to check if the player already exists
def get_player_name(your_name):
    c.execute("Select * From QuizData Where name =: name", {'name': your_name})
    return c.fetchone()

#to add player to the database
def insert_player(your_name, initial_score):
    with conn:
        c.execute("INSERT INTO quizData VALUES (:name, :score)", {'name': your_name, 'score': initial_score})

#to update the score of players with already existing account
def update_score(your_name, initial_score):
    with conn:
        c.execute("""UPDATE Quizdata SET score =: score
                           WHERE name = : name""",
                  {'name': your_name, 'score': initial_score})


#To Create Table for User Added Questions and Options
c.execute("""CREATE TABLE IF NOT EXISTS QuestionsData(
         questions text,
         options text,
         correct_option text
         )
         """)

# To Add Question & Options in Database
def insert_question_options(question, options, correct_option):
    with conn:
        c.execute("INSERT INTO QuestionsData VALUES (:db_question, :db_options, :db_correct_option)", {'db_question':question, 'db_options':options, 'db_correct_option':correct_option})

# To load Questions & Options from Database
def load_questions_options():
    with conn:
        c.execute("SELECT * FROM QuestionsData")
        return c.fetchall()

#database end


