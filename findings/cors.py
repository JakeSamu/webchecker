import config
from main import *
from findings import finding
import template


corsheader = "Access-Control-Allow-Origin"
credheader = "Access-Control-Allow-Credentials"
dependencyheader = config.config['hostname']

text_origin1 = "In dem folgenden HTTP-Request mitsamt Response ist zu sehen, dass der Header "+template.cursive_start+corsheader+template.cursive_end+" ein Wildcard enthält und somit beliebige Origins erlaubt."
text_origin2 = "In dem folgenden HTTP-Request mitsamt Response ist zu sehen, dass der Header "+template.cursive_start+corsheader+template.cursive_end+" denselben Wert wie in der Response überträgt und somit beliebige Origins erlaubt."
text_creds = " Zusätzlich ist zu sehen, dass der Header "+template.cursive_start+credheader+template.cursive_end+" auf "+template.cursive_start+"true"+template.cursive_end+" gesetzt wird."


def check_origin(headers, hostname="*"):
    if (headers.get("Access-Control-Allow-Origin") == hostname):
        return True
    else: return False

def check_creds(headers):
    if (headers.get("Access-Control-Allow-Credentials") == "true"):
        return True
    else: return False

def check_cors(request, response):
    print("... checking CORS policy ...", end='')

    check_creds(response.headers)

    if 'Access-Control-Allow-Origin' in response.headers:
        if check_origin(response.headers):
            text = text_origin1
            highlight = [corsheader]
            if check_creds(response.headers):
                text += text_creds
                highlight.append(credheader)
            code = format.create_both(request, response, highlight)
            finding.create_finding("cors", text, code)
        else:
            #Check if origin depends on request header.
            addheader = {'Origin': dependencyheader, 'Referer': dependencyheader}
            response2 = webcall.call(addheader)

            text = text_origin2
            highlight = [dependencyheader]
            if check_origin(response2.headers, dependencyheader):
                if check_creds(response2.headers):
                    text += text_creds
                    highlight.append(credheader)
                code = format.create_both(response2.request, response2, highlight)
                finding.create_finding("cors", text, code)

    print("")
