debug = False #set to True if you want to have debugging/verbose comments
output = True # set to false if you do not want to save the output

proxy=False #set to True, if you want to use the proxy defiend in proxyip
proxies = { #set to the IPs of the proxy if you want to use it
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080'
}
vfy=True #check for proxy certificate

# relative path to the folder where the output is going to be written. Remember: it overwrites files with same name!
relative = True # Set to false, if you always want to go to a specific absolute path
relativepath = ""
absolutepath = ""

# Default parameters for the web calls
method = "GET"
file = ""
url = ""
header = "{}"
body = ""
tls = True
port = 443

#No change yet supported
redirect = False
interactive = False
hostname = 'github.JakeSamu.StandardWebFindings'
