# Role Saver
Discord bot that saves and restores member roles when they leave and rejoin a server.

# Hosting
First you need to [Create a Discord Bot](#creating-the-discord-bot)

After, there are 2 ways to run the bot - either via [Docker](#docker) or the [old fashion python way](#classic-python-way).

## Creating the Discord Bot
No matter your method of hosting, you need to create the bot account first.

1. Create a Discord Bot in the [Discord Developers Portal](https://discord.com/developers/applications). You can do so by going to Applications, creating a new Application, going to Bot and creating a new bot.
2. Save the token that it gives you.
3. Under "Privileged Gateway Intents" make sure "Server Members Intent" is selected.
4. Invite your bot to your server by using this link, replacing APPLICATION_ID with the application ID of your bot found under General Information: https://discord.com/oauth2/authorize?client_id=`APPLICATION_ID`&scope=bot&permissions=2550138912

## Docker
1. First, you will obviously need to install [Docker](https://docs.docker.com/engine/install/)

2. Create an empty directory and make a file in it called `docker-compose.yml`.

3. Copy and paste the stuff from [my docker compose file](docker-compose.yml) into you `docker-compose.yml`.
    - If you are already running a MySQL server, or you installed one manually, and don't need to spin up a new one, you can comment out or delete everything below [line 13](docker-compose.yml#13) and set the [MYSQL_HOST](docker-compose.yml#9) and [MYSQL_PASSWORD](docker-compose.yml#13) variables to your MySQL serer

4. Put your bot token you got from [creating the discord bot](#creating-the-discord-bot) and set it to the DISCORD_TOKEN variable in your [docker-compose.yml on line 8](docker-compose.yml#8)

5. Set the password for your MySQL server at [MYSQL_PASSWORD on line 11](docker-compose.yml#11). Set that same password at [MYSQL_ROOT_PASSWORD on line 25](docker-compose.yml#25)

6. Save the file

7. In the directory containing your `docker-compose.yml`, run `docker compose up -d`.

8. It is now running! You can check the logs by running `docker logs rolesaver_discord_bot`

## Classic Python Way
If for some reason you don't want to use Docker, you can also run it as a normal Python app. This assumes you have basic knowledge of hosting and can set up a MySQL server and Python

1. Clone or download this repo to your machine 

2. Install and run a [MySQL server](https://dev.mysql.com/downloads/installer/). You will need to create a database called `rolesaver`

3. Install [Python 3.12](https://www.python.org/)

4. cd into the repo directory `cd rolesaver`

5. Run `python3 -m pip install -r requirements.txt` to install all required packages

6. Rename the [.env.example](.env.example) file to just `.env`

7. Set the variables in `.env` to your MySQL credentials and your Discord token

8. Uncomment lines 1 and 6 from [main.py](main.py) so it looks like below
```python
from dotenv import load_dotenv
from bot import rolesaver
import commands
import events
import context
load_dotenv() # loads token from local .env file. 

rolesaver.run()
```

9. Save main.py and run `python3 main.py`

10. It is now running!

# Updating
Updating should be simple, the main branch of this repo will always be the latest version that the public bot uses.

## Updating via Docker
Updating is easy with docker. 

For automatic updates, I recommend using [watchtower](https://containrrr.dev/watchtower/). You will need to follow the instructions for [allowing watchtower to access private registries](https://containrrr.dev/watchtower/private-registries/). After watchtower is set up correctly, it will check every 24 hours and automatically update your containers if needed.

For manually updating, you just need to run 3 commands:
1. cd into your directory containing your `docker-compose.yml`
2. Run `docker compose pull` to pull latest image
3. Run `docker compose up -d --remove-orphans` to restart your containers
4. Run `docker image prune` to remove the old images

## Updating via Python

1. cd into your directory containing the repo
2. Stop the current bot
3. Pull the latest changes with `git pull` or redownload manually from github
4. Start the bot