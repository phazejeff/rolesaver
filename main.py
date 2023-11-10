from dotenv import load_dotenv
from bot import RoleSaver
load_dotenv() # loads token from local .env file. when in production, ill probably just use docker

rolesaver = RoleSaver()
rolesaver.run()