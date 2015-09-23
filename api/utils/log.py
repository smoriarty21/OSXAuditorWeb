import logging
from logging.handlers import SysLogHandler
from bson.objectid import ObjectId

FOUNDATION_IS_IMPORTED = False
BIPLIST_IS_IMPORTED  = False
PLISTLIB_IS_IMPORTED = False

try:
    import Foundation                                           #It only works on OS X
    FOUNDATION_IS_IMPORTED = True
    print(u"DEBUG: Mac OS X Obj-C Foundation successfully imported")
except ImportError:
    print(u"DEBUG: Cannot import Mac OS X Obj-C Foundation. Installing PyObjC on OS X is highly recommended")
    try:
        import biplist
        BIPLIST_IS_IMPORTED = True
    except ImportError:
        print(u"DEBUG: Cannot import the biplist lib. I may not be able to properly parse a binary pblist")
    try:
        import plistlib
        PLISTLIB_IS_IMPORTED = True
    except ImportError:
        print(u"DEBUG: Cannot import the plistlib lib. I may not be able to properly parse a binary pblist")

HTML_LOG_FILE = False
HTML_LOG_CONTENT = u""
HTML_LOG_MENU = u""

HTML_EVENTS_TL = u""
HTML_EVENTS_LANES = []
HTML_EVENTS_ITEMS = u""

def PrintAndLog(LogStr, TYPE):
    """ Write a string of log depending of its type and call the function to generate the HTML log or the Syslog if needed """

    global HTML_LOG_FILE
    global SYSLOG_SERVER

    if TYPE == "INFO" or "INFO_RAW":
        print(u"[INFO] " + LogStr)
        logging.info(LogStr)

    elif TYPE == "ERROR":
        print(u"[ERROR] " + LogStr)
        logging.error(LogStr)

    elif TYPE == "WARNING":
        print(u"[WARNING] " + LogStr)
        logging.warning(LogStr)

    elif TYPE == "DEBUG":
        print(u"[DEBUG] " + LogStr)
        logging.debug(LogStr)

    elif TYPE == "SECTION" or TYPE == "SUBSECTION":
        SectionTitle = u"\n#########################################################################################################\n"
        SectionTitle += "#                                                                                                       #\n"
        SectionTitle += "#         " +LogStr+ " "*(94-len(LogStr)) + "#\n"
        SectionTitle += "#                                                                                                       #\n"
        SectionTitle += "#########################################################################################################\n"
        print(SectionTitle)
        logging.info(u"\n" + SectionTitle)

    if HTML_LOG_FILE:
        HTMLLog(LogStr, TYPE)