import requests # type: ignore
#API key to connect project with firebase
API_KEY = "AIzaSyBNKnNFXQpTr-B8Cty-mmYIBsKL9p3TFNA"
#Function for user sign up
def signUp(email, password):
        url= f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
        data = {
              "email": email,
              "password": password,
              "returnSecureToken": True
              
        }
        response = requests.post(url, json=data)
        return response.json()
#Function for user log in
def login_user(email, password):
    url= f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    data = {
        "email":email,
        "password":password,
        "returnSecureToken":True
    }


    response = requests.post(url, json=data)
    return response.json()