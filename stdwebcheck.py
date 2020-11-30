from __init__ import *
from main import *

# Ignore HTTPS warnings while using a proxy
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# did not work:
# os.environ['PYTHONWARNINGS'] = "ignore:Unverified HTTPS request"

import argparse


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

parser.add_argument('-f','--file', type=str, help='Use a file that contains a copy of burp request',default="")
parser.add_argument('-u','--url', type=str, help='Standard webcall to given url',default="")
parser.add_argument('-v','--verbose', type=str2bool, nargs='?', const=True, default=False,help='Detailed output')
parser.add_argument('-dr','--dir', type=str, help='Define the directory which is used to save all the files into. Without this option the current directory is used',default="")
parser.add_argument('-da', type=str, help='Absolute path',default="")


soon = parser.add_argument_group('Coming soon')
soon.add_argument('-m','--method', type=str, help='Only works with usage of url, defines the method. Default is GET', default="GET")
soon.add_argument('-p','--port', type=str, help='Only works with usage of file, use this if the standard port is not in use (443 or 80)',default="")
soon.add_argument('-c','--clear', type=str, help='Use this if the target is not using TLS or SSL',default="")
soon.add_argument('--interactive', type=str, help='(Dachte dabei an soetwas wie bei jedem einzelnen Finding ja nein drücken, oder auch paramter dabei zu ändern ... ist natürlich viel Aufwand ...',default="")
soon.add_argument('--proxy', type=str, help='',default="")
soon.add_argument('--redirect', type=str, help='',default="")
soon.add_argument('--follow', type=str, help='',default="")

args = parser.parse_args()

config.debug=args.verbose
file1=args.file
use_file=False if (file1 == "") else True
url=args.url
use_url=False if (url == "") else True
config.path=args.dir
config.relative=False if (config.relative == "") else True
config.absolutepath=args.da
config.relative=True if (config.absolutepath == "") else False

#use_file = use_url = False
#file = url = ""

def start(response):
    burpconverter.httpvers = "HTTP/" + str(response.raw.version)[:1] + "." + str(response.raw.version)[1:]  # workaround for showing the http-version
    findings.finding.check_for_findings(response.request, response)

print(1)

if (use_file == False and use_url == False):
    print("Neither an url nor a file was given.")
    exit(0)

print(2)
#Prepare webcall and start it
webcall.check_proxy()
print(3)
print(use_file)
print(file1)
if (use_file): webcall.set_file(file1)
else: webcall.set_url(url)
print(5)
response = webcall.call()
print(6)
start(response)
print(7)
