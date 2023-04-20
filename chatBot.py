import mysql.connector as cnctr
import random as rn
import pyttsx3
import wikipedia
from datetime import date
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
    def newReg():
        print("PLEASE PROVIDE YOUR CREDENTIAL:")
        speak("PLEASE PROVIDE YOUR CREDENTIAL:")
        global uid
        uid=input("USER ID: ")
        pswd=input("PASSWORD: ")
        pswdConf=input("CONFIRM PASSWORD: ")
        if pswd==pswdConf:
            qry="select * from user where uid='{}'".format(uid)
            myCur.execute(qry)
            myCur.fetchall()
            if myCur.rowcount<=0:
                qry="insert into user(uid, pswd, utype, usess, dbstat) values('{}', '{}', '{}', '{}', '{}')".format(uid, pswd, '2', '', 'C')
                myCur.execute(qry)
                myCon.commit()
            else:
                print("USER ID ALREADY EXISTS. PLEASE LOGIN WITH YOUR CREDENTIAL.")
        else:
            print("PASSWORD AND CONFIRM PASSWORD DOES NOT MATCH")
            
    def login():
        print("PLEASE PROVIDE YOUR CREDENTIAL:")
        speak("PLEASE PROVIDE YOUR CREDENTIAL:")
        global uid
        uid=input("USER ID: ")
        pswd=input("PASSWORD: ")
        qry="select * from user where uid='{}' and pswd='{}'".format(uid, pswd)
        myCur.execute(qry)
        myCur.fetchall()
        if myCur.rowcount<=0:
            print("INVALID CREDENTIAL.")
            speak("INVALID CREDENTIAL.")
            login()
        else:
            speak("Hello, I am PIKACHU, the myChatBot")
            speak("What is your name?")
            unm=input()
            S="Hello "+unm
            speak(S)
            speak("How can I help you?")
    def calculateAge(birthDate):
        dob=date(int(birthDate[0:4]), int(birthDate[5:7]), int(birthDate[8:10]))
        today = date.today()
        age = today-dob
        return age
    def chatText():
        chatTxt=input()
        qry="select * from chattraining where ques='{}' or '{}' like concat(concat('%', ques),'%')".format(chatTxt, chatTxt)
        myCur.execute(qry)
        myCur.fetchall()
        if myCur.rowcount<=0:
            S='I WILL PROVIDE THE ANSWER SOON. (MAY BE IN OUR NEXT SESSION)'
            print(S)
            speak(S)
            qry="select * from userques order by qidtemp desc"
            myCur.execute(qry)
            rows=myCur.fetchall()
            if myCur.rowcount<=0:
                newQid=0
            else:
                newQid=rows[0][0]+1
            qry="insert into userques(qidtemp, uid, ques, qid) values({}, '{}', '{}', '{}')".format(newQid, uid, chatTxt, '')
            myCur.execute(qry)
            myCon.commit()
        else:
            qry="select * from chattraining where ques='{}' or '{}' like concat(concat('%', ques),'%') ORDER BY RAND() LIMIT 1".format(chatTxt, chatTxt)
            myCur.execute(qry)
            data=myCur.fetchone()
            if data[0]==1:
               S='I am '+str(calculateAge(data[2]))+' old'
            else:
                S=data[2]
            print(S)
            speak(S)
            qry="select * from userques order by qidtemp desc"
            myCur.execute(qry)
            rows=myCur.fetchall()
            if myCur.rowcount<=0:
                newQid=0
            else:
                newQid=rows[0][0]+1
            qry="insert into userques(qidtemp, uid, ques, qid) values({}, '{}', '{}', '{}')".format(newQid, uid, chatTxt, data[0])
            myCur.execute(qry)
            myCon.commit()
            if data[0]==7:
                return False
            else:
                return True
    def chatTextWiki():
        chatTxt=input(">>>")
        gb=['GOOD BYE', 'BYE', 'EXIT']
        if chatTxt.upper() in gb:
            print("GOOD BYE FROM WIKIPEDIA.")
            return False
        else:
            S=wikipedia.summary(chatTxt, sentences=4)
            print(S)
            speak(S)
            return True
    S='WELCOME TO MyChatBot'    
    print(S)
    speak(S)
    while uid=='':
        newRegVal=input("ENTER\n1. TO LOGIN\n2. FOR NEW USER\n3. TO EXIT: ")[:1]
        if newRegVal=='1':
            login()
        elif newRegVal=='2':
            newReg()
        elif newRegVal=='3':
            print("GOOD BYE")
            break
        else:
            print("INVALID CHOICE.")
        if uid=='':
            ch=input("DO YOU WANT TO CONTINUE (Y/N)?")[:1].upper()
            if ch=='N':
                break
    while True and uid!='':
        print("1. FOR GENERAL CHAT\n2. FOR WIKIPEDIA\n3. TO EXIT")
        ch=input(">>>")[:1]
        if ch=='1':
            while True:
                retVal=chatText()
                if retVal==False:
                    break
        elif ch=='2':
            while True:
                retVal=chatTextWiki()
                if retVal==False:
                    break
        elif ch=='3':
            print("GOOD BYE")
            break
        else:
            print("INVALID CHOICE.")
    myCon.close()
                  
