from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import numpy as np
#from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from PIL import Image
from io import BytesIO
import pymongo
import random
import math

from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

app.secret_key = 'your_secret_key'

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.mydatabase
collection = db.collection
collection2 = db.collection2

def save_to_mongodb(name, price, text, user_name, key, nexuser, code,location):
    db.collection.insert_one({
        "name": name,
        "price": price,
        "text": text,
        "user_name": user_name,
        "key": key,
        "nexuser": nexuser,
        "status": 'off',
        "code": code,
        "location":location
    })

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

# def save_to_mongodbchat(user1, user2, chat1, chat2, time):
#     db.collection2.insert_one({
#         "user1": user1,
#         "user2": user2,
#         "chat1": chat1,
#         "chat2": chat2,
#         "time": time
#     })

# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')





@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        user_name = username
        key = hashed_password
        text2 = 'na'
        save_to_mongodb(username, 0, '', username, key, text2, random.randint(1000, 9999),None)

        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        user = collection.find_one({'user_name': username})
        if user and check_password_hash(user["key"], password):
            session['username'] = username
            
            if latitude and longitude:
                collection.update_one(
                    {'name': username},
                    {'$set': {'location': {'latitude': float(latitude), 'longitude': float(longitude)}}}
                )
            
            return redirect(url_for('home'))
        else:
            flash('Invalid username/password')
            return redirect(url_for('login'))
    return render_template('login.html')



@app.route('/index')
def index():
    return render_template('index.html')

# @app.route('/find', methods=['GET', 'POST'])
# def find():
#     if request.method == 'POST':
#         amount = request.form['amount']
#         username = session.get('username')
#         if username:
#             filter = {"name": username}
#             update = {"$set": {"price": amount}}
#             collection.update_one(filter, update)
#         return redirect(url_for('index'))
#     return render_template('find.html')
@app.route('/process_amount', methods=['GET', 'POST'])
def process_amount():
        if request.method == 'POST':
            
            amount = request.form['amount']
            username = session.get('username')
            
            if username:
                filter = {"name": username}
                update = {"$set": {"price": amount}}
                collection.update_one(filter, update)
        return redirect(url_for('find'))
    
@app.route('/select_username', methods=['POST'])
def select_username():
    # if request.method == 'POST':
    #     random_number = random.randint(1000, 9999)
    #     guser = request.form['options']
    #     username = session.get('username')
    #     filter={"name":guser}
    #     update={"$set":{"code":random_number}}
    #     collection.update_one(filter, update)
    #     if username:
    #         filter2={"name":username}
    #         update2={"$set":{"code":random_number}}
    #         collection.update_one(filter2, update2)


    # user = session.get('username')
    # query = {'nexuser': user}
    # results = collection.find(query, {"name": 1, "_id": 0})
    # options = [item["name"] for item in results]
    
    # return render_template('find.html', options=options)

     if request.method == 'POST':
        guser = request.form['options']
        username = session.get('username')
        if username:
            random_number = random.randint(1000, 9999)
            collection.update_one({"name": guser}, {"$set": {"code": random_number}})
            collection.update_one({"name": username}, {"$set": {"code": random_number}})   
     return redirect(url_for('chat'))





@app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == 'GET':
        username = session.get('username')
        if username:
            current_user = collection.find_one({'name': username}, {'location': 1, '_id': 0})
            if current_user and 'location' in current_user:
                current_location = current_user['location']
                lat1, lon1 = current_location['latitude'], current_location['longitude']
                results = collection.find({'location': {'$exists': True},'nexuser':username}, {"name": 1, "location": 1, "_id": 0})
                options = []
                for item in results:
                    if item['name'] != username and 'location' in item:
                        lat2, lon2 = item['location']['latitude'], item['location']['longitude']
                        distance = haversine(lat1, lon1, lat2, lon2)
                        if distance <= 100:
                            options.append(item["name"])
                
                return render_template('find.html', options=options)
    return redirect(url_for('login'))


@app.route('/select', methods=['POST'])
def select():
    guser = request.form['options']
    username = session.get('username')
    if username:
        random_number = random.randint(1000, 9999)
        collection.update_one({"name": username}, {"$set": {"code": random_number}})
        collection.update_one({"name": guser}, {"$set": {"code": random_number}})
        query = {'nexuser': username}
        results = collection.find(query)
        options = [item["name"] for item in results]
        return render_template('index.html', options=options, username=username)
    return redirect(url_for('login'))

@app.route('/view_request', methods=['GET', 'POST'])
def view_request():
    if request.method == 'POST':
        guser = request.form['options']
        username = session.get('username')
        if username:
            filter = {"name": username}
            update = {"$set": {"nexuser": guser}}
            collection.update_one(filter, update)
    
    # Fetch the updated options
    username = session.get('username')
    query={'name':username}
    result=collection.find(query,{"code":1,"id":0})
    # query={'code':result}
    # ee=collection.find(query,{"n":1,"id":0})
    query={'name':{'$ne':username},'code':result}
    un=collection.find(query,{"name":1,"id":0})
    # if un:
    #     return render_template('view_request.html', options=options,show=True)
    query2 = {'price': {'$ne': 0}}
    results = collection.find(query2, {"name": 1, "_id": 0})
    options = [item["name"] for item in results]
    if un:
        return render_template('view_request.html', options=options,show=True)
    return render_template('view_request.html', options=options,show=False)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    username = session.get('username')
    
    if not username:
        return redirect(url_for('login'))
    
    # Find the user's code
    user = collection.find_one({'name': username}, {'code': 1, '_id': 0})
    
    if not user:
        flash('User not found')
        return redirect(url_for('login'))
    
    user_code = user['code']
    
    # Find all users with the same code, excluding the current user
    other_users = list(collection.find({'name': {'$ne': username}, 'code': user_code}, {'name': 1, 'text': 1, '_id': 0}))
    
    # Extract the names and text messages
    dynamic_texts = [{'name': user['name'], 'text': user['text']} for user in other_users]
    
    # Debugging: Print the dynamic texts
    #print("Dynamic Texts:", dynamic_texts)
    
    if request.method == 'POST':
        if username:
            dtext = request.form['user_text']
            filter = {"name": username}
            update = {"$set": {"text": dtext}}
            collection.update_one(filter, update)
            
            # Reload dynamic texts after update
            other_users = list(collection.find({'name': {'$ne': username}, 'code': user_code}, {'name': 1, 'text': 1, '_id': 0}))
            dynamic_texts = [{'name': user['name'], 'text': user['text']} for user in other_users]
            
            # Debugging: Print the updated dynamic texts
            #print("Updated Dynamic Texts:", dynamic_texts)
    
    return render_template('chat.html', dynamic_texts=dynamic_texts)


@app.route('/share_location', methods=['GET', 'POST'])
def share_location():
    if request.method == 'POST':
        lat = request.form['latitude']
        lng = request.form['longitude']
        username = session.get('username')
        
        if username:
            collection.update_one(
                {'name': username},
                {'$set': {'location': {'latitude': lat, 'longitude': lng}}}
            )
            flash('Location shared successfully!')
        return redirect(url_for('chat'))
    
    return render_template('share_location.html')

@app.route('/view_location')
def view_location():
    sname = session.get('username')
    user_code = collection.find_one({'name': sname}, {'code': 1, '_id': 0})
    if user_code:
        code_value = user_code['code']
        other_users = collection.find({'name': {'$ne': sname}, 'code': code_value}, {'name': 1, 'location': 1, '_id': 0})
        users = [{'name': user['name'], 'location': user['location']} for user in other_users if 'location' in user]
        if users:
            return render_template('view_location.html', users=users)
    return render_template('view_location.html')



if __name__ == '__main__':
    app.run(debug=True)
