import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage


# from Student import Student

def dbconn_ref_bucket():
      cred = credentials.Certificate("serviceAccountKey.json")
      db_init=firebase_admin.initialize_app(cred,
                              {"databaseURL":"", 
                               ""}
                                           )
      ref=db.reference("Students")
      bucket=storage.bucket()
      return ref ,bucket

ref ,bucket=dbconn_ref_bucket()



## for key, value in data.items():
##     ref.child(key).set(value)
## student_info=db.reference(f'Students/{id}').get()
## ref = db.reference(f'Students/{id}')
## print(ref.child("20211368487").get())


