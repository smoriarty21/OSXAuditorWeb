import os
import log
import sqlite3

ROOT_PATH = '/'

def ParseQuarantines():
    all_data = []
    log.PrintAndLog(u"Quarantines", "SECTION")

    for User in os.listdir(os.path.join(ROOT_PATH, "Users/")):
        print User
        if User[0] != ".":
            log.PrintAndLog(User.decode("utf-8") +"\'s quarantine", "SUBSECTION")
            DbPathV2 = os.path.join(ROOT_PATH, "Users", User, "Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2")        # OS X >= 10.7
            DbPathV1 = os.path.join(ROOT_PATH, "Users", User, "Library/Preferences/com.apple.LaunchServices.QuarantineEvents")          # OS X <= 10.6
            if os.path.isfile(DbPathV2):
                DbPath = DbPathV2
            elif os.path.isfile(DbPathV1):
                DbPath = DbPathV1
            else:
                log.PrintAndLog(u"No quarantined files for user " + User.decode("utf-8") + u"\n", "INFO")
                continue
            DbConnection = sqlite3.connect(DbPath)
            DbCursor = DbConnection.cursor()
            LSQuarantineEvents = DbCursor.execute("SELECT * from LSQuarantineEvent")
            for LSQuarantineEvent in LSQuarantineEvents:
                JointLSQuarantineEvent = u""
                for Q in LSQuarantineEvent:
                    JointLSQuarantineEvent += u";" + unicode(Q)
                    data = JointLSQuarantineEvent[1:] + u"\n".decode("utf-8")
                    all_data.append(data)
                log.PrintAndLog(JointLSQuarantineEvent[1:] + u"\n".decode("utf-8"), "INFO")
            DbConnection.close()

    return all_data