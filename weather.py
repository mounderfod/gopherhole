import urllib.parse
import os
import requests
from pituophis import Item
from dotenv import load_dotenv
from prettytable import PrettyTable
from pyfiglet import Figlet

load_dotenv()


def get_code(code):
    match code:
        case 0:
            return "Clear sky"
        case 1 | 2 | 3:
            return "Partly cloudy"
        case 45 | 48:
            return "Foggy"
        case 51 | 53 | 55:
            return "Drizzle"
        case 56 | 57:
            return "Freezing drizzle"
        case 61 | 63 | 65:
            return "Rain"
        case 66 | 67:
            return "Freezing rain"
        case 71 | 73 | 675:
            return "Snow"
        case 77:
            return "Snow grains"
        case 80 | 81 | 82:
            return "Rain showers"
        case 85 | 86:
            return "Snow showers"
        case 95:
            return "Thunderstorm"
        case 96 | 99:
            return "Thunderstorm with hail"
        case _:
            return "Unknown"


def get_cities(query):
    data = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=10&language=en&format=json").json()
    if "results" in data:
        return [Item(
            itype="0",
            text=f"{i['name']} ({i['admin1'] + ', ' if 'admin1' in i else ''}{i['country']})",
            path=f"/weathertxt?latlong={str(i['latitude'])}@{str(i['longitude'])}&city={i['name']}",
            host=os.getenv("HOSTNAME")
        ) for i in data['results']]
    else:
        return [Item(itype="3", text="City could not be found")]


def get_weather(city):
    result = []
    query = city.split("?latlong=")[1]
    latitude = query.split("&city=")[0].split("@")[0]
    longitude = query.split("&city=")[0].split("@")[1]
    place = query.split("&city=")[1]

    print(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly"
                        f"=temperature_2m,relativehumidity_2m,precipitation_probability,"
                        f"weathercode,windspeed_10m&daily=weathercode,"
                        f"temperature_2m_max,temperature_2m_min,sunrise,"
                        f"sunset&current_weather=true&timezone=auto")

    data = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly"
                        f"=temperature_2m,relativehumidity_2m,precipitation_probability,"
                        f"weathercode,windspeed_10m&daily=weathercode,"
                        f"temperature_2m_max,temperature_2m_min,sunrise,"
                        f"sunset&current_weather=true&timezone=auto").json()

    f = Figlet(font="big")
    result += f.renderText("weather").split("\n")
    f.setFont(font="small")

    result.append("="*80)
    result.append(f"{place}".center(80))
    result.append("="*80)

    result += f.renderText("hourly").split("\n")
    table_hourly = PrettyTable()
    table_hourly.field_names = ["Time", "Summary", "Temperature", "Humidity", "Precipitation Chance", "Wind Speed"]
    for idx, i in enumerate(data['hourly']['time'][:23]):
        table_hourly.add_row([
            i[-5:],
            get_code(data['hourly']['weathercode'][idx]),
            f"{data['hourly']['temperature_2m'][idx]} C",
            f"{data['hourly']['relativehumidity_2m'][idx]} %",
            f"{data['hourly']['precipitation_probability'][idx]} %",
            f"{data['hourly']['windspeed_10m'][idx]} km/h",
        ])
    result.append(table_hourly.get_string())
    result += ["\n"] * 3

    result += f.renderText("daily").split("\n")
    table_daily = PrettyTable()
    table_daily.field_names = ["Date", "Summary", "Temperature (Max/Min)", "Sunrise / Sunset"]
    for idx, i in enumerate(data['daily']['time']):
        table_daily.add_row([
            i,
            get_code(data['daily']['weathercode'][idx]),
            f"{data['daily']['temperature_2m_max'][idx]} C / {data['daily']['temperature_2m_min'][idx]} C",
            f"{data['daily']['sunrise'][idx][-5:]} / {data['daily']['sunset'][idx][-5:]}"
        ])
    result.append(table_daily.get_string())

    return result
