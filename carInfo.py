#Reddit bot that gives information on a specific car
import praw
import os

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

#Creating a set of car models, short set for testing purposes right now
car_models = {"camry", "corolla", "civic", "brz", "86", "supra", "m3", "accord"}

#initializing
id = ""
secret = ""
usrname = ""
passwd = ""
agent = ""



reddit = login(id, secret, usrname, passwd, agent)
comments_replied_to = get_saved_comments()
while True:
    run_bot(reddit, comments_replied_to)







