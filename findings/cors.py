#Access-Control-Allow-Origin: *
#Access-Control-Allow-Credentials: true

# ToDo: neuer Call mit gesetzter Origin um zu überprüfen, ob nicht * gesetzt ist, sondern einfach die Origin verwendet wird.
# Versuche mit "Origin: https://www.tuv.com" den Access-Control-Allow-Origin auf https://www.tuv.com zu setzen.

def check_headers(headers):
    if (headers.get("Access-Control-Allow-Origin") == "*"):
        print("Arbitrary origin allowed.")
    if (headers.get("Access-Control-Allow-Credentials") == "true"):
        print("CORS-Credentials allowed")

def check_cors(request, response):
    check_headers(response.headers)