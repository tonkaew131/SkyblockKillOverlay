import config as config
import os
import time
import requests

def GetKillMobsList(stats):
    MobsList = []
    for mob in stats:
        if mob[:6] == "kills_":
            MobsList.append([mob, stats[mob]])
    return MobsList

# Check if folder is exist
if not os.path.exists('kills'):
    os.makedirs('kills')
    
# Check if config is valid
Config = [config.ApiKey, config.Username, config.Profile, 
        config.EnableKillCount, config.RefreshTime, config.EnableAll]    
if Config[0]==None:
    print("Invalid API Key")
    exit()
elif Config[1]==None:
    print("Username can't be empty")
    exit()
elif Config[2]==None:
    print("Profile can't be empty")
    exit()
elif len(Config[3])==0 and Config[5]==False:
    print("You must choose enable all or enable some")
    exit()
elif type(Config[4])!=int:
    print("Refresh time must be number")
    exit()

# Check if username is valid and get uuid
UUID = ""
r = requests.get("https://api.mojang.com/users/profiles/minecraft/"+Config[1])
status = r.status_code
if status == 200:
    data = r.json()
    UUID = data["id"]
elif status == 204:
    print("Username not found")
    exit()
else:
    print("Mojang API Error")
    exit()

while True:
    # Check if Hypixel API is limit
    Limit = True
    r = requests.get("https://api.hypixel.net/key?key="+Config[0]) 
    data = r.json()
    if(data["success"]==False):
        print("[WARNING]: Hypixel API Error, " + data["cause"])
    if(data["success"]==True):
        if(data["record"]["queriesInPastMin"] >= ( data["record"]["limit"] - 1 )): 
            Limit = True
            print("WARNING]: API Queries limit!")
        else:
            Limit = False

    # Get Skyblock Profile stats
    stats = {}
    if Limit == False:
        r = requests.get("https://api.hypixel.net/skyblock/profiles?key="+Config[0]+"&uuid="+UUID) 
        data = r.json()
        if(data["success"]==False):
            print("[WARNING]: Hypixel API Error, " + data["cause"])
        if(data["success"]==True):
            Profiles = data["profiles"]
            for Profile in Profiles:
                if Profile["cute_name"] == Config[2]:
                    if ( "stats" in Profile["members"][UUID] ):
                        stats = Profile["members"][UUID]["stats"]
                    else:
                        print("[ERROR]: API Disable")
                        exit()
            if not stats:
                print("Can't find " + Config[2] + " profile")
                exit()
    
    # Update kills text file
    if Config[5]:
        for mob in GetKillMobsList(stats):
            f = open("./kills/"+mob[0]+".txt", "w")
            f.write(str(round(mob[1])))
            f.close()
    else:
        [x.lower() for x in Config[3]]
        for mob in GetKillMobsList(stats):
            if mob[0].replace("kills_", "").lower() in Config[3]:
                f = open("./kills/"+mob[0]+".txt", "w")
                f.write(str(round(mob[1])))
                f.close()

    # Refresh Time
    time.sleep(Config[4])