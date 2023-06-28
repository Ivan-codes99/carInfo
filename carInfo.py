#Reddit bot that gives information on a specific car
import praw

#initializing
client_id = ""
client_secret = ""
username = ""
password = ""
user_agent = ""

#Creating a set of car models, short set for testing purposes right now
car_models = {"camry", "corolla", "civic", "brz", "86", "supra", "m3", "accord"}

#creating reddit instance
def login():
    reddit = praw.Reddit(client_id = client_id,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = user_agent)
    return reddit

def run_bot(r):
    subreddit = r.subreddit('test')  # Retrieve the subreddit object
    for comment in subreddit.stream.comments():
        for item in car_models:
            if item in comment.body:
                print("Car model: " + item + " found in comment.")

reddit = login()
run_bot(reddit)





