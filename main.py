from dotenv import load_dotenv
from bot import rolesaver
from commands.blacklist import blacklist
load_dotenv() # loads token from local .env file. when in production, ill probably just use docker

rolesaver.run()