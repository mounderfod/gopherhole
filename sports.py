import requests
from prettytable import PrettyTable
from pyfiglet import Figlet
from unidecode import unidecode

def get_f1():
    result = []
    f = Figlet(font="big")
    result += f.renderText("formula 1").split("\n")

    result.append("=" * 80)
    result.append("Last Race".center(80))
    result.append("=" * 80)

    lastRace = requests.get("http://ergast.com/api/f1/current/last/results.json").json()['MRData']['RaceTable']['Races'][0]
    result.append(f"Round {lastRace['round']}: {lastRace['raceName']}")
    result.append(f"Took place @ {lastRace['Circuit']['circuitName']} on {lastRace['date']}")

    result.append("\n\n")

    results = PrettyTable()
    results.field_names = ['Position', 'Driver', 'Constructor', 'Time']

    for i in lastRace['Results']:
        if i['status'] != "Finished":
            results.add_row([
                i['positionText'],
                unidecode(i['Driver']['givenName']) + " " + unidecode(i['Driver']['familyName']),
                i['Constructor']['name'],
                f"DNF lap {i['laps']} ({i['status']})"
            ])
        else:
            results.add_row([
                i['positionText'],
                unidecode(i['Driver']['givenName']) + " " + unidecode(i['Driver']['familyName']),
                i['Constructor']['name'],
                i['Time']['time']
            ])

    result.append(results.get_string())
    result.append("\n\n")

    result.append("=" * 80)
    result.append("Next Race".center(80))
    result.append("=" * 80)

    nextRace = requests.get("http://ergast.com/api/f1/current/next.json").json()['MRData']['RaceTable']['Races'][0]
    result.append(f"Round {nextRace['round']}: {nextRace['raceName']}")
    result.append(f"Taking place @ {nextRace['Circuit']['circuitName']}")
    result.append(f"P1: {nextRace['FirstPractice']['date']} @ {nextRace['FirstPractice']['time'][:5]}")
    result.append(f"P2: {nextRace['SecondPractice']['date']} @ {nextRace['SecondPractice']['time'][:5]}")
    result.append(f"P2: {nextRace['ThirdPractice']['date']} @ {nextRace['ThirdPractice']['time'][:5]}")
    result.append(f"Qualifying: {nextRace['Qualifying']['date']} @ {nextRace['Qualifying']['time'][:5]}")
    result.append(f"Final Race: {nextRace['date']} @ {nextRace['time'][:4]}")

    result.append("\n\n")

    result.append("=" * 80)
    result.append("Driver Standings".center(80))
    result.append("=" * 80)

    driverStandings = requests.get("http://ergast.com/api/f1/current/driverStandings.json").json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    dsTable = PrettyTable()
    dsTable.field_names = ["Position", "Driver", "Constructor", "Points", "Wins"]
    for i in driverStandings:
        dsTable.add_row([
            i['positionText'],
            f"{unidecode(i['Driver']['givenName'])} {unidecode(i['Driver']['familyName'])} ({i['Driver']['nationality']})",
            i['Constructors'][0]['name'],
            i['points'],
            i['wins']
        ])
    result.append(dsTable.get_string())
    result.append("\n\n")

    result.append("=" * 80)
    result.append("Constructor Standings".center(80))
    result.append("=" * 80)

    constructorStandings = requests.get("http://ergast.com/api/f1/current/constructorStandings.json").json()['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    csTable = PrettyTable()
    csTable.field_names = ["Position", "Constructor", "Points", "Wins"]
    for i in constructorStandings:
        csTable.add_row([
            i['positionText'],
            i['Constructor']['name'],
            i['points'],
            i['wins']
        ])
    result.append(csTable.get_string())

    return result