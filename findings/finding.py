import findings
import config
import template
import pathlib

def create_finding(type, text, code, suffix=""):
    print(" found " + type + " ...", end='')
    filename = type
    if (suffix != ""): filename += "." + suffix

    if (config.relative): path = str(pathlib.Path().absolute()) + "/" + config.relativepath
    else: path = config.absolutepath

    if (config.debug): print("Path = " + path)

    if config.output:
        with open(path + "/" + filename, "w") as f:
            f.write(template.template_start + text + "\n\n" + code + template.template_end)

def check_for_findings(request, response):
    print("Starting the web calls and checking for findings ...")
    #Call every finding-script here
    findings.cookies.check_cookies(request, response)
    findings.hsts.check_hsts(request, response)
    findings.infodisc.info_disc(request, response)
    findings.cors.check_cors(request, response)
    findings.arbitraryhost.check_hostheader(request, response)
    print("... done")
