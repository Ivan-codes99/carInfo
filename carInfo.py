#Reddit bot that gives information on a specific car
import praw

#creating reddit instance
def login(client_id, client_secret, username, password, user_agent):
    reddit = praw.Reddit(client_id = client_id,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = user_agent)
    print(reddit.user.me())
    return reddit

def run_bot(r):
    subreddit = r.subreddit('test')  # Retrieve the subreddit object
    for comment in subreddit.stream.comments():
        for item in car_models:
            if item in comment.body:
                comment.reply("Beep boop: Car model: " + item + " found in comment.") #need to fix this so that it does not reply to itself infinitely

#Creating a set of car models, short set for testing purposes right now
car_models = {"camry", "corolla", "civic", "brz", "86", "supra", "m3", "accord"}

#initializing
id = ""
secret = ""
usrname = ""
passwd = ""
agent = ""

reddit = login(id, secret, usrname, passwd, agent)
run_bot(reddit)







