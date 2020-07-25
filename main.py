import os
import time
import requests
from sys import exit

def GetKillMobsList(stats):
    MobsList = []
    for mob in stats:
        if mob[:6] == "kills_":
            MobsList.append([mob, stats[mob]])
    return MobsList

# Check if folder is not exist
if not os.path.exists('kills'):
    os.makedirs('kills')
if not os.path.exists('etc'):
    os.makedirs('etc')
    
# Check if config file is not exist
if not os.path.isfile('./config.py'):
    f = open("./config.py", "w")
    f.write("""# You can obtain an API key by joining mc.hypixel.net 
# with a valid Minecraft account and running the /api command.
ApiKey = ""

# Your minecraft username & profile name
Username    = ""
ProfileName = ""

# Enable all kill
EnableKillAll = True

# Refresh time ( in seconds ) ( default is 30 )
RefreshTime = 30

# etc
EnableFairySouls = True

# Kill count enable list ( Leave it empty when EnableAll is True )
# Example: ['zealot_enderman', 'ruin_wolf']
EnableKillCount = ['zealot_enderman', 'enderman']""")
    f.close()
    print("No Config file, created.")
    print("Please set config first.")
    input("Press Enter to continue...")
    exit()

# Check if config is valid
import config as config

ApiKey           = config.ApiKey
Username         = config.Username
ProfileName      = config.ProfileName
RefreshTime      = config.RefreshTime
EnableKillCount  = config.EnableKillCount
EnableKillAll    = config.EnableKillAll
EnableFairySouls = config.EnableFairySouls

if ApiKey==None:
    print("Invalid API Key")
    input("Press Enter to continue...")
    exit()
elif Username==None:
    print("Username can't be empty")
    input("Press Enter to continue...")
    exit()
elif ProfileName==None:
    print("Profile can't be empty")
    input("Press Enter to continue...")
    exit()
elif len(EnableKillCount)==0 and EnableKillAll==False:
    print("You must choose enable all or enable some")
    input("Press Enter to continue...")
    exit()
elif type(RefreshTime)!=int:
    print("Refresh time must be number")
    input("Press Enter to continue...")
    exit()

# Check if username is valid and get uuid
UUID = ""
r = requests.get("https://api.mojang.com/users/profiles/minecraft/"+Username)
status = r.status_code
if status == 200:
    data = r.json()
    UUID = data["id"]
elif status == 204:
    print("Username not found")
    input("Press Enter to continue...")
    exit()
else:
    print("Mojang API Error")
    input("Press Enter to continue...")
    exit()

while True:
    # Check if Hypixel API is limit
    Limit = True
    r = requests.get("https://api.hypixel.net/key?key="+ApiKey) 
    data = r.json()
    if(data["success"]==False):
        print("[WARNING]: Hypixel API Error, " + data["cause"])
    if(data["success"]==True):
        if(data["record"]["queriesInPastMin"] >= ( data["record"]["limit"] - 1 )): 
            Limit = True
            print("WARNING]: API Queries limit!")
        else:
            Limit = False

    # Get Skyblock Profile stats & Fairy Souls count
    stats = {}
    fairy_souls_collected = 0
    if Limit == False:
        r = requests.get("https://api.hypixel.net/skyblock/profiles?key="+ApiKey+"&uuid="+UUID) 
        data = r.json()
        if(data["success"]==False):
            print("[WARNING]: Hypixel API Error, " + data["cause"])
        if(data["success"]==True):
            Profiles = data["profiles"]
            for Profile in Profiles:
                if Profile["cute_name"] == ProfileName:

                    # Get fairy souls
                    if ( EnableFairySouls and "fairy_souls_collected" in Profile["members"][UUID] ):
                        fairy_souls_collected = Profile["members"][UUID]["fairy_souls_collected"]
                    elif ( EnableFairySouls and "fairy_souls_collected" not in Profile["members"][UUID] ):
                        print("[ERROR]: API Disable")
                        input("Press Enter to continue...")
                        exit()

                    # Get stats
                    if ( "stats" in Profile["members"][UUID] ):
                        stats = Profile["members"][UUID]["stats"]
                    else:
                        print("[ERROR]: API Disable")
                        input("Press Enter to continue...")
                        exit()

            if not stats:
                print("Can't find " + ProfileName + " profile")
                input("Press Enter to continue...")
                exit()
    
    # Update kills text file
    if EnableKillAll:
        for mob in GetKillMobsList(stats):
            f = open("./kills/"+mob[0]+".txt", "w")
            f.write(str(round(mob[1])))
            f.close()
    else:
        [x.lower() for x in EnableKillCount]
        for mob in GetKillMobsList(stats):
            if mob[0].replace("kills_", "").lower() in Config[3]:
                f = open("./kills/"+mob[0]+".txt", "w")
                f.write(str(round(mob[1])))
                f.close()

    # Update fairy souls
    if EnableFairySouls:
        f = open("./etc/fairy_souls_collected.txt", "w")
        f.write(str(fairy_souls_collected))
        f.close()

    # Refresh Time
    time.sleep(RefreshTime)
