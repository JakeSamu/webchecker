config = {}
config['debug'] = False  # set to True if you want to have debugging/verbose comments
config['output'] = True  # set to false if you do not want to save the output

config['proxy'] = False  # set to True, if you want to use the proxy defiend in proxyip
config['proxies'] = {  # set to the IPs of the proxy if you want to use it
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080'
}
config['vfy'] = True  # check for proxy certificate

# relative path to the folder where the output is going to be written. Remember: it overwrites files with same name!
config['relative'] = True  # Set to false, if you always want to go to a specific absolute path
config['relativepath'] = ""
config['absolutepath'] = ""

# Default parameters for the web calls
config['method'] = "GET"
config['file'] = ""
config['url'] = ""
config['hostname'] = ""
config['header'] = "{}"
config['body'] = ""
config['tls'] = True
config['port'] = 443
config['redirect'] = False
config['hostname-test'] = 'github.JakeSamu.StandardWebFindings'

# No change yet supported
config['interactive'] = False
