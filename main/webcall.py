import requests
from main import burpconverter
import config

#todo: tls, port, method
def set_url(url):
    config.url = url
    config.file = ""

def set_file(file):
    config.file = file
    (urlpath, config.method, config.header, config.body) = burpconverter.burp_to_request(file)

    # ToDo: this assumes port 443, change it corresponding to input, eventually plaintext?
    if (config.tls):
        url = "https://"
        if (config.port != 443): url += ":" + config.port
    else:
        url = "http://"
        if (config.port != 80): url += ":" + config.port
    config.url = url + config.header["Host"]
    if config.url[-1] == "/": config.url = config.url[:-1] + urlpath
    else: config.url += urlpath


def check_proxy(proxies=config.proxies):
    #ToDo: check if certificate is present or given
    if (config.proxy):
        config.vfy = False
        config.proxies = proxies
    else:
        config.vfy = True
        config.proxies = ""

#ToDO: exception handling if url is wrong, no internet-connection, or if file does not exist

#ToDo: make it compatible with input
def call(addheader={}):
    headers = config.header.copy()
    headers.update(addheader)

    response = requests.request(config.method, config.url, headers=headers, data=config.body,
                                proxies=config.proxies, verify=config.vfy, allow_redirects=config.redirect)
    return response
