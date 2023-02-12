from pyzm.interface import ZMESConfig
import pyzm
import pyzm.api as zmapi
import getpass
import traceback
import yaml
import pyzm.ZMMemory as zmmemory
from pyzm.interface import GlobalConfig, MLAPI_DEFAULT_CONFIG as DEFAULT_CONFIG
import pyzm.helpers.mlapi_db as mlapi_user_db
from pyzm import __version__ as pyzm_version
from pyzm.api import ZMApi
from pyzm.helpers.pyzm_utils import str2bool, import_zm_zones, start_logs
from pyzm.helpers.pyzm_utils import LogBuffer

CONFIG_PATH = r'/var/lib/zmeventnotification/mlapi/mlapiconfig.yml'
SECRETS_LOCAL = r'/home/arndt/Develop/zm-programming/zm-api/secrets.yml'

g: GlobalConfig


def loadYAML():

    # with open(SECRETS_LOCAL, 'r') as file:
    with open('/etc/zm/secrets.yml', 'r') as file:

        prime_service = yaml.safe_load(file)

    api_url = prime_service['secret']['ZM_API_PORTAL']
    portal_url = prime_service['secret']['ZM_PORTAL']

    return (prime_service)


def main():

    global g
    g = GlobalConfig()

    g.DEFAULT_CONFIG = DEFAULT_CONFIG
    g.logger = LogBuffer()
    api: ZMApi = g.api
    mlc: ZMESConfig = ZMESConfig(CONFIG_PATH, DEFAULT_CONFIG, "mlapi")
    g.config = mlc.config

    api_url = loadYAML()['secret']['ZM_API_PORTAL']
    portal_url = loadYAML()['secret']['ZM_PORTAL']

    api_options = {
        "apiurl": loadYAML()['secret']['ZM_API_PORTAL'],
        "portalurl": loadYAML()['secret']['ZM_PORTAL'],
        "user": loadYAML()['secret']['ZM_ML_USER'],
        "password": loadYAML()['secret']['ZM_ML_PASSWORD'],
        "basic_auth_user": loadYAML()['secret']['ZM_ML_USER'],
        "basic_auth_password": loadYAML()['secret']['ZM_ML_PASSWORD'],
        "logger": g.logger,  # currently, just a buffer that needs to be iterated and displayed
        "disable_ssl_cert_check": str2bool(g.config.get("allow_self_signed")),
        "sanitize_portal": str2bool(g.config.get("sanitize_logs")),
    }

    g.api = ZMApi(options=api_options)

    Auth = g.api.get_auth()

    """ Monitors"""
    Monitors = g.api.monitors()

    """ Events """
    Events = g.api.events()

    l = 0
    for i in Events.events:
        if Events.events[l].notes != 'Motion: All':
            print(f"Notes:{l:2} {Events.events[l].notes}")
        l = l+1

    E1 = Events.events
    E2 = Events.events[00]
    E3 = Events.events[00].event
    E3 = Events.events[00].event['Event']
    Id = Events.events[00].event['Event']['Id']

    """ Event - Monitor - Frame """
    g.Event, g.Monitor, g.Frame = g.api.get_all_event_data(4364)
    event = g.Event
    monitor = g.Monitor
    frame = g.Frame
    FrameId = frame[00]["Id"]

    Zones = g.api.zones()
    States = g.api.states()

    """ Version """
    version = g.api.version()
    status = version["status"]
    zm_version = version["zm_version"]

    """ State """
    Authenticated = g.api.authenticated
    States = g.api.states

    Config = g.api.configs()

    i = 0


if __name__ == "__main__":
    main()
