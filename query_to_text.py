import wikipedia
import requests
from bs4 import BeautifulSoup
import praw
import re

import warnings
warnings.filterwarnings("ignore")

soupify = lambda link: BeautifulSoup(requests.get(link).text, 'html.parser')

def decompose(soup, sections):
        #for example, sections = [("div",  {"id": "vdo_ai_div"})]
        #decomposes the irrelevent html elements
        for section in sections:
            print("section: ", section, "\n\n")
            for s in soup.find_all(section):
                s.decompose()
        return soup




def query_to_text(query = False):
    #interects with user and reports final text to be summarized

    if not query:
        query = input("What do you want to tl;dr today? : ")
    
    text = ""
    try:
        host = (query.split("/")[2]).split(".")[-2]
    except:

        try:
            text = wikipedia.summary(query)
        except wikipedia.exceptions.DisambiguationError as e:
            print("I didn't get you. Pick one to tl;dr.")
            print(e.options)
            query = input("I want to tl;dr : ")
            return query_to_text(query)
        except wikipedia.exceptions.PageError:
            print("I totally lost you. Don't troll me again! :-)")
            return query_to_text()

        return re.sub('\n+', ' ', text)


    
    if host == "reddit":
        reddit = praw.Reddit(
            client_id="",
            client_secret="",
            user_agent="python:none:v0.0.1 (by u/vijaykes)")
        r = praw.models.Submission(reddit, url=query)
        text = r.selftext

    elif host == "theprint":
        soup = soupify(query)
        soup = soup.find("div", {"class": "td-post-content"})

        soup = decompose(soup, (
            ("div",  {"id": "vdo_ai_div"}),
            ("div",  {"class": "code-block"}),
            # ("p", {"class": "postBtm"}),
            ("button"),
            ("div", {"class": "td-post-featured-image"}),
            ("div", {"class": "fontsize_Btn"}),
            ("a", {"title": re.compile("")})
        ))

        text = soup.get_text()
    
    
    elif host == "wikipedia":
        text =  wikipedia.summary(query.split("/")[-1])  
    
    return re.sub('\n+', ' ', text)