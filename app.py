import os
from os import listdir
from os.path import isfile, join
from dotenv import load_dotenv
from pituophis import Item, serve
from pyfiglet import Figlet
import news
import weather

load_dotenv()
figlet = Figlet(font="big")


def handle(request):
    if request.path == "" or request.path == "/":
        menu = []
        with open("static/ascii/cat.txt", "r") as f:
            menu += [Item(text=i) for i in f.readlines()]

        menu.append(Item(itype="1", text="......NEWS", path="/news", host=os.getenv("HOSTNAME")))
        menu.append(
            Item(itype="7", text="......WEATHER (type in city name)", path="/weather", host=os.getenv("HOSTNAME")))
        menu.append(Item(itype="1", text="......OWNER'S SITE", path="/personal", host=os.getenv("HOSTNAME")))
        return menu
    elif request.path.startswith("/newstxt"):
        return news.get_newstxt(request.path.split("?article=")[1])
    elif request.path.startswith("/weathertxt"):
        return weather.get_weather(request.path)
    elif request.path == "/personal":
        with open("personal/gophermap", "r") as f:
            return [i for i in f.readlines()]
    elif request.path == "/news" or request.path == "/weather":
        menu = []
        text = figlet.renderText(request.path[1:]).split("\n")
        menu += [Item(text=i) for i in text]
        match request.path:
            case "/news":
                menu.append(Item(text="=== Provided by The Guardian ==="))
                menu += news.get_news()
            case "/weather":
                menu += weather.get_cities(request.query)
        return menu
    else:
        return [Item(itype="3", text="Page not found")]


serve(port=70, handler=handle)
