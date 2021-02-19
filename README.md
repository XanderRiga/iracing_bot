# iRacing Bot
This is a cog for discord.py that allows users to view and compare their iRacing data directly inside of discord.

This uses [My iRacing Cog](https://github.com/XanderRiga/iracing_cog) under the hood

## Like this bot? You can buy me a beer [here](https://www.buymeacoffee.com/xanderriga)

## You can always use `!help` to see what the bot can do


# What it Does
This bot has 2 primary functions, it can show you the current weekly combos of what track your favorite series are on, 
and compare you to your friends through the leaderboards and other statistics. 
You can find examples of these actions and the commands to do these actions below.


# Some Important Notes
- The iRacing API is _slow_ to update. 
  When you finish a race it can take a day or sometimes more to appear in their API, which means the bot will not have that information either.
  When in doubt, run `!update`
- Please do not spam `!update` and `!updateserver`. 99% of the time the iRacing API just hasn't updated yet, 
  so you will never get live to the minute data, that just isn't a capability of the current iRacing API.

# Bot Invite Link
Want the bot in your discord? Click this link to add it:
https://discord.com/oauth2/authorize?client_id=706222703664693308&scope=bot

# Support & Questions
Come to the discord [here](https://discord.gg/bAq8Ec5JPQ) for support

## Commands
## Series Combos Related
### !allseries
This will give a list of all current active series names and IDs(which are used for the favorite series commands).

### !setfavseries <Series IDs\>
This will set the favorite series for your server. Server IDs in this case is a list of comma separated
Series IDs that can be found from the `!allseries` command. Setting favorite series is necessary to
use the `!currentseries` command.

### !currentseries
Once favorite series have been set through `!setfavseries` this command prints images
showing the current tracks for each of the favorite series for this race week and the next race week.

### !addfavseries
This is similar to `!setfavseries` except it just adds a single series to the favorites list.

### !removefavseries
This removes a single favorite from the saved favorite series

## Leaderboard/Statistics Related
### !saveid <iRacing Client ID\>
Use this command to save your iRacing ID to your discord ID.
If you already have one saved this will overwrite it

### !savename <iRacing Name\>
Use this command to save your name and iRacing ID to your discord ID.
The name you submit must be exactly the same as your name on iRacing, including any numbers
If you already have one saved this will overwrite it

### !recentraces <iRacing Client ID \>
This gives detailed information on the last 10 races of the given user.
If no iRacing Client ID is provided, it will default to the saved ID of the user who called it.
If the user who called it has not saved their ID, then they must provide an ID when calling.

### !update
This will update the saved information for just the user who called the command.

### !updateserver
This will update the saved information for all users in the discord for use of the `!leaderboard` command.
All discords are automatically updated every hour, so often this is unnecessary to run.

**NOTE:** The iRacing API does not update frequently, so even if you finished a race recently and expect to see changes, 
it can take up to a day for those to come through on the bot.

### !leaderboard <category\> <type\>
This prints a leaderboard of all users with saved IDs(through the `!saveid` command) for the given category and type.
Category can be any of `road`, `oval`, `dirtroad`, and `dirtoval`, but it defaults to `road`.
Type is either `career` or `yearly`, and it defaults to career. `career` will show all time data, 
and `yearly` will only show data from the current year.

**NOTE:** This can be called with a category and no type, but if you want to call with a type, you need to pass a category.
For instance, I can call `!leaderboard oval`, but if I want the road leaderboard yearly I need to specify: `!leaderboard road yearly`, `!leaderboard yearly` is **NOT** valid.

### !iratings <category\>
This prints a graph of all saved user's iratings over the last 6 months. 
Category can be any of `road`, `oval`, `dirtroad`, and `dirtoval`, and defaults to `road`. 

### !careerstats <iRacing Client ID\>
This will give an overview of the career stats of the player with the given iRacing Client ID.
If an iRacing Client ID is not provided, then it will use the saved ID for the user who called the command.
If the user has not saved their ID, they must provide an iRacing Client ID.

### !yearlystats <iRacing Client ID\>
This will give an overview of the yearly stats of the player with the given iRacing Client ID.
If an iRacing Client ID is not provided, then it will use the saved ID for the user who called the command.
If the user has not saved their ID, they must provide an iRacing Client ID.

# Local Setup
- Make sure you have [pipenv](https://pypi.org/project/pipenv/) installed wherever you plan to run the bot.
- From the root folder of the bot you will need to clone [this repo](https://github.com/XanderRiga/iracing_cog) 
  into the `iracing_cog` folder
- From the root folder of the **cog**(note: not the bot, the cog), you will need to clone 
  [this repo](https://github.com/Esterni/pyracing) into the pyracing folder.
- Run `pipenv shell` and then pip install . from inside the root of the `pyracing` dir
  
  *Note* I am aware this setup is insane with 3 nested repos, and I am actively working to move away from this method.
- Once you have cloned the bot, from inside the root folder of the bot, run `pipenv install`
- You will need to do a special installation for `wkhtmltopdf` which is part of what is used to generate images. 
  Follow the instructions from step 2 [here](https://pypi.org/project/imgkit/) for your platform.
- You will also need to install the chromium chromedriver:

Linux: `sudo apt install chromium-chromedriver`

Mac: `brew install chromedriver -cask`
- You will need a `.env` file in the root of this project that looks like this:
```
IRACING_USERNAME=your username here
IRACING_PASSWORD=your password here
BOT_TOKEN=your bot's token from discord
```
This will allow the bot to actually hit the iracing servers using your login information.
- From the root of the bot repo, run `pipenv shell` if you aren't already in the shell, and then `python bot.py`
- You did it! The bot should be running locally now and once you invite it to your server, you can use it
- If you want to keep the bot running 24/7, you should be able to get it running with [PM2](https://pm2.keymetrics.io/)

## Common Gotchas
- If the images seem to be failing, make sure you followed the instructions to install wkhtmltopdf correctly.
- If there seems to be something strange happening, make sure you pull master for the bot, the cog, and pyracing. 
  I know this setup is insane, and I intend to merge the bot and the cog eventually.
- Make sure your iracing credentials are correct, and sometimes you may need to go to the member website and do a 
  captcha if the bot seems stuck getting failures.
- There will be a bunch of noisy log output. This is because I am using LogDNA for my bot in production and 
  built it to use that, I will be removing this requirement as it causes a lot of noise if it isn't set up, 
  but you don't have to worry about it. If by some chance you also use LogDNA, you can set the 
  `LOG_LOCATION` and `LOGDNA_INGESTION_KEY` in the `.env` where the location is `dev` or `prod` or something like that, 
  and it will link up to your LogDNA account.