from __init__ import *
from main import *
import argparse

# Ignore HTTPS warnings while using a proxy
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Allow several arguments besides True and False
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file',     type=str,       default=config.file,        help='Use a file that contains a copy of burp request')
parser.add_argument('-u', '--url',      type=str,       default=config.url,         help='Standard webcall to given url')
parser.add_argument('-v', '--verbose',  type=str2bool,  default=config.debug,       help='Detailed output', nargs='?', const=True)
parser.add_argument('-dr', '--dir',     type=str,       default=config.relativepath,        help='Define the directory which is used to save all the files into. Without this option the current directory is used')
parser.add_argument('-da',              type=str,       default=config.relative,    help='Absolute path')


soon = parser.add_argument_group('Coming soon')
soon.add_argument('-m', '--method',     type=str,       default=config.method,      help='Only works with usage of url, defines the method. Default is GET')
soon.add_argument('-p', '--port',       type=str,       default="",                 help='Only works with usage of file, use this if the standard port is not in use (443 or 80)')
soon.add_argument('-c', '--clear',      type=str,       default="",                 help='Use this if the target is not using TLS or SSL')
soon.add_argument('--interactive',      type=str,       default="",                 help='(Dachte dabei an soetwas wie bei jedem einzelnen Finding ja nein drücken, oder auch paramter dabei zu ändern ... ist natürlich viel Aufwand ...')
soon.add_argument('--proxy',            type=str,       default="",                 help='')
soon.add_argument('--redirect',         type=str,       default="",                 help='')
soon.add_argument('--follow',           type=str,       default="",                 help='')

args = parser.parse_args()

config.debug = args.verbose
#File
file1 = args.file
use_file = False if (file1 == "") else True
#URL
url = args.url
use_url = False if (url == "") else True
#Path
config.relative = True if (config.relativepath != args.dir) else False
config.absolutepath = args.da
config.relativepath = args.dir


def start(response):
    burpconverter.httpvers = "HTTP/" + str(response.raw.version)[:1] + "." + str(response.raw.version)[1:]  # workaround for showing the http-version
    findings.finding.check_for_findings(response.request, response)

if (use_file == False and use_url == False):
    print("Neither an url nor a file was given.")
    exit(0)

#Prepare webcall and start it
webcall.check_proxy()
if (use_file): webcall.set_file(file1)
else: webcall.set_url(url)
response = webcall.call()
start(response)
