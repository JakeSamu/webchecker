from bs4 import BeautifulSoup
import os
#ToDo: converts burp-copy&paste to an http-request-format and the response to the correct burp-output.
#ToDo: only first part, second part is already done, just has to be moved here.
global httpvers


def removeemptylines(text):
    if text.count("\n\n") > 1:
        text = text.replace("\n\n", "\n")
    return text

def burp_get_header(text):
    text = text.split("\n\n")[0]
    text = text.split("\n", 1)[1] #remove the first line which states the method
    header = {}
    for line in text.splitlines():
        tmp = line.split("\n")[0]
        header[tmp.split(": ")[0]] = tmp.split(": ")[1]
    return header

def burp_get_body(text):
    out = ""
    try: out = text.split("\n\n")[1]
    finally: return out

def burp_to_request(burpfile):
    with open(burpfile, "rt") as f:
        text = removeemptylines(f.read())
        method = text.split(" ", 1)[0]
        header = burp_get_header(text)
        body = burp_get_body(text)
        return (method, header, body)

def burp_to_response():
    print("\'burp_to_response\' was not needed yet, so does not exists")

def readable_headers(r):
    header = ""
    for h,v in r.headers.items():
        if (h == "Set-Cookie"):
            tmp = h + ": " + v + "\n"
            for cookie in r.cookies:
                tmp = tmp.replace(", " + cookie.name + "=", "\nSet-Cookie: " + cookie.name + "=")
            header += tmp
        else: header += h + ": " + v + "\n"

    return header

def request_to_readable(request):
    path = "/" + str(request.url).split("/")[3]
    firsthead = str(request).split("[")[1].split("]")[0] + " " + path + " " + httpvers + "\n"
    reqbody = ''
    if (request.body):
        reqbody = "\n\n" + str(request.body)
    return firsthead + readable_headers(request) + reqbody

def response_to_readable(response):
    firsthead = httpvers + " " + str(response.status_code) + " " + response.reason + "\n"
    soup = BeautifulSoup(str(response.text), 'html.parser').prettify()
    # ToDo: would it be better, if the indent is setable to 2 or 3 instead of 1?
    nlines = min(7, len(soup.splitlines()))
    return firsthead + readable_headers(response) + "\n" + os.linesep.join(str(soup).split(os.linesep)[:nlines])
