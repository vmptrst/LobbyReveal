import sys
import requests
import json
import platform
import psutil
import base64
from time import sleep
from os import system, name
from urllib3 import disable_warnings


disable_warnings()


app_port = None
auth_token = None
riotclient_auth_token = None
riotclient_app_port = None
region = None
lcu_name = None
showNotInChampSelect = True


def getLCUName():
    global lcu_name
    if platform.system() == "Windows":
        lcu_name = "LeagueClientUx.exe"
    elif platform.system() == "Darwin":
        lcu_name = "LeagueClientUx"
    elif platform.system() == "Linux":
        lcu_name = "LeagueClientUx"


def LCUExists():
    return lcu_name in (p.name() for p in psutil.process_iter())


def getLCUInfo():
    global auth_token, app_port, region, riotclient_auth_token, riotclient_app_port

    if not LCUExists():
        sys.exit('No ' + lcu_name + ' process found. Please open the client and try again.')
        sys.sleep(3)
    
    for proc in psutil.process_iter():
        if proc.name() == lcu_name:
            args = proc.cmdline()

            for a in args:
                if '--region=' in a:
                    region = a.split('--region=', 1)[1].lower()
                if '--remoting-auth-token=' in a:
                    auth_token = a.split('--remoting-auth-token=', 1)[1]
                if '--app-port' in a:
                    app_port = a.split('--app-port=', 1)[1]
                if '--riotclient-auth-token=' in a:
                    riotclient_auth_token = a.split('--riotclient-auth-token=', 1)[1]
                if '--riotclient-app-port=' in a:
                    riotclient_app_port = a.split('--riotclient-app-port=', 1)[1]


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def main():
    global showNotInChampSelect

    sys.argv[0] = "LobbyReveal - Scary"

    getLCUName()
    getLCUInfo()

    lcu_api = 'https://127.0.0.1:' + app_port
    riotclient_api = 'https://127.0.0.1:' + riotclient_app_port

    lcu_session_token = base64.b64encode(
        ('riot:' + auth_token).encode('ascii')).decode('ascii')

    riotclient_session_token = base64.b64encode(
        ('riot:' + riotclient_auth_token).encode('ascii')).decode('ascii')

    lcu_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic ' + lcu_session_token
    }

    riotclient_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'LeagueOfLegendsClient',
        'Authorization': 'Basic ' + riotclient_session_token
    }


    current_summoner = lcu_api + '/lol-summoner/v1/current-summoner'

    r = requests.get(current_summoner, headers=lcu_headers, verify=False)
    r = json.loads(r.text)

    print('Connected ' + r['displayName'])

    try:
        checkForLobby = True

        while True:
            get_champ_select = lcu_api + '/lol-champ-select/v1/session'

            r = requests.get(get_champ_select, headers=lcu_headers, verify=False)
            r = json.loads(r.text)

            if 'errorCode' in r:
                checkForLobby = True
                if showNotInChampSelect:
                    clear()
                    print("Couldn't find champ select. Waiting for lobby..")
                    showNotInChampSelect = False
            else:
                if checkForLobby:
                    clear()
                    print('\n* Found lobby *\n')

                    get_lobby = riotclient_api + '/chat/v5/participants/champ-select'

                    r = requests.get(get_lobby, headers=riotclient_headers, verify=False)
                    r = json.loads(r.text)

                    for x in r['participants']:
                        print(x['game_name'] + ' joined the lobby')
                    
                    print ('\n')

                    showNotInChampSelect = True
                    checkForLobby = False
            sleep(2)
    except KeyboardInterrupt:
        print('\n\n* Exiting..')
        sys.exit(0)


if __name__ == '__main__':
    main()