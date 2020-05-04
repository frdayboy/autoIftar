#!/usr/bin/env python
import os
import json
import time

runforever = False

def config():
    while True:
        runforeverprompt = raw_input("[autoIftar] Would you like to have this tool run forever until stopped?(yes or no): ")
        if runforeverprompt == "yes":
            runforever = True
            break
        elif runforeverprompt == "no":
            break
        else:
            print("[autoIftar] Wrong input")
    try:
        with open("./config.json", "r") as f:
            global city, country
            config = json.loads(str(f.read()))
            city = config["city"]
            country = config["country"]
            f.close()
    #No config file, probably first use of tool
    except IOError:
        with open("./config.json", "w+") as f:
            print("[autoIftar] No configuration file found. This seems to be your first time using this tool.")
            city = raw_input("[autoIftar] Please enter your city (Spaces and Capitalizations Included): ")
            country = raw_input("[autoIftar] Please enter your country (Spaces and Capitalizations Included): ")
            f.write('{"city":"%s","country":"%s"}' % (city, country) )
            f.close()

def queryAPIMaghrib():
    try:
        import requests
    except ImportError:
        while True:
            install_perm = raw_input("[autoIftar] A needed utility was not found, would you like to install?(yes or no): ")
            if install_perm == "yes":
                os.system("pip install requests")
                break
            elif install_perm == "no":
                exit(0)
                break
            else:
                print("[autoIftar] Wrong input")
    response = requests.get("http://api.aladhan.com/v1/timingsByCity?city={}&country={}&method=8".format(city, country))
    json_response = response.json()
    if response.status_code != 200 or json_response["status"] != "OK":
        print("[autoIftar] Something went wrong. Check your internet connection and your spelling.")
        exit(1)
    #We don't convert it back to an int because if the two first digits are zeros, the int gets simplified
    maghrib_time = str(json_response["data"]["timings"]["Maghrib"]).replace(":", "")
    return maghrib_time

def loopForAthan(trigger):
    try:
        from playsound import playsound
    except ImportError:
        while True:
            install_perm = raw_input("[autoIftar] A needed utility was not found, would you like to install?(yes or no): ")
            if install_perm == "yes":
                os.system("pip install playsound")
                break
            elif install_perm == "no":
                exit(0)
                break
            else:
                print("[autoIftar] Wrong input")
    if not runforever:
        while True:
            time.sleep(60)
            current_time = int(str(time.strftime("%H:%M", time.localtime())).replace(":", ""))
            if current_time == trigger:
                playsound("./athan.mp3")
                break
    else:
        while True:
            time.sleep(60)
            current_time = int(str(time.strftime("%H:%M", time.localtime())).replace(":", ""))
            if current_time == trigger:
                playsound("./athan.mp3")

if __name__ == '__main__':
    config()
    loopForAthan(queryAPIMaghrib())
