import firebase_admin

from firebase_admin import db

import json

# DB Connection
cred_object = firebase_admin.credentials.Certificate('firebase_accountkey.json')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL':'https://feelinbot-default-rtdb.firebaseio.com/'
})
ref = db.reference("/")

# Retrieve all the input in a json format of a certain user.
def get_input(user_id):
    user_list = db.reference("/users/")

    users = user_list.get()

    for i in range(len(users)):
        for key, value in users[i].items():

            if key == "id" and value == user_id:
                ref = db.reference("/users/"+ str(i)+ "/inputs/")

                return ref.get()
    
# Save the input of the user depending of its ID
def set_input(user_id, inputs):
    user_list = db.reference("/users/")

    users = user_list.get()

    for i in range(len(users)):
        for key, value in users[i].items():

            if key == "id" and value == user_id:
                ref = db.reference("/users/"+ str(i))
                
                ref.child('inputs').push().set({
                    'text': inputs,
                })
