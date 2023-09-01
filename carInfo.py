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
    list_subreddit = ["carporn", "Autos", "MechanicAdvice", "projectcar", "justrolledintotheshop", "Cartalk","whatisthiscar", "idiotsincars", "spotted"]
    for element in list_subreddit:
        subreddit = r.subreddit(element)  # Retrieve the subreddit object
        word_split_regex = re.compile(r'\W+|\d+')
        for comment in subreddit.comments(limit = 10):
            lst_str_comment = word_split_regex.split(comment.body.lower())
            # print("lst_str_comment is ")
            # print(lst_str_comment)
            for word in lst_str_comment: 
                if word == "is" or word == "Is" or word == "iS":
                    continue
                if word.lower() in [model.lower() for model in car_models] and (comment.id not in comments_replied_to) and (comment.author != r.user.me()): #conditionals check for comment author and previously replied to comments
                    model_trims = fetchTrims(word)
                    
                    str_model_trims = ', '.join(str(element) for element in model_trims)
                    model_ext_colors = fetchExColors(word)
                    str_model_ext_colors = ', '.join(str(element) for element in model_ext_colors)
                    model_int_colors = fetchInColors(word)
                    str_model_int_colors = ", ".join(str(element) for element in model_int_colors)
                    model_body_types = fetchBodyTypes(word)
                    str_model_body_types = ", ".join(str(element) for element in model_body_types)
                    
                    print("Beep boop: Car model: " + word + " found in comment." + "\n" + "Availabe trims: " + str_model_trims)
                    comment.reply("Beep boop: Car model: " +"\"" + word + "\"" + " found in comment." + 
                                "\n\n" + "Availabe trims: " + str_model_trims + 
                                ".\n\n sample available exterior colors: " + str_model_ext_colors + "." +
                                "\n\n sample available interior colors: " + str_model_int_colors + 
                                ".\n\n" + "Available body types: " + str_model_body_types + "." + 
                                "\n\n This data is for 2020 year.")
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


def fetchCarModels(year = "year=2020"):
    api_url = "https://carapi.app/api/models?year=2020"
    currpage = 1
    headers = {
        'accept': 'application/json',
        'Authorization' : f'Bearer {jwt_token}'
    }
    search_params = {
        "year": 2020
    }

    while api_url:
        
        response = requests.get(api_url, params = search_params, headers=headers)
        print("Status code:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            car_models.extend(item["name"] for item in data["data"])
            if "next" in data["collection"] != "":
                currpage +=1
                api_url = "https://carapi.app" + "/api/models?page=" + str(currpage) + "&" + year
            else:
                api_url = None
        else:
            break
        

def fetchTrims(model, year="year=2020"):
    model = model.capitalize()
    set_trims = set()
    api_url = "https://carapi.app/api/trims?" + year + "&model=" + model
    headers = {
        'accept': 'application/json',
        'Authorization' : f'Bearer {jwt_token}'
    }

    search_params = {
        "year": 2020
    }
    currpage = 1
    while api_url:
        response = requests.get(api_url, params = search_params, headers=headers)
        print("Status code:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            for item in data["data"]:
                set_trims.add(item["name"])
            break
        if "next" in data["collection"] != "":
            currpage +=1
            api_url = "https://carapi.app/api/trims?page=" + str(currpage) + "&" + year  + "&model=" + model
        else:
            break
        
    lst_trims = list(set_trims)    
    return lst_trims[:10]

def fetchExColors(model, year="year=2020"):
    set_exterior_colors = set()
    api_url = "https://carapi.app/api/exterior-colors?year=2020&model=" + model
    headers = {
        'accept': 'application/json',
        'Authorization' : f'Bearer {jwt_token}'
    }

    search_params = {
        "year": 2020
    }
    currpage = 1
    while api_url:
        response = requests.get(api_url, params = search_params, headers=headers)
        print("Status code:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            for item in data["data"]:
                set_exterior_colors.add(item["name"])
            if "next" in data["collection"] != "":
                currpage +=1
                api_url = "https://carapi.app/api/exterior-colors?page=" + str(currpage) + "&" + year  + "&model=" + model
            else:
                api_url = None
        else:
            break
    lst_exterior_colors = list(set_exterior_colors)
    return lst_exterior_colors[:5]

def fetchInColors(model, year="year=2020"):
    set_interior_colors = set()
    api_url = "https://carapi.app/api/interior-colors?year=2020&model=" + model
    headers = {
        'accept': 'application/json',
        'Authorization' : f'Bearer {jwt_token}'
    }

    search_params = {
        "year": 2020
    }
    currpage = 1
    while api_url:
        response = requests.get(api_url, params = search_params, headers=headers)
        print("Status code:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            for item in data["data"]:
                set_interior_colors.add(item["name"])
            if "next" in data["collection"] != "":
                currpage +=1
                api_url = "https://carapi.app/api/exterior-colors?page=" + str(currpage) + "&" + year  + "&model=" + model
            else:
                api_url = None
                break
        else:
            print("API request failed. Status code:", response.status_code)
            break
    lst_interior_colors = list(set_interior_colors)
    return lst_interior_colors[:5]

def fetchBodyTypes(model, year = "2020"):
    set_body_types = set()
    api_url = "https://carapi.app/api/bodies?year=2020&model=" + model
    headers = {
        'accept': 'application/json',
        'Authorization' : f'Bearer {jwt_token}'
    }

    search_params = {
        "year": 2020
    }
    currpage = 1
    while api_url:
        response = requests.get(api_url, params = search_params, headers=headers)
        print("Status code:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            for item in data["data"]:
                set_body_types.add(item["type"])
            if "next" in data["collection"] != "":
                currpage +=1
                api_url = "https://carapi.app/api/bodies?page=" + str(currpage) + "&" + year  + "&model=" + model
            else:
                api_url = None
                break
        else:
            break
    lst_body_types = list(set_body_types)
    return lst_body_types[:10]
    
    
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
run_bot(reddit, comments_replied_to)









