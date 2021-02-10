import template
from main import format
from findings import finding

text_httponly_plural = "In dem folgenden HTTP-Request mitsamt Response wird an der gelb markierten Stelle gezeigt, dass das Attribut " + template.cursive_start + "HttpOnly" + template.cursive_end + " nicht verwendet wird. Die davon betroffenen Cookies sind: "
text_httponly_singular = "In dem folgenden HTTP-Request mitsamt Response wird an der gelb markierten Stelle gezeigt, dass das Attribut " + template.cursive_start + "HttpOnly" + template.cursive_end + " nicht verwendet wird. Das davon betroffene Cookie ist: "
text_secure_plural = "In dem folgenden HTTP-Request mitsamt Response wird an der gelb markierten Stelle gezeigt, dass das Attribut " + template.cursive_start + "secure" + template.cursive_end + " nicht verwendet wird. Die davon betroffenen Cookies sind: "
text_secure_singular = "In dem folgenden HTTP-Request mitsamt Response wird an der gelb markierten Stelle gezeigt, dass das Attribut " + template.cursive_start + "secure" + template.cursive_end + " nicht verwendet wird. Das davon betroffene Cookie ist: "

#ToDo: interactive-mode, which allows to say which cookie should be considered as what

def has_http_only(cookie):
    extra_args = cookie.__dict__.get("_rest")
    if extra_args:
        for key in extra_args.keys():
            if key.lower() == "httponly":
                return True
    return False

def cookiefinding(request, response, cookiename, type, text):
    # ToDo: ist es möglich format.create_both zu extrahieren? besser wäre wahrscheinlich soetwas wie "1" oder "2" als Übergabe ... bis auf bei arbitrary host header ...
    code = format.create_both(request, response, ["Set-Cookie: " + cookiename + "="])
    finding.create_finding(type, text, code, str(cookiename))

def all_cookie_findings(request, response, type, text, cookienames):
    highlightings = []
    for name in cookienames:
        highlightings.append("Set-Cookie: " + name + "=")
    code = format.create_both(request, response, highlightings)
    finding.create_finding(type, text, code, "all")

def check_cookies(request, response):
    print("... checking cookies ...", end='')

    nothttponlycookies = []
    cookienames_http = ""
    notsecurecookies = []
    cookienames_secure = ""
    for cookie in response.cookies:
        if not has_http_only(cookie):
            nothttponlycookies.append(cookie.name)
            cookienames_http += cookie.name + ", "
            #ToDo: uncomment the next line and have a parameter to check, if every cookie should have their own file.
            #cookiefinding(request, response, cookie.name, "cookie.httponly", text_httponly)
        if not cookie.secure:
            notsecurecookies.append(cookie.name)
            cookienames_secure += cookie.name + ", "
            #ToDo: uncomment the next line and have a parameter to check, if every cookie should have their own file.
            #cookiefinding(request, response, cookie.name, "cookie.secureflag", text_secure)

    if (len(nothttponlycookies) > 0):
        if (len(nothttponlycookies) == 1):
            text_httponly = text_httponly_singular
        else:
            text_httponly = text_httponly_plural
        fulltext = text_httponly + template.cursive_start + cookienames_http[:-2] + template.cursive_end
        all_cookie_findings(request, response, "cookie.httponly", fulltext, nothttponlycookies)

    if (len(notsecurecookies) > 0):
        if (len(notsecurecookies) == 1):
            text_secure = text_secure_singular
        else:
            text_secure = text_secure_plural
        fulltext = text_secure + template.cursive_start + cookienames_secure[:-2] + template.cursive_end
        all_cookie_findings(request, response, "cookie.secureflag", fulltext, notsecurecookies)

    print("")
