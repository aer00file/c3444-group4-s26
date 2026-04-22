import requests
import time

DATABASE_URL = "https://buddyup-f2a80-default-rtdb.firebaseio.com/"
""""
This function will create any user posts, this is the first version I will work to update so that it tracks the exact user who posts.
So far it can track the user, the content posted, the time it was posted and the likes.
"""

def create_post(user_email, content, tags):
    url = f"{DATABASE_URL}/posts.json"
    data ={
        "user":user_email,
        "content":content,
        "timeposted":int(time.time()),
        "likes": 0,
        "tags": tags
    }

    response = requests.post(url, json=data)
    return response.json()

def delete_post(post_id):
    url = f"{DATABASE_URL}/posts/{post_id}.json"
    response = requests.delete(url)
    return response

def get_posts():
    url =f"{DATABASE_URL}/posts.json"
    response = requests.get(url)
    return response.json()
    
def update_likes(post_id, new_likes):
        url = f"{DATABASE_URL}/posts/{post_id}.json"
        data = {"likes": new_likes}
        requests.patch(url, json=data)

def add_comment(post_id, user, text):
    url = f"{DATABASE_URL}/comments/{post_id}.json"
    data = {
        "user": user,
        "content": text,
        "timeposted": int(time.time()),
        "likes": 0
    }
    return requests.post(url, json=data)

def get_comments(post_id):
    url = f"{DATABASE_URL}/comments/{post_id}.json"
    response = requests.get(url)
    return response.json()

def createUserProfile(userUID, email):
    url = f"{DATABASE_URL}/users/{userUID}.json"
    data = {
        "email": email,
        "bio": ""
    }
    response = requests.put(url, json=data)
    return response.json()

def getProfile(userUID):
    url = f"{DATABASE_URL}/users/{userUID}.json"

    response = requests.get(url)
    return response.json()

def updateBio(userUID, new_bio):
    url = f"{DATABASE_URL}/users/{userUID}.json"
    data = {"bio": new_bio}
    response = requests.patch(url, json=data)
    return response.json()
