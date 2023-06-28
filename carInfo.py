#Reddit bot that gives information on a specific car
import praw

#initializing
client_id = ""
client_secret = ""
username = ""
password = ""
user_agent = ""

#creating reddit instance
reddit = praw.reddit(client_id = client_id,
                     client_secret = client_secret,
                     username = username,
                     password = password,
                     user_agent = user_agent)
