import mysql.connector as cnctr
import pyttsx3
engine = pyttsx3.init()
def speak(txt):
    engine.say(txt)
    engine.runAndWait()
myCon=cnctr.connect(host='localhost', user='root', password='', database='chatbot')
if myCon.is_connected()==False:
    print('UNABLE TO CONNECT TO MYSQL DATABASE SERVER.')
    speak('UNABLE TO CONNECT TO MYSQL DATABASE SERVER.')
else:
    myCur=myCon.cursor()
    uid=''
    unm=''
    def login():
        print("PLEASE PROVIDE YOUR ADMIN CREDENTIAL:")
        speak("PLEASE PROVIDE YOUR ADMIN CREDENTIAL:")
        uid=input("ADMIN USER ID: ")
        pswd=input("ADMIN PASSWORD: ")
        qry="select * from user where uid='{}' and pswd='{}' and utype in(1)".format(uid, pswd)
        myCur.execute(qry)
        myCur.fetchall()
        if myCur.rowcount<=0:
            print("AUTHENTICATION ERROR.")
            speak("Authentication Error.")
            login()
        else:
            speak("Hello, I am Pikachu, the myChatBot. I have been deloped by Asmita Mallick on 26th June of 2022.")
            speak("What is your name?")
            unm=input("What is your name?")
            S="Hello "+unm
            speak(S)       
    print('WELCOME TO MyChatBot Training')
    speak("Welcome to my chatbot training")
    login()
    while True:
        S='Do you want to add a new question answer pair?'
        print(S,'(Y/N)')
        speak(S)
        ch=input()[:1].upper()
        if ch=='Y':
            S='Please provide the question:'
            print(S)
            speak(S)
            ques=input().capitalize()
            S='Please provide the answer:'
            print(S)
            speak(S)
            ans=input().capitalize()
            qry="select * from chattraining order by qid desc"
            myCur.execute(qry)
            rows=myCur.fetchall()
            if myCur.rowcount<=0:
                newQid=0
            else:
                newQid=rows[0][0]+1
            qry="insert into chattraining(qid, ques, ans) values({}, '{}', '{}')".format(newQid, ques, ans)
            myCur.execute(qry)
            myCon.commit()
        elif ch=='N':
            S='Good bye. Have a nice day '+unm
            print(S)
            speak(S)
            break
        else:
            S='Invalid choice. Please enter an valid option'
            print(S)
            speak(S)
    myCon.close()
                  
