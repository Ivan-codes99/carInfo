#Reddit bot that gives information on a specific car
import praw
import os
import requests
import json

#creating reddit instance
def login(client_id, client_secret, username, password, user_agent):
    reddit = praw.Reddit(client_id = client_id,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = user_agent)
    return reddit

def run_bot(r, comments_replied_to):
    subreddit = r.subreddit('test')  # Retrieve the subreddit object
    
    for comment in subreddit.comments(limit=10):
        for item in car_models:
            if item in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me(): #conditionals check for comment author and previously replied to comments
                comment.reply("Beep boop: Car model: " + item + " found in comment.")
                print("Beep boop: Car model: " + item + " found in comment.")
                comments_replied_to.append(comment.id)

                with open("savedComments.txt", "a") as pc:
                    pc.write(comment.id + "\n")
    
def get_saved_comments():
    if not os.path.isfile("savedComments.txt"):
        comments_replied_to = []
    else:
        with open("savedComments.txt", "r") as pc:
            comments_replied_to = pc.read()
            comments_replied_to = comments_replied_to.split("/n")

    return comments_replied_to

def requesting():
    api_token = ""
    api_secret = ""

    login_url = "https://carapi.app/api/auth/login"
    login_data = {
        "api_token": api_token,
        "api_secret": api_secret
    }

    response = requests.post(login_url, json = login_data)
    if response.status_code == 200:
        jwt_token = response.text.strip()
        print("JWT Token:", jwt_token)
    else:
        print("Authentication failed. Status code:", response.status_code)

    api_url = "https://carapi.app/api/models"
    headers = {
        'accept': 'application/json',
        'Authorization' : f'Bearer {jwt_token}'
    }

    search_criteria = {
    "year": 2020,
    "make": "ford"
}

    response = requests.get(api_url, params = search_criteria, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("API request failed. Status code:", response.status_code)



#Creating a set of car models, short set for testing purposes right now
car_models = {"camry", "corolla", "civic", "brz", "86", "supra", "m3", "accord"}

#initializing
id = ""
secret = ""
usrname = ""
passwd = ""

agent = "my car app"


reddit = login(id, secret, usrname, passwd, agent)
comments_replied_to = get_saved_comments()
# while True:
#     run_bot(reddit, comments_replied_to)
requesting()







