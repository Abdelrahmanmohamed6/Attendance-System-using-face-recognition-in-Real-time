import DB
import Student

import os
import pickle
import numpy as np
from datetime import datetime

import cv2
import cvzone
import face_recognition
import matplotlib.pyplot as plt

import firebase_admin
from firebase_admin import db
from firebase_admin import storage
################################ DataBase Connection and Retrive Data #################################
# 
##ACCESS FIREBASE REAL TIME DATABASE
if not firebase_admin._apps:
     ref ,bucket=DB.dbconn_ref_bucket()
else:
     app=firebase_admin.get_app()
     ref=firebase_admin.db.reference("Students")
     bucket=storage.bucket()

##ACCESS RESOURCES
img_background=cv2.imread("resources/background.png")

folder_of_modes=os.listdir("resources/modes")
modes=[cv2.imread(os.path.join("resources/modes",path)) for path in folder_of_modes ]

##RETRIVE SAVED ENODED IMGS  
with open("encoding.p","rb") as file:
     encoded_imgs , student_ids = pickle.load(file)


###############################Live Camera#################################################################
modetype=0
counter=0
id=-1
img_student=[]

cap=cv2.VideoCapture(0)
cap.set(1,640)#x size
cap.set(2,480)#y size

while True: 
    # print(counter)
    ret, frame = cap.read()
    
    imgs=cv2.resize(frame,(0,0),None,0.25,0.25)
    imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
    img_background[195:195+480,75:75+640]=frame
    img_background[112:112+633,800:800+414]=modes[modetype]

    if len(student_ids)>0:
        face_cur_frame=face_recognition.face_locations(imgs)
        face_encoded=face_recognition.face_encodings(imgs,face_cur_frame)

        ##if any face detected
        if face_cur_frame:
            for face_loc , face_encod in zip(face_cur_frame,face_encoded):
                matches=face_recognition.compare_faces(encoded_imgs,face_encod)##boolean for recognision
                distance=face_recognition.face_distance(encoded_imgs,face_encod)##list of distances

                matchIndex = np.argmin(distance)

                if matches[matchIndex]:
                    id=student_ids[matchIndex]

                    y1,x2,y2,x1=face_loc
                    y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1

                    img_background=cvzone.cornerRect(img_background,bbox,rt=0)

                    if counter==0:

                        cvzone.putTextRect(img_background,"Loading....",(275, 400))
                        cv2.imshow("Live",img_background)#overflowing on currnt camera
                        cv2.waitKey(1)
                        counter = 1
                        modetype = 1    #go to student status 
            if counter!=0:
    # 
    # 
                if counter==1:#there is face detected
                    ##Get the data
                    student_info=ref.child(id).get()
                    blob=bucket.get_blob(f'Images/{id}.jpg')


                    array=np.frombuffer(blob.download_as_string(), np.uint8)
                    img_student=cv2.imdecode(array,cv2.COLOR_BGR2RGB)


                    datetimeObject = datetime.strptime(student_info['last_attendance_time'],"%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    # print(secondsElapsed)

                    if secondsElapsed > 30:#the time that allows for next assignment
                        stu=ref.child(id)
                        student_info['total_attendance'] += 1
                        stu.child('total_attendance').set(student_info['total_attendance'])
                        stu.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modetype = 3        #already marked
                        counter = 0
                        img_background[112:112+633,800:800+414]=modes[modetype]
    # 
    # 
                if modetype != 3:#if not already marked

                        if 10 < counter < 20:
                            modetype = 2  #congrats you are registered

                        img_background[112:112+633,800:800+414]=modes[modetype]

                        if counter <= 10:#still showing student status
                            

                            cv2.putText(img_background, str(student_info['total_attendance']), (860, 185),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                            cv2.putText(img_background, str(student_info['major']), (992 , 615),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            cv2.putText(img_background, str(id), (992, 555),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            
                            (w, h), _ = cv2.getTextSize(student_info['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                            offset = (414 - w) // 2
                            cv2.putText(img_background, str(student_info['name']), (800 + offset, 500),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                            
                            img_background[243:243+216,901:901+216] = img_student

                        counter += 1

                        if counter >= 20:#return to active mode
                            counter = 0
                            modetype = 0
                            studentInfo = []
                            img_student = []
                            img_background[112:112+633,800:800+414]=modes[modetype]
        else:
                modetype = 0
                counter = 0


    cv2.imshow("Live",img_background)


    # Breaking gracefully
    if cv2.waitKey(1) & 0XFF == ord('q'):
            Student.to_csvv()
            break    
    if cv2.waitKey(1) & 0XFF == ord('a'):
            Student.window_addStudent()
            with open("encoding.p","rb") as file:
              encoded_imgs , student_ids = pickle.load(file)  
    if cv2.waitKey(1) & 0XFF == ord('d'):
            Student.window_deleteStudent()
            with open("encoding.p","rb") as file:
              encoded_imgs , student_ids = pickle.load(file) 
# Release the webcam
cap.release()
# Close the image show frame
cv2.destroyAllWindows()

