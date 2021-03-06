import requests
import pydactyl
import pysftp
from os import environ, remove
from dotenv import load_dotenv
load_dotenv()

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
 
sftp_url = environ.get('SFTP_URL')
sftp_port = int(environ.get('SFTP_PORT'))
sftp_user = environ.get('SFTP_USER')
sftp_password = environ.get('SFTP_PASS')

paper_jarfile = environ.get('PAPER_JAR')

panel_key = environ.get('PANEL_KEY')
panel_url = environ.get('PANEL_URL')
print(panel_url)

panel = pydactyl.PterodactylClient(panel_url, panel_key)
servers = panel.client.list_servers()
server_id = servers[0]['identifier']

print('Stopping server...')
panel.client.send_power_action(server_id, 'stop')
print('Server stopped')

print('Downloading Paper JAR')
request = requests.get('https://papermc.io/api/v1/paper/1.16.1/latest/download')
open(paper_jarfile, 'wb').write(request.content)

with pysftp.Connection(host=sftp_url, port=sftp_port, username=sftp_user, password=sftp_password, cnopts=cnopts) as sftp:
    print('SFTP connection established')
    sftp.remove(paper_jarfile)
    print('Old JAR deleted, uploading new...')
    sftp.put(paper_jarfile)
    print('New JAR uploaded, deleting local copy...')
    remove(paper_jarfile)

print('Starting server back up...')
panel.client.send_power_action(server_id, 'start')
print('Server started')        