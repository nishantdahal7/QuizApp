from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random  # For randomizing the sequence in which questions are asked and their options are displayed
import sqlite3  # For maintaining the data of playername and their scores, adding questions & options in database
import _pickle as cPickle

game_score = 0
player_name = ""
questions_attempted = 1  # For keeping count of questions diplayed(it'll be used to diplay FINISH BUTTON on the final question)
qualifying_score = 3
errors = None  # For Error Checking while uploading question & options in database

# *********************** TIMER **************************#

time_in_sec = 20  # Total Time for Quiz


def timer():
    global time_in_sec, mylabel, button, myoptionlabel
    if (time_in_sec > 0):
        minutes, seconds = divmod(time_in_sec, 60)
        time_left = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        timer_label.config(text=time_left)
        time_in_sec -= 1
        timer_label.after(1000, timer)
    else:
        mylabel.destroy()
        button.destroy()
        myoptionlabel.destroy()
        completed_session()


# *********************** TIMER **************************#

# ************** DATABASE DATABASE DATABASE **************#

conn = sqlite3.connect('Database.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS QuizData(
         name text,
         score number
         )
         """)


# This function will be used later to Check If the player already exists in database
def get_player_name(player_name):
    c.execute("SELECT * FROM QuizData WHERE name=:name", {'name': player_name})
    return c.fetchone()


# This function is used to add player to the database with score
def insert_player(player_name, game_score):
    with conn:
        c.execute("INSERT INTO quizData VALUES (:name, :score)", {'name': player_name, 'score': game_score})


# This function is used to update the score of the player if he exists in the database already
def update_score(player_name, game_score):
    with conn:
        c.execute("""UPDATE QuizData SET score = :score
                    WHERE name = :name""",
                  {'name': player_name, 'score': game_score})


# To Create Table for User Added Questions and Options
c.execute("""CREATE TABLE IF NOT EXISTS QuestionsData(
         questions text,
         options text,
         correct_option text
         )
         """)


# To Add Question & Options in Database
def insert_question_options(question, options, correct_option):
    with conn:
        c.execute("INSERT INTO QuestionsData VALUES (:db_question, :db_options, :db_correct_option)",
                  {'db_question': question, 'db_options': options, 'db_correct_option': correct_option})


# To load Questions & Options from Database
def load_questions_options():
    with conn:
        c.execute("SELECT * FROM QuestionsData")
        return c.fetchall()


# ************** DATABASE DATABASE DATABASE **************#

# Function To Raise The Chosen Frame
def show_frame(frame):
    frame.tkraise()


# To Extract Player Details, Start Timer And Load Questions
def submit_form():
    global player_name
    load_questions_options_curr_session()
    player_name = input_name.get().split()[0]
    player_name = player_name.lower()
    frame3.tkraise()
    timer()
    load_questions()


# To Extract Questions & Options From Database And append it to the Lists & Dictionary respectively
def load_questions_options_curr_session():
    global questions, solutions, answers
    curr_session = load_questions_options()
    for curr_data in curr_session:
        curr_question = curr_data[0]
        # curr_options = eval(curr_data[1])
        curr_options = cPickle.loads(curr_data[1])
        print(curr_options)
        curr_correct_option = curr_data[2]

        if (curr_question not in questions):
            questions.append(curr_question)
            answers.append(curr_options)
            solutions[curr_question] = curr_correct_option


# Main Quiz Logic
def load_questions():
    global game_score, mylabel, button, myoptionlabel, time_in_sec, questions_attempted
    button = Button(frame3, image=next_btn, cursor="hand2", borderwidth=0, bg="black",
                    command=lambda: var.set(1))  # Next Button
    button.place(x=700, y=600)
    random.shuffle(questions)  # Shuffling Questions Sequence
    # curr_sesh_questions = questions[0:4] # To load Only 4 Questions For Current Session
    # for question in curr_sesh_questions:
    for question in questions:
        mylabel = Label(frame3, text=question, anchor=CENTER, font=("times new roman", 18, "bold"), bg="black",
                        fg="white", wraplength=800)
        mylabel.place(x=485, y=225)
        for value, key in solutions.items():
            if question == value:
                for answer in answers:
                    if key in answer:
                        random.shuffle(answer)
                        option1 = answer[0]
                        option2 = answer[1]
                        option3 = answer[2]
                        option4 = answer[3]
                        myoptionlabel = Label(frame3, bg="black")
                        myoptionlabel.place(x=700, y=330)
                        # RadioButtons For 4 Options
                        Radiobutton(myoptionlabel, text=option1, font=("times new roman", 18, "bold"), bg="black",
                                    fg="white", variable=var2, value=option1, selectcolor="#000000").pack(pady=5,
                                                                                                          anchor="w")
                        Radiobutton(myoptionlabel, text=option2, font=("times new roman", 18, "bold"), bg="black",
                                    fg="white", variable=var2, value=option2, selectcolor="#000000").pack(pady=5,
                                                                                                          anchor="w")
                        Radiobutton(myoptionlabel, text=option3, font=("times new roman", 18, "bold"), bg="black",
                                    fg="white", variable=var2, value=option3, selectcolor="#000000").pack(pady=5,
                                                                                                          anchor="w")
                        Radiobutton(myoptionlabel, text=option4, font=("times new roman", 18, "bold"), bg="black",
                                    fg="white", variable=var2, value=option4, selectcolor="#000000").pack(pady=5,
                                                                                                          anchor="w")
                        button.wait_variable(var)
                        selected_option = var2.get()
                        if selected_option == key:  # To Check If Right Option Is Selected
                            game_score += 1
                        questions_attempted += 1
                        if questions_attempted == 4:  # To Check If it's the Last Question
                            # Destroy Previous Next Button And Create a New Button with Finish Text
                            button.destroy()
                            button = Button(frame3, image=finish_btn, cursor="hand2", borderwidth=0, bg="black",
                                            command=lambda: var.set(1))
                            button.place(x=700, y=600)
                        mylabel.destroy()
                        myoptionlabel.destroy()
    button.destroy()
    time_in_sec = 0  # To Stop The Timer and Resume The Application Execution Process From Else Part Of The Timer

