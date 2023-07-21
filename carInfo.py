#Reddit bot that gives information on a specific car
import praw
import os
import requests
import re

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
    word_split_regex = re.compile(r'\W+|\d+')
    for comment in subreddit.comments(limit=10):
        lst_str_comment = word_split_regex.split(comment.body.lower())
        # print("lst_str_comment is ")
        # print(lst_str_comment)
        for word in lst_str_comment:
            if word in [model.lower() for model in car_models] and (comment.id not in comments_replied_to) and (comment.author != r.user.me()): #conditionals check for comment author and previously replied to comments
                print("Beep boop: Car model " + word + " is found in comment.")
                comment.reply("Beep boop: Car model: " + word + " found in comment.")
                comments_replied_to.append(comment.id)

                with open("savedComments.txt", "a") as pc:
                    pc.write(comment.id + "\n")
    
def get_saved_comments():
    if not os.path.isfile("savedComments.txt"):
        comments_replied_to = []
    else:
        with open("savedComments.txt", "r") as pc:
            comments_replied_to = pc.read()
            comments_replied_to = comments_replied_to.split("\n")
    
    return comments_replied_to

def Authorize():
    login_url = "https://carapi.app/api/auth/login"
    login_data = {
        "api_token": api_token,
        "api_secret": api_secret
    }

    response = requests.post(login_url, json = login_data)
    if response.status_code == 200:
         global jwt_token
         jwt_token = response.text.strip()
         print("JWT Token:", jwt_token)
    else:
        print("Authentication failed. Status code:", response.status_code)


def fetchCarModels():
    api_url = "https://carapi.app/api/models?year=2020"
    year = "year=2020"
    currpage = 1
    headers = {
        'accept': 'application/json',
        'Authorization' : f'Bearer {jwt_token}'
    }
    search_params = {
        "year": 2020,
    }

    while api_url:
        response = requests.get(api_url, params = search_params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            car_models.extend(item["name"] for item in data["data"])

            if "next" in data["collection"] != "":
                currpage +=1
                api_url = "https://carapi.app" + "/api/models?page=" + str(currpage) + "&" + year
            else:
                api_url = None
        else:
            print("API request failed. Status code:", response.status_code)
            break
            
    
#initializing
usrname = ""
passwd = ""
agent = ""
id = ""
secret = ""

reddit = login(id, secret, usrname, passwd, agent)
comments_replied_to = get_saved_comments()

car_models = []
api_token = ""
api_secret = ""
jwt_token = ""

Authorize()
fetchCarModels()
i=1
while i <=10 :
    run_bot(reddit, comments_replied_to)
    i+=1









