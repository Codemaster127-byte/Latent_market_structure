import webbrowser
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect

API_KEY    = "hznezic9e4qy291u"
API_SECRET = "q0q7i4mxbnet8677xa8h2zw0kaz7e59n"
TOKEN_FILE = "token.json"

captured = {}

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        captured["request_token"] = params["request_token"][0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Login successful! You can close this tab.")

    def log_message(self, *args):
        pass


def fresh_login(kite):
    webbrowser.open(kite.login_url())
    HTTPServer(("127.0.0.1", 5000), CallbackHandler).handle_request()
    session = kite.generate_session(captured["request_token"], api_secret=API_SECRET)
    json.dump({"access_token": session["access_token"]}, open(TOKEN_FILE, "w"))
    return session["access_token"]


def initiation():
    kite = KiteConnect(api_key=API_KEY)

    # Trigger fresh login on any token error
    kite.set_session_expiry_hook(lambda: fresh_login(kite))

    # Load saved token if exists, otherwise login
    if os.path.exists(TOKEN_FILE):
        data = json.load(open(TOKEN_FILE))
        kite.set_access_token(data["access_token"])
    else:
        fresh_login(kite)

    print("Done!", kite.profile()["user_name"])
    return kite