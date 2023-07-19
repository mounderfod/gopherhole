import os

from dotenv import load_dotenv
from pituophis import Item, serve
from pyfiglet import Figlet

import news
import sports
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
        menu.append(Item(itype="1", text="......SPORTS", path="/sports", host=os.getenv("HOSTNAME")))
        return menu
    elif request.path.startswith("/newstxt"):
        return news.get_newstxt(request.path.split("?article=")[1])
    elif request.path.startswith("/weathertxt"):
        return weather.get_weather(request.path)
    elif request.path == "/news" or request.path == "/weather" or request.path == "/sports":
        menu = []
        text = figlet.renderText(request.path[1:]).split("\n")
        menu += [Item(text=i) for i in text]
        match request.path:
            case "/news":
                menu.append(Item(text="=== Provided by The Guardian ==="))
                menu += news.get_news()
            case "/weather":
                menu += weather.get_cities(request.query)
            case "/sports":
                menu += [
                    menu.append(Item(itype="0", text="FORMULA 1", path="/sports/f1", host=os.getenv("HOSTNAME")))
                ]
        return menu
    elif request.path.startswith("/sports/"):
        match request.path:
            case "/sports/f1":
                return sports.get_f1()
    else:
        return [Item(itype="3", text="Page not found")]


serve(port=70, handler=handle, pub_dir="personal")
