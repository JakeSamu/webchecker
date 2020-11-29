from __init__ import *
from main import *

help = """
NAME
    StandardWebCheck - get your standard web findings ready for your report
    
SYNOPSIS
    python3 stdwebcheck.py [OPTIONS]
        
OPTIONS
    --help, -h\t\t\tshow this
    --file [BURPFILE], -f\t\t\tUse a file that contains a copy of burp request
    --url [URL], -f\t\t\tStandard webcall to given url
    --verbose, -v\t\t\tDetailed output
    --dir, -dr\t\t\tDefine the directory which is used to save all the files into. Without this option the current directory is used.
    \t-da\t\t\tAbsolute path
    
    Coming soon:
    --method [METHOD], -m\t\t\tOnly works with usage of url, defines the method. Default is GET
    --port [PORT], -p\t\t\tOnly works with usage of file, use this if the standard port is not in use (443 or 80)
    --clear, -c\t\t\tUse this if the target is not using TLS or SSL
    --interactive (Dachte dabei an soetwas wie bei jedem einzelnen Finding ja nein drücken, oder auch paramter dabei zu ändern ... ist natürlich viel Aufwand ...
    --proxy
    --redirect/--follow
    
EXAMPLES
    python3 stdwebcheck.py -u https://www.google.com
    python3 stdwebcheck.py -f burprequest
    """

use_file = use_url = False
file = url = ""

def start(response):
    burpconverter.httpvers = "HTTP/" + str(response.raw.version)[:1] + "." + str(response.raw.version)[1:]  # workaround for showing the http-version
    findings.finding.check_for_findings(response.request, response)

def single_option(option):
    if (option == "--help" or option == "-h"):
        print(help)
        exit(0)
    if (option == "--verbose" or option == "-v"):
        config.debug = True

def argument_option(option, param):
    global use_file, file, use_url, url
    if (option == "--file" or option == "-f"):
        if (use_file == False and use_url == False):
            use_file = True
            file = param
        else: print("You already used a file or an url as an argument.")
    if (option == "--url" or option == "-u"):
        if (use_file == False and use_url == False):
            use_url = True
            url = param
        else: print("You already used a file or an url as an argument.")
    if (option == "--dir" or option == "-dr"):
        config.relative = True
        config.path = param
    if (option == "-da"):
        config.relative = False
        config.absolutepath = param

if (len(sys.argv) < 2):
    print(help)
    exit(0)
else:
    use_file = False
    use_url = False
    hadoption = False

    i = 1 #since argument 0 is predefined as the path to current directory
    while i < len(sys.argv):
        option = sys.argv[i]
        if ("-" != option[0]):
            print("The argument \'" + option + "\' is not a defined option.")
            exit(0)
        if (i + 1 >= len(sys.argv)):
            single_option(option)
            break
        param = sys.argv[i+1]

        if ("-" == param[0]):
            i += 1
            single_option(option)
        else:
            i += 2
            argument_option(option, param)

    if (use_file == False and use_url == False):
        print("Neither an url nor a file was given.")
        exit(0)

    #Prepare webcall and start it
    webcall.check_proxy()
    if (use_file): webcall.set_file(file)
    else: webcall.set_url(url)
    response = webcall.call()
    start(response)
