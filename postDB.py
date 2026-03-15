import requests
import time

DATABASE_URL = "https://buddyup-f2a80-default-rtdb.firebaseio.com/"
""""
This function will create any user posts, this is the first version I will work to update so that it tracks the exact user who posts.
So far it can track the user, the content posted, the time it was posted and the likes.
"""
def create_post(user_email, content):
    url = f"{DATABASE_URL}/posts.json"
    data ={
        "user":user_email,
        "content":content,
        "timeposted":int(time.time()),
        "likes": 0
    }

    response = requests.post(url, json=data)
    return response.json()

def get_posts():
    url =f"{DATABASE_URL}/posts.json"
    response = requests.get(url)
    return response.json()
    
def update_likes(post_id, new_likes):
        url = f"{DATABASE_URL}/posts/{post_id}.json"
        data = {"likes": new_likes}
        requests.patch(url, json=data)