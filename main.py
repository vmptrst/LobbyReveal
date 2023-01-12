import os as o
import requests as r
import psutil as u
import json as j
import base64 as b

# ------------------------------------------------------- #


def ranked_name_exploit():
    [x]=[[i.cmdline()[2].split('=')[1],i.cmdline()[1].split('=')[1]] for i in u.process_iter() if i.name() == 'LeagueClient.exe']
    e=list(r.get(url=f'https://127.0.0.1:{x[0]}/chat/v5/participants/champ-select',headers={'Authorization':f"Basic {b.b64encode(f'riot:{x[1]}'.encode()).decode()}",'Accept': 'application/json'},verify=r"{}\riotgames.pem".format(o.getcwd())))
    return [ i['name'] for i in j.loads(''.join(s.decode() for s in e))['participants']]


def check_region() -> str:
    print("Region: ", "?")
    region = input("Region: ").lower()
    region = region.replace("Region: ", "")
    return region

# ------------------------------------------------------- #


def main() -> None:
    region = check_region()
    while True:
        print("Type `pull` to pull the names from your lobby.")
        pull = input("> ")
        pull = pull.replace("> ", "")
        if pull == "pull":
            print(ranked_name_exploit())
        else:
            if pull != "exit":
                print("Invalid command")
            else:
                break


if __name__ == "__main__":
    main()
