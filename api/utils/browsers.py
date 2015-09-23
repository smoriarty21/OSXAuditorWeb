import os
import log
import core
import sqlite3
import binascii

ROOT_PATH = '/'

firefox_data = []
chrome_data = []
safari_data = {}

browsers = []

def DumpSQLiteDb(SQLiteDbPath):
    all_rows = []
    if os.path.isfile(SQLiteDbPath):
        try:
            DbConnection = sqlite3.connect(SQLiteDbPath)
            DbCursor = DbConnection.cursor()
            DbCursor.execute("SELECT * from sqlite_master WHERE type = 'table'")
            Tables =  DbCursor.fetchall()
            for Table in Tables:
                DbCursor.execute("SELECT * from " + Table[2])
                Rows = DbCursor.fetchall()
                if len(Rows) == 0:
                    log.PrintAndLog(u"Table " + Table[2].decode("utf-8") + u" is empty", "INFO")
                else:
                    for Row in Rows:
                        all_rows.append(str(Row).decode("utf-8"))
                DbConnection.close()
        except Exception as e:
            log.PrintAndLog(u"Error with " + SQLiteDbPath.decode("utf-8") + u": " + str(e.args).decode("utf-8"), "ERROR")
    else:
        log.PrintAndLog(SQLiteDbPath.decode("utf-8") + u" not found\n", "ERROR")

    return all_rows

def ParseFirefoxProfile(User, Profile, data):
    # Cookies
    data['cookies'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "cookies.sqlite"))

    # Downloads
    data['downloads'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "downloads.sqlite"))
    
    # Form History
    data['form-history'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "formhistory.sqlite"))
    
    # Places
    data['places'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "places.sqlite"))
    
    # Signons
    data['signons'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "signons.sqlite"))

    # Permissions
    data['permissions'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "permissions.sqlite"))
    
    # Addons
    data['addons'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "addons.sqlite"))
    
    # Extensions
    data['extensions'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "extensions.sqlite"))
    
    # Content Preferences
    data['content-preferences'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "content-prefs.sqlite"))
    
    # Health Reports
    data['health-report'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "healthreport.sqlite"))
    
    # App Store
    data['web-apps-store'] = DumpSQLiteDb(os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles/", Profile, "webappsstore.sqlite"))

    return data

def ParseFirefox():
    for User in os.listdir(os.path.join(ROOT_PATH, "Users")):
        tmp_ff_data = {}
        UserFFProfilePath = os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Firefox/Profiles")      

        if User[0] != "." and os.path.isdir(UserFFProfilePath):
            tmp_ff_data['user'] = User
            tmp_ff_data['user_profile_path'] = UserFFProfilePath

            for Profile in os.listdir(UserFFProfilePath):
                if Profile[0] != "." and os.path.isdir(os.path.join(UserFFProfilePath,  Profile)):
                    tmp_ff_data = ParseFirefoxProfile(User, Profile, tmp_ff_data)
            firefox_data.append(tmp_ff_data)

    ff_data_dict = {
        'firefox': firefox_data
    }

    browsers.append(ff_data_dict)

def ParseSafariProfile(User, Path):
    HistoryPlist = False
    DownloadsPlist = False
    NbFiles = 0

    DownloadsPlistPath = os.path.join(Path, "Downloads.plist")
    DownloadsPlist = core.UniversalReadPlist(DownloadsPlistPath)

    if DownloadsPlist:
        if "DownloadHistory" in DownloadsPlist:
            downloads = []
            Downloads = DownloadsPlist["DownloadHistory"]
            for DL in Downloads:
                download = {}
                download['DownloadEntryURL'] = DL["DownloadEntryURL"].decode("utf-8")
                download['DownloadEntryPath'] = DL["DownloadEntryPath"].decode("utf-8")
                download['DownloadEntryIdentifier'] = DL["DownloadEntryIdentifier"].decode("utf-8")
                downloads.append(download)
            safari_data['downloads'] = downloads

    HistoryPlistPath = os.path.join(Path, "History.plist")

    HistoryPlist = core.UniversalReadPlist(HistoryPlistPath)

    if HistoryPlist:
        if "WebHistoryDates" in HistoryPlist:
            History =  HistoryPlist["WebHistoryDates"]
            for H in History:
                HStr = u""
                if "title" in H:
                    HStr += unicode(H["title"]) + u" - "
                if "diplayTitle" in H:
                    HStr += unicode(H["diplayTitle"]) + u" - "
                HStr += unicode(H[""]) + u"\n"

    TopSitesPlistPath = os.path.join(Path, "TopSites.plist")
    top_sites = {}
    top_sites['user'] = User
    top_sites['p_list_dir'] = TopSitesPlistPath

    TopSitesPlist = core.UniversalReadPlist(TopSitesPlistPath)

    if TopSitesPlist:
        if "TopSites" in TopSitesPlist:
            TopSites =  TopSitesPlist["TopSites"]
            site_list = []
            
            for T in TopSites:
                ts = {}
                ts['title'] = unicode(T['TopSiteTitle'])
                ts['url'] = unicode(T['TopSiteURLString'])
                site_list.append(ts)
            safari_data['top_sites'] = site_list



    log.PrintAndLog(User + u"\'s Safari LastSession", "SUBSECTION")
    LastSessionPlistPath = os.path.join(Path, "LastSession.plist")

    log.PrintAndLog(LastSessionPlistPath.decode("utf-8"), "DEBUG")
    LastSessionPlist = core.UniversalReadPlist(LastSessionPlistPath)

    if "SessionWindows" in LastSessionPlist:
        LastSession = LastSessionPlist["SessionWindows"][0]["TabStates"][0]
        #safari_data['last_session'] = LastSession
        log.PrintAndLog(LastSession["TabURL"].decode("utf-8") + u" - " + binascii.hexlify(LastSession["SessionState"]).decode("hex").decode("utf-8", "ignore"), "INFO")



    log.PrintAndLog(User + u"\'s Safari databases", "SUBSECTION")
    for Db in os.listdir(os.path.join(Path, "Databases")):
        DumpSQLiteDb(os.path.join(Path, "Databases", Db))
        NbFiles += 1

    if  NbFiles == 0:
        log.PrintAndLog(User + u"\'s Safari databases is empty", "INFO")

    NbFile = 0

    log.PrintAndLog(User + u"\'s Safari LocalStorage", "SUBSECTION")
    for Db in os.listdir(os.path.join(Path, "LocalStorage")):
        DumpSQLiteDb(os.path.join(Path, "LocalStorage", Db))
        NbFiles += 1

    if  NbFiles == 0:
        log.PrintAndLog(User + u"\'s Safari LocalStorage is empty", "INFO")

    #return safari_data
    sf_data_dict = {
        'safari': safari_data
    }

    browsers.append(sf_data_dict)

def ParseSafari():
    for User in os.listdir(os.path.join(ROOT_PATH, "Users")):
        UserSafariProfilePath = os.path.join(ROOT_PATH, "Users", User, "Library/Safari")
        if User[0] != "." and os.path.isdir(UserSafariProfilePath):
            data = ParseSafariProfile(User, UserSafariProfilePath)
            return data

def ParseChromeProfile(User, Path):
    NbFiles = 0

    log.PrintAndLog(User + u"\'s Chrome profile", "SUBSECTION")

    log.PrintAndLog(User + u"\'s Chrome history", "SUBSECTION")
    chrome_data.append(DumpSQLiteDb(os.path.join(Path, "History")))

    log.PrintAndLog(User + u"\'s Chrome archived history", "SUBSECTION")
    chrome_data.append(DumpSQLiteDb(os.path.join(Path, "Archived History")))

    log.PrintAndLog(User + u"\'s Chrome cookies", "SUBSECTION")
    chrome_data.append(DumpSQLiteDb(os.path.join(Path, "Cookies")))

    log.PrintAndLog(User + u"\'s Chrome login data", "SUBSECTION")
    chrome_data.append(DumpSQLiteDb(os.path.join(Path, "Login Data")))

    log.PrintAndLog(User + u"\'s Chrome Top Sites", "SUBSECTION")
    chrome_data.append(DumpSQLiteDb(os.path.join(Path, "Top Sites")))

    log.PrintAndLog(User + u"\'s Chrome web data", "SUBSECTION")
    chrome_data.append(DumpSQLiteDb(os.path.join(Path, "Web Data")))

    log.PrintAndLog(User + u"\'s Chrome databases", "SUBSECTION")
    for Db in os.listdir(os.path.join(Path, "databases")):
        CurrentDbPath = os.path.join(Path, "databases", Db)
        if CurrentDbPath[-8:] != "-journal" and not os.path.isdir(CurrentDbPath):
            chrome_data.append(DumpSQLiteDb(CurrentDbPath))
        NbFiles += 1

    if  NbFiles == 0:
        log.PrintAndLog(User + u"\'s Chrome databases is empty", "INFO")

    NbFiles = 0

    log.PrintAndLog(User + u"\'s Chrome LocalStorage", "SUBSECTION")
    for Db in os.listdir(os.path.join(Path, "Local Storage")):
        CurrentDbPath = os.path.join(Path, "Local Storage", Db)
        if CurrentDbPath[-8:] != "-journal" and not os.path.isdir(CurrentDbPath):
            chrome_data.append(DumpSQLiteDb(CurrentDbPath))
        NbFiles += 1

    if  NbFiles == 0:
        log.PrintAndLog(User + u"\'s Chrome LocalStorage is empty", "INFO")

def ParseChrome():
    for User in os.listdir(os.path.join(ROOT_PATH, "Users")):
        chrome_tmp = {}
        UsersChromePath = os.path.join(ROOT_PATH, "Users", User, "Library/Application Support/Google/Chrome/Default")
        ParseChromeProfile(User, UsersChromePath)

    #return chrome_data

def ParseBrowsers():
    ParseSafari()
    ParseFirefox()

    # TODO: Chrome path has changed.  Need to add support
    #       for both old and new locations for chrome
    #ParseChrome()

    return browsers