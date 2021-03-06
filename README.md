# Skyblock Kill Overlay

Create Text file that contained kill count of all mobs or specific mob. Kill count get from Hypixel API and update every 30 seconds by default.

- Total Kill Count
- Kill since program started
- Fairy souls Count

## Installation & Run

### From release

1. Download the program, By click [this](https://github.com/tonkaew131/SkyblockKillOverlay/releases/tag/1.2) or go to release page

2. Extract .rar file, wherever you want.

3. Run main.exe for first time to create config file.

4. Config some settings.

4. Run main.exe and Enjoy!

### From Source

```
python main.py
```

This application will automatic create text file in kills directory. Then you can add text file to your OBS or etc.

![OBS Picture](https://github.com/tonkaew131/SkyblockKillOverlay/blob/master/picture1.png)

## Config

```
# You can obtain an API key by joining mc.hypixel.net 
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
EnableFairySouls = True
```

## Contributing

Feel free to fix my error.

## Authors

* **Athicha Leksansern** - *Initial work* - [Tonkaew](https://github.com/tonkaew131/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
