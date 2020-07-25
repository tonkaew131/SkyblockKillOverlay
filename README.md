# Skyblock Kill Overlay

Create Text file that contained kill count of all mobs or specific mob. Kill count get from Hypixel API and update every 30 seconds by default.

## Run

### From release

First, you need to download this program. By click ![this](https://github.com/tonkaew131/SkyblockKillOverlay/releases/tag/1) or go to release page

After that, Extract .RAR file. You will get folder's name Skyblock Kill Overlay V1. Now you just click main.exe to run ( don't forget to config first )

## From Source

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
Username = ""
Profile = ""

# Enable all kill
EnableAll = False

# Refresh time ( in seconds ) ( default is 30 )
RefreshTime = 30

# Kill count enable list ( Leave it empty when EnableAll is True )
# Example: ['zealot_enderman', 'ruin_wolf']
EnableKillCount = ['zealot_enderman', 'enderman']
```

## Contributing

Feel free to fix my error.

## Authors

* **Athicha Leksansern** - *Initial work* - [Tonkaew](https://github.com/tonkaew131/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
