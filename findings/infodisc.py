from main import *
from findings import finding
from main import format
import findings.lists.infodisclist
import template

#ToDo: check if something is in body:
# keycloak/auth/resources/%versionsnummer/admin/keycloak
# Apache Tomcat/


#ToDo: Sammle alle Header wie sie nicht gesetzt sein sollten, beispielsweise falsche Konfig für XSS oder X-Content-Type-Options


text = "In dem folgenden HTTP-Request mitsamt Response sind an den gelb markierten Stellen Informationspreisgaben zu erkennen. Diese sind: "

def info_disc_headers(headerdict):
    output = {}
    list = findings.lists.infodisclist.headers
    for hk,hv in headerdict.items():
        if (hk in list):
            output[hk] = hv
    return output

def info_disc_body(body):
    #This is still buggy and not well written
    output = {}
    bodydict = findings.lists.infodisclist.body
    for tk,tv in bodydict.items():
        if all(parts in body for parts in tv):
            output[tv[0]] = tk
    return output

def info_disc(request, response):
    print("... checking obvious information disclosures ...", end='')

    headers = info_disc_headers(response.headers)
    body = info_disc_body(response.text)

    if (len(headers) > 0):
        tmp = ""
        for key in headers:
            tmp += headers[key] + ", "
        for key in body:
            tmp += body[key] + ", "
        tmp = tmp[:-2]
        tmp = text + template.cursive_start + tmp + template.cursive_end

        code = format.create_both(request, response, headers.keys())
        #ToDo: fix that, it currently deletes nearly everything -.-
        #code = format.highlight_ifall_inline(code, body.keys())
        #ToDo: for every body finding a different file!
        finding.create_finding("infodisc", tmp, code)
    print("")
