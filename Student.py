import os
from datetime import datetime
import cv2
import shutil
import numpy as np

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import pickle

import DB 
import firebase_admin
from firebase_admin import db
from firebase_admin import storage

import face_recognition
import pandas as pd
################################ DataBase Connection and Retrive Data #################################
# 
##ACCESS FIREBASE REAL TIME DATABASE
if not firebase_admin._apps:
     ref ,bucket=DB.dbconn_ref_bucket()
else:
     app=firebase_admin.get_app()
     ref=firebase_admin.db.reference("Students")
     bucket=storage.bucket()

#####################################################################################################
entries = []; data={} ;encode=np.empty(0)
filepath="" ; id=""

def Student_informations(id,name,major,minor,grade,last_attendance_time,total_attendance):
         id=str(id)#key must to be string
         data[id]={
               "name":name,
               "major":major,
               "minor":minor,
               "grade" :grade ,
               "last_attendance_time":last_attendance_time,
               "total_attendance":total_attendance
         }
         ref.child(id).set(data[id])

def Student_files(encoded_img,id,folder_path="Images"):
        try:
                file_name=f'{folder_path}/{id}.jpg'
                blob=bucket.blob(file_name)
                blob.upload_from_filename(file_name)
                with open("encoding.p", "rb") as file:
                        encoded_imgs, student_ids = pickle.load(file)
                        encoded_imgs.append(encoded_img)
                        student_ids.append(id)
                with open("encoding.p", "wb") as file:
                        pickle.dump([encoded_imgs, student_ids], file)
        except:
                print("Error while uploading/reading files")


def window_addStudent():
        root = tk.Tk()
        root.title("Student Information")
        root.geometry("600x600")
        content_frame = tk.Frame(root, padx=10, pady=80)
        content_frame.pack()
        # Define labels and text fields
        parameters = ['ID', 'Name', 'Major', 'Minor', 'Grade', 'Last Attendance Time', 'Total Attendance']
        tk.Label(content_frame, text="Please Fill Fileds", fg='black', font=('Helvetica', 20)).grid(column=1)
        for i, parameter in enumerate(parameters):
                i=i + 1
                tk.Label(content_frame, text=parameter, fg='black', font=('Helvetica', 16)).grid(row=i,pady=5)
                entry = tk.Entry(content_frame, bg='white', fg='black', font=('Helvetica', 16))
                entry.grid(row=i, column=1,pady=5) 

                if parameter =="Last Attendance Time":
                                entry.insert(i,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                entry.config(state="disable")
                if parameter =="Total Attendance":  
                                entry.insert(i,0)   
                                entry.config(state="disable")

                entries.append(entry)

        # Function to open the file dialog and print the selected file path

        def upload_file():
                global filepath
                global encode
                global img
                filepath= os.path.join(filedialog.askopenfilename())
                if filepath!="":
                        try:
                                img=cv2.imread(filepath)
                                encode=face_recognition.face_encodings(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))[0]
                                img=cv2.resize(img,(216,216),interpolation=cv2.INTER_AREA)

                        except:
                                messagebox.showwarning("error on uploaded image!","you enter invalid image make sure the image contains one face")
                return encode
# 
# 
        def submit():
                student_info=[]
                global id
                global flag

                for parameter, entry in zip(parameters, entries):
                        if entry.get()=="":
                                break
                        else:
                                # try
                                if parameter=="ID" :
                                        # if len(entry.get())==11:#20211******
                                          id=str(entry.get())
                                          student_info.append(int(entry.get()))
                                        # else:
                                        #         break
                                elif parameter=='Total Attendance':
                                        student_info.append(int(entry.get()))
                                elif parameter=='Grade':
                                        student_info.append(float(entry.get()))
                                else:
                                        student_info.append(entry.get())
#                       
#                                 
                if len(student_info)==7 and encode.size>0:
                                try:
                                        cv2.imwrite(f"Images/{id}.jpg",img)
                                        ### shutil.copy2(filepath,f"Images\\{id}.jpg")
                                        Student_informations(*student_info)
                                        Student_files(encode,id)
                                        root.destroy()
                                        print(":) student added successfully")
                                except:
                                        print("Student didn' not added")

                                        
        # Add a file upload button
        tk.Button(content_frame, text='Upload File', command=upload_file, bg='blue', fg='white', font=('Helvetica', 16)).grid(row=len(parameters)+1, column=1,pady=5)

        # Add a submit button
        tk.Button(content_frame, text='Submit', command=submit, bg='green', fg='white', font=('Helvetica', 16)).grid(row=len(parameters)+2, column=1,pady=5)
        submit()
        root.mainloop()
        return root

########################################################################
def delete_student(id,folder_path="Images"):
       try:
        id=str(id)
        with open("encoding.p", "rb") as file:
                encoded_imgs, student_ids = pickle.load(file)
                if id in student_ids:
                        idx=student_ids.index(id)
                        encoded_imgs.pop(idx)
                        student_ids.pop(idx)
        with open("encoding.p", "wb") as file:
                pickle.dump([encoded_imgs, student_ids], file)
        file_todelete=f'{folder_path}/{id}.jpg'
        ref.child(id).delete()
        blob=bucket.blob(file_todelete)
        if blob.exists():
                blob.delete()
        if os.path.exists(file_todelete):
                os.remove(file_todelete)
       except:
               print("Error while deleting")

def window_deleteStudent():
        def delete_item():
                """Function called when the button is clicked. Prints the entered ID and removes it from the list."""
                id = entry.get()
                delete_student(id)
                root.destroy()

        # Create the main window
        root = tk.Tk()
        root.geometry("600x600")
        root.title("Remove Item")
        content_frame = tk.Frame(root, padx=100, pady=100)
        content_frame.pack()
        # Create a label for the ID
        label = tk.Label(content_frame, text="Enter Item ID:",pady=20,font=('Helvetica', 20))
        label.pack(pady=10)

        # Create an entry field for the ID
        entry = tk.Entry(content_frame, width=20,font=('Helvetica', 20))
        entry.pack()

        # Create the button to delete the item
        delete_button = tk.Button(content_frame, text="Delete", command=delete_item,font=('Helvetica', 20))
        delete_button.pack()

        # Start the main loop
        root.mainloop()

def to_csvv():
        df=pd.read_csv('excel.csv')
        df=df[df["id"]==0]
        all_stu=ref.get()
        for stu_id,dictt in all_stu.items():
                dictt["id"]=stu_id
                for k,v in dictt.items():
                        dictt[k]=[v]
                inp=pd.DataFrame(dictt)
                df=pd.concat([df,inp],axis=0)
        df.to_csv('excel.csv',index=False)

to_csvv()
