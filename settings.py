import datetime
import sys
from pathlib import Path
from configparser import ConfigParser

scriptpath = Path(__file__).resolve().parent
inifile = ConfigParser()
try:
    inifile.read(scriptpath / 'localsettings.ini') # Versie die niet in Git is ingecheckt
except:
    inifile.read(scriptpath / 'settings.ini')

subdomain = int(inifile.get('general', 'subdomain'))
api_key = inifile.get('general', 'api_key')
api_secret = inifile.get('general', 'api_secret')
