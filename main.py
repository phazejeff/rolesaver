from dotenv import load_dotenv
from bot import rolesaver
import commands
import events
import context
load_dotenv() # loads token from local .env file. when in production, ill probably just use docker

rolesaver.run()