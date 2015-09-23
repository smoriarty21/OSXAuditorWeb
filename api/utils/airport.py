import os
import core
import error

ROOT_PATH = '/'

def ParseAirportPrefs():
    global HTML_LOG_FILE
    AirportPrefPlist = False
    NbAirportPrefs = 0
    rmbr_networks = []

    AirportPrefPlistPath = os.path.join(ROOT_PATH, "Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist")
    AirportPrefPlist = core.UniversalReadPlist(AirportPrefPlistPath)

    if AirportPrefPlist:
        if "RememberedNetworks" in AirportPrefPlist:
            RememberedNetworks = AirportPrefPlist["RememberedNetworks"]

            for RememberedNetwork in RememberedNetworks:
                network = {}
                if OSX_VERSION["MinorVersion"] <= 8: # 10.8 or lower
                    Geolocation = "N/A (Geolocation disabled)"
                    if GEOLOCATE_WIFI_AP:
                        Geolocation = GeomenaApiLocation(RememberedNetwork["CachedScanRecord"]["BSSID"])

                        network['ssid'] = RememberedNetwork["SSIDString"].decode("utf-8")
                        network['rssi'] = str(RememberedNetwork["CachedScanRecord"]["RSSI"])
                        network['bssid'] = RememberedNetwork["CachedScanRecord"]["BSSID"]
                        network['last_connected'] = str(RememberedNetwork["LastConnected"])
                        network['security_type'] = str(RememberedNetwork["SecurityType"])
                        network['location'] = Geolocation
                elif OSX_VERSION["MinorVersion"] >= 9: # 10.9 or higher
                    Geolocation = "N/A (Geolocation disabled)"

                    if GEOLOCATE_WIFI_AP:
                        Geolocation = GeomenaApiLocation(RememberedNetwork["SSID"])

                    network['ssid'] = RememberedNetwork["SSIDString"].decode("utf-8")
                    network['closed'] = str(RememberedNetwork["Closed"])
                    network['security_type'] = str(RememberedNetwork["SecurityType"])
                    network['location'] = Geolocation
                else:
                    throw = {
                        'ERROR': 'No Airport Preferences File Detected'
                    }
                    return throw

                NbAirportPrefs += 1
                rmbr_networks.append(network)
        if len(rmbr_networks):
            return rmbr_networks
        else:
            return error.AIRPORT_EMPTY_ERROR
    else:
        return error.AIRPORT_EMPTY_ERROR