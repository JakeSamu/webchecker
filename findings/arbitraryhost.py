import config
from findings import finding

# ToDo: assume everytime that host header is set. then call another time and compare status response and body
from main import webcall

text = "Die folgenden HTTP Requests mitsamt Response zeigen auf, dass trotz unterschiedlichem Host Header, die Response die gleiche ist. Auch wenn keine direkte Möglichkeit gefunden wurde diese Schwachstelle auszunutzen, so ist es empfehelenswert, den Host Header zu überprüfen."


# This checks if the length is the same and if at least 90% of those lines are the same
def linewise_compare(string1, string2, percent=0.9):
    split1 = string1.split("\n")
    split2 = string2.split("\n")
    count = maxcount = 0
    if (len(split1) != len(split2)):
        return 0
    else:
        for i in range(len(split1)):
            if split1[i] == split2[i]:
                count += 1
            maxcount += 1
        if (count >= maxcount * percent):
            return True
        else:
            return False


def compare_body(body1, body2):
    return linewise_compare(body1, body2)


def compare(response1, response2):
    return compare_body(response1.text, response2.text)


def check_hostheader(request, response):
    print("... checking for arbitrary host header ...", end='')

    addheader = {'Host': config.hostname}
    response2 = webcall.call(addheader)
    highlight = ["Host: "]

    if compare(response, response2):
        code1 = format.create_both(request, response, highlight, [""], "Request 1:", "Response 1:")
        code2 = format.create_both(response2.request, response2, highlight, [""], "Request 2:", "Response 2:")
        finding.create_finding("arbitraryhost", text, code1 + code2)

    print("")
