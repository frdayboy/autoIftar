#!/usr/bin/env python
import os
import json

def config():
    try:
        with open("./config.json", "r") as f:
            config = json.loads(f.read())
            city = config["city"]
            country = config["country"]
            global city, country
            f.close()
    #No config file, probably first use of tool
    except IOError:
        with open("./config.json", "w+") as f:
            print("[autoIftar] No configuration file found. This seems to be your first time using this tool.")
            city = raw_input("[autoIftar] Please enter your city (Spaces and Capitalizations Included): ")
            country = raw_input("[autoIftar] Please enter your country (Spaces and Capitalizations Included): ")
            global city, country
            json.dump('{"city":"%s", "country":"%s"}' % (city, country), f)
            f.close()
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

def queryAPIMaghrib():
    response = requests.get("http://api.aladhan.com/v1/timingsByCity?city={}&country={}&method=8".format(city, country))
    if response.status_code !== 200:
        print("[autoIftar] Something went wrong. Check your internet connection and your spelling.")
        exit(1)
    json_response = response.json()
    
if __name__ == '__main__':
    config()
    queryAPIMaghrib()
    playAthan()
