import os
import urllib.parse
import html2text
import requests
from dotenv import load_dotenv
from pituophis import Item

load_dotenv()

def get_news():
    results = []
    data = requests.get(f"https://content.guardianapis.com/search?api-key={os.getenv('GUARDIAN_API')}&page-size=50").json()
    results += [Item(
        itype="0",
        text=i['webTitle'],
        path=f"/newstxt?article={urllib.parse.quote(i['id'], safe='')}",
        host=os.getenv("HOSTNAME")
    ) for i in data['response']['results']]
    return results


def get_newstxt(article):
    path = urllib.parse.unquote(article)
    data = requests.get(f"https://content.guardianapis.com/{path}?api-key={os.getenv('GUARDIAN_API')}&show-fields=body").json()
    h = html2text.HTML2Text()
    h.use_automatic_links = True
    h.images_to_alt = True
    h.ignore_tables = True
    h.ignore_links = True
    h.emphasis_mark = ""
    h.strong_mark = ""
    text = f"{data['response']['content']['webTitle']}\n" + ("=" * 60) + "\n"
    text += h.handle(data['response']['content']['fields']['body'])
    return text