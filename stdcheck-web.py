import os
import findings.finding
import config
import json
import argparse
import pathlib
from main import burpconverter, webcall
import urllib3


# Allow several arguments besides True and False
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def start(response):
    burpconverter.httpvers = "HTTP/" + str(response.raw.version)[:1] + "." + str(response.raw.version)[
                                                                             1:]  # workaround for showing the http-version
    findings.finding.check_for_findings(response.request, response)


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Ignore HTTPS warnings while using a proxy

    parser = argparse.ArgumentParser(description="Stdcheck-Web")

    optional = parser._action_groups.pop()
    required = parser.add_argument_group("exactly one of these arguments")

    required.add_argument('-u', '--url', type=str, default=config.config['url'], help='Standard webcall to given url')
    required.add_argument('-f', '--file', type=str, default=config.config['file'],
                          help='Use a file that contains a copy of burp request')

    optional.add_argument('-v', '--verbose', type=str2bool, default=config.config['debug'], help='Detailed output', nargs='?',
                          const=True)
    optional.add_argument('-dr', '--dir', type=str, default=config.config['relativepath'],
                          help='Define the directory which is used to save all the files into via relative path.\nDefault is the current directory.')
    optional.add_argument('-da', type=str, default=config.config['absolutepath'],
                          help='Define the directory per absolute path instead of relative path.')
    optional.add_argument('-n', '--no-output', type=str2bool, default=config.config['output'],
                          help='Set to true if files shall be generated.', nargs='?', const=True)
    optional.add_argument('-r', '--redirect', type=str2bool, default=config.config['redirect'],
                          help='Use this to follow redirections.', nargs='?', const=True)
    optional.add_argument('-m', '--method', type=str, default=config.config['method'],
                          help='Only works with usage of url, defines the method.\nDefault is GET')
    optional.add_argument('--header', type=json.loads, default=config.config['header'],
                          help='Add the header of the request as a dictionary.\nOnly compatible with -u.')
    optional.add_argument('--body', type=str, default=config.config['body'],
                          help='Define the body of the request as a string.\nOnly compatible with -u.')
    optional.add_argument('-p', '--port', type=str, default=config.config['port'],
                          help='Only works with usage of -f, use this if the standard port is not in use (443 for https, 80 for http)')
    optional.add_argument('--tls', type=str2bool, default=config.config['tls'],
                          help='Set to False if endpoint is not using TLS.\nDefault is ' + str(
                              config.config['tls']) + '\nOnly compatible with -f')
    optional.add_argument('--proxy-tls', type=str2bool, default=config.config['vfy'],
                          help='Use this to check for the proxy certificate.', nargs='?', const=True)
    optional.add_argument('--proxy', type=str2bool, default=config.config['proxy'],
                          help='Proxy IP is defined in the config.config[\'file\']. This parameter is just to turn it on or off.',
                          nargs='?', const=True)
    parser._action_groups.append(optional)

    # Implement from top to down in this order
    soon = parser.add_argument_group('Coming soon')
    soon.add_argument('-i', '--interactive', type=str2bool, default=config.config['interactive'],
                      help='(Idea to have an interactive mode to check every finding and click at every point to use it or not.)')

    args = parser.parse_args()

    # Those that are only flags without values
    config.config['debug'] = args.verbose
    config.config['output'] = args.no_output
    config.config['redirect'] = args.redirect
    # Proxy
    config.config['proxy'] = args.proxy
    config.config['vfy'] = args.proxy_tls

    # File
    config.config['file'] = args.file
    use_file = True if (config.config['file'] != "") else False
    # URL
    config.config['url'] = args.url
    if (config.config['url'] != "" and use_file):
        print("You have given both, an url and a file. Please only use one of both.")
        exit(0)
    # Path
    config.config['relative'] = True if (config.config['relativepath'] != args.dir) else False
    config.config['relativepath'] = args.dir
    config.config['absolutepath'] = args.da

    # TLS and ports
    config.config['tls'] = args.tls
    if (args.port != config.config['port']):
        config.config['port'] = args.port
    else:
        if (config.config['tls']):
            config.config['port'] = 443
        else:
            config.config['port'] = 80

    # Request-config.config['ration']
    config.config['header'] = args.header
    config.config['body'] = args.body
    config.config['method'] = args.method

    # Check if given directory exists
    if config.config['relative']:
        path = pathlib.Path(config.config['relativepath'])
    else:
        path = pathlib.Path(config.config['absolutepath'])
    if not pathlib.Path.exists(path):
        create = str2bool(input("Your given directory does not exists. Do you want to create it? (Y/n)"))
        if create:
            os.mkdir(path)
        else:
            exit(1)

    if (config.config['file'] == "" and config.config['url'] == ""):
        print("Neither an url nor a file was given.")
        exit(0)

    # Prepare webcall and start it
    webcall.check_proxy()
    if (use_file):
        webcall.set_file(config.config['file'])
    else:
        webcall.set_url(config.config['url'])
    response = webcall.call()
    start(response)


main()
