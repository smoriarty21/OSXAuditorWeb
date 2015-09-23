import log

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

# TODO: Build this. The user module needs it badly
def reduce(key, data_array):
    print key

def UniversalReadPlist(PlistPath):
    plistDictionnary = False

    if FOUNDATION_IS_IMPORTED:
        plistNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(PlistPath, Foundation.NSUncachedRead, None)
        if errorMessage is not None or plistNSData is None:
            log.PrintAndLog(u"Unable to read in the data from the plist file: " + PlistPath.decode("utf-8"), "ERROR")
        plistDictionnary, plistFormat, errorMessage = Foundation.NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(plistNSData, Foundation.NSPropertyListMutableContainers, None, None)
        if errorMessage is not None or plistDictionnary is None:
            log.PrintAndLog(u"Unable to read in the data from the plist file: " + PlistPath.decode("utf-8"), "ERROR")
        if not hasattr(plistDictionnary, "has_key"):
            log.PrintAndLog(u"The plist does not have a dictionary as its root as expected: " + PlistPath.decode("utf-8"), "ERROR")
        return plistDictionnary
    else:
        if BIPLIST_IS_IMPORTED:
            try:
                plistDictionnary = biplist.readPlist(PlistPath)
            except (IOError):
                log.PrintAndLog (u"Cannot open " + PlistPath.decode("utf-8") , "ERROR")
            except:
                log.PrintAndLog(u"Cannot parse " + PlistPath.decode("utf-8") + u" (Binary or JSON plist may FAIL) \n", "ERROR")
            return plistDictionnary

        elif PLISTLIB_IS_IMPORTED:
            try:
                plistDictionnary = plistlib.readPlist(PlistPath)
            except (IOError):
                log.PrintAndLog (u"Cannot open " + PlistPath.decode("utf-8") , "ERROR")
            except:
                log.PrintAndLog(u"Cannot parse " + PlistPath.decode("utf-8") + u" (Binary or JSON plist may FAIL) \n", "ERROR")
            return plistDictionnary
        else:
            log.PrintAndLog(u"Cannot parse " + PlistPath.decode("utf-8") + u". No plist lib available.\n", "ERROR")
            return None

def StringFromDic(dic):
    Content = u""
    for stuff in dic:
        Content += stuff + u"\n"
    return Content