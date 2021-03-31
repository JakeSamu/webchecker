import findings
import config
import template
import pathlib
from config import config
from main.str2bool import str2bool

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
    
    findinglist = {
                   'cookie flags': findings.cookies.check_cookies,
                   'HSTS': findings.hsts.check_hsts,
                   'information disclosures': findings.infodisc.info_disc,
                   'CORS': findings.cors.check_cors,
                   'host header': findings.arbitraryhost.check_hostheader,
                   'xssfilter': findings.xssfilter.check_xssfilter
                  }
    
    for (name,func) in findinglist.items():
        if (config['interactive']):
            create = str2bool(input("Do you want to check "+name+"? (Y/n)"))
            if create:
                func(request, response)
    
    print("... done")
