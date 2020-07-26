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

# Refresh time ( in seconds ) ( default is 30 )
RefreshTime = 30

# --------------------------- Total Kill --------------------------- #
# Kill total count mobs list ( Leave it empty when EnabletTotalKill_AllMobs is True )
# Example: ['zealot_enderman', 'ruin_wolf']
EnableTotalKill = ['zealot_enderman', 'ruin_wolf']
# Enable total kill ( all mobs )
EnabletTotalKill_AllMobs = False

# -------------------- Kill since program start -------------------- #
# Kill count mobs list ( Leave it empty when EnabletTotalKill_AllMobs is True )
# Example: ['zealot_enderman', 'ruin_wolf']
EnableKill = []
# Enable kill ( all mobs )
EnabletKill_AllMobs = True

# ------------------------------ etc ------------------------------ #
EnableFairySouls = True""")
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

EnableTotalKill             = config.EnableTotalKill
EnabletTotalKill_AllMobs    = config.EnabletTotalKill_AllMobs

EnableKill          = config.EnableKill
EnabletKill_AllMobs = config.EnabletKill_AllMobs

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
elif (len(EnableTotalKill)!=0) and EnabletTotalKill_AllMobs:
    print("You must choose Enable all mobs or Enable some mobs or Disable both")
    input("Press Enter to continue...")
    exit()
elif (len(EnableKill)!=0) and EnabletKill_AllMobs:
    print("You must choose Enable all mobs or Enable some mobs or Disable both")
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

FirstTime = True
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
    
    # If it's first then save start state
    if FirstTime:
        if EnabletKill_AllMobs or len(EnableKill)!=0:
            Start_Kill_AllMobs_List = []
            Start_Kill_List         = []
            for mob in GetKillMobsList(stats):
                if EnabletKill_AllMobs:
                    Start_Kill_AllMobs_List.append([mob[0], mob[1]])
                else:
                    if mob[0].replace("kills_", "").lower() in EnableKill:
                        Start_Kill_List.append([mob[0], mob[1]])
        FirstTime = False

    # Update total kills text file
    if EnabletTotalKill_AllMobs:
        for mob in GetKillMobsList(stats):
            f = open("./kills/total_"+mob[0]+".txt", "w")
            f.write(str(round(mob[1])))
            f.close()
    elif len(EnableTotalKill)!=0:
        [x.lower() for x in EnableTotalKill]
        for mob in GetKillMobsList(stats):
            if mob[0].replace("kills_", "").lower() in EnableTotalKill:
                f = open("./kills/total_"+mob[0]+".txt", "w")
                f.write(str(round(mob[1])))
                f.close()

    # Update kills since start program text file
    if EnabletKill_AllMobs:
        for mob in GetKillMobsList(stats):
            for start_mob in Start_Kill_AllMobs_List:
                if start_mob[0] == mob[0]:
                    f = open("./kills/"+mob[0]+".txt", "w")
                    f.write(str(round(mob[1]-start_mob[1])))
                    f.close()
    elif len(EnableKill)!=0:
        [x.lower() for x in EnableKill]
        for mob in GetKillMobsList(stats):
            if mob[0].replace("kills_", "").lower() in EnableKill:
                for start_mob in Start_Kill_List:
                    if start_mob[0] == mob[0]:
                        f = open("./kills/"+mob[0]+".txt", "w")
                        f.write(str(round(mob[1]-start_mob[1])))
                        f.close()


    # Update fairy souls
    if EnableFairySouls:
        f = open("./etc/fairy_souls_collected.txt", "w")
        f.write(str(fairy_souls_collected))
        f.close()

    # Refresh Time
    time.sleep(RefreshTime)
