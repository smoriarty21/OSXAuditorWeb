import os
from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

from utils import user
from utils import kernel
from utils import header
from utils import airport
from utils import startup
from utils import browsers
from utils import downloads
from utils import event_logs
from utils import quarantines
from utils import applications

ROOT_PATH = '/'

app = FlaskAPI(__name__)

@app.route("/getheader", methods=['POST'])
def get_header():
    if request.method == 'POST':
        data = header.generate_header()

    return data

@app.route("/getkernerext", methods=['POST'])
def get_kerner_extensions():
    if request.method == 'POST':
        HASH_DATA = kernel.ParsePackagesDir(os.path.join(ROOT_PATH, "System/Library/Extensions/"))

    return HASH_DATA

@app.route("/getstartup", methods=['POST'])
def get_startup():
    if request.method == 'POST':
        print "Im doing shit"
        data = startup.ParseStartup()

    return data

@app.route("/getapplications", methods=['POST'])
def get_applications():
    if request.method == 'POST':
        data = applications.ParseInstalledApps()

    return data

@app.route("/getquarantines", methods=['POST'])
def get_quarantines():
    if request.method == 'POST':
        data = quarantines.ParseQuarantines()

    return data

@app.route("/getdownloads", methods=['POST'])
def get_downloads():
    if request.method == 'POST':
        data = downloads.ParseDownloads()

    return data

@app.route("/getbrowsers", methods=['POST'])
def get_browsers():
    if request.method == 'POST':
        data = browsers.ParseBrowsers()

    return data

@app.route("/getairportprefs", methods=['POST'])
def get_airport_prefs():
    if request.method == 'POST':
        data = airport.ParseAirportPrefs()

    return data

@app.route("/getuseraccounts", methods=['POST'])
def get_user_acts():
    if request.method == 'POST':
        data = user.ParseUsersAccounts()

    return data

@app.route("/geteventlogs", methods=['POST'])
def get_event_logs():
    if request.method == 'POST':
        data = event_logs.ParseEventLogs()

    return data

if __name__ == "__main__":
    app.run(debug=True)