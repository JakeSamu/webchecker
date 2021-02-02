import template
from main import format
from findings import finding
#ToDo: to remove that part, make it such that the value is returned instead of called ... would be simpler to handle ...

text = "In dem folgenden HTTP-Request mitsamt Response wird aufgezeigt, dass der Header " + template.cursive_start + "Strict-Transport-Security" + template.cursive_end + " nicht gesetzt wird."

def check_hsts(request, response):
    print("... checking usage of HSTS ...", end='')

    if "Strict-Transport-Security" not in response.headers:
        code = format.create_both(request, response)
        finding.create_finding("hsts", text, code)

    print("")
