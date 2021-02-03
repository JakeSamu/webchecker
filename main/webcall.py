import requests
from main import burpconverter
import config

#todo: tls, port, method
def set_url(url):
    config.config['url'] = url
    config.config['file'] = ""

def set_file(file):
    config.config['file'] = file
    (urlpath, config.config['method'], config.config['header'], config.config['body']) = burpconverter.burp_to_request(file)

    # ToDo: this assumes port 443, change it corresponding to input, eventually plaintext?
    if (config.config['tls']):
        url = "https://"
        if (config.config['port'] != 443): url += ":" + config.config['port']
    else:
        url = "http://"
        if (config.config['port'] != 80): url += ":" + config.config['port']
    config.config['url'] = url + config.config['header']["Host"]
    if config.config['url'][-1] == "/": config.config['url'] = config.config['url'][:-1] + urlpath
    else: config.config['url'] += urlpath


def check_proxy(proxies=config.config['proxies']):
    #ToDo: check if certificate is present or given
    if (config.config['proxy']):
        config.config['vfy'] = False
        config.config['proxies'] = proxies
    else:
        config.config['vfy'] = True
        config.config['proxies'] = ""

#ToDO: exception handling if url is wrong, no internet-connection, or if file does not exist

#ToDo: make it compatible with input
def call(addheader={}):
    headers = config.config['header'].copy()
    headers.update(addheader)

    response = requests.request(config.config['method'], config.config['url'], headers=headers, data=config.config['body'],
                                proxies=config.config['proxies'], verify=config.config['vfy'], allow_redirects=config.config['redirect'])
    return response
