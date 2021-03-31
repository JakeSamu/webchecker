import template
from main import format
from findings import finding

text = "In dem folgenden HTTP-Request mitsamt Response wird aufgezeigt, dass der Header " + template.cursive_start + "X-XSS-Protection" + template.cursive_end + " explizit so gesetzt ist, dass der XSS-Filter deaktiviert ist."

def check_xssfilter(request, response):
    print("... checking usage of XSS-filter ...", end='')

    if 'X-XSS-Protection' in response.headers:
    	if (response.headers.get("X-XSS-Protection") == 0):
            code = format.create_both(request, response, "X-XSS-Protection: 0")
            finding.create_finding("xss-filter-disabled", text, code)

    print("")
