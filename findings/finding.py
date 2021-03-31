import findings
import config
import template
import pathlib
from config import config

def create_finding(type, text, code, suffix=""):
    print(" found " + type + " ...", end='')
    filename = type
    if (suffix != ""): filename += "." + suffix

    if (config['relative']): path = pathlib.Path().absolute() / config['relativepath']
    else: path = pathlib.Path(config['absolutepath'])

    if (config['debug']): print("Path = " + path)

    #dradis-workaround
    if (template.dradis):
        if ("p." in code[-4:]): code = code[:-4]

    if config['output']:
        with open(path / filename, "w") as f:
            f.write(template.template_start + text + "\n\n" + code + template.template_end)

def check_for_findings(request, response):
    print("Starting the web calls and checking for findings ...")
    #Call every finding-script here
    findings.cookies.check_cookies(request, response)
    findings.hsts.check_hsts(request, response)
    findings.infodisc.info_disc(request, response)
    findings.cors.check_cors(request, response)
    findings.arbitraryhost.check_hostheader(request, response)
    findings.xssfilter.check_xssfilter(request, response)
    print("... done")
