import os
import log
import crypto
import binascii

import time

ROOT_PATH = '/'

FOUNDATION_IS_IMPORTED = False
BIPLIST_IS_IMPORTED  = False
PLISTLIB_IS_IMPORTED = False

HASHES = []

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

# TODO: Move these fucking parsers into a parse module
def ParseStartupItems(StartupItemsPath):
    """ Parse the StartupItems plist and hash its program argument """
    all_data = []

    StartupItemsPlist = False
    NbStartupItems = 0

    for StartupItems in os.listdir(StartupItemsPath):
    	data = {}

        StartupItemsPlistPath = os.path.join(StartupItemsPath, StartupItems, "StartupParameters.plist")

        log.PrintAndLog(StartupItemsPlistPath, "DEBUG")
        StartupItemsPlist = UniversalReadPlist(StartupItemsPlistPath)

        if StartupItemsPlist:
            if "Provides" in StartupItemsPlist:
                FilePath = os.path.join(StartupItemsPath, StartupItems, StartupItemsPlist["Provides"][0])
                data['filepath'] = FilePath
                data['dirpath'] = os.path.join(StartupItemsPath, StartupItems)

                Md5 = BigFileMd5(FilePath)
                if Md5:
                    if Md5 not in HASHES:
                        HASHES.append(Md5)
                        data['hash'] = str(Md5)

                    log.PrintAndLog(Md5 + u" "+ FilePath.decode("utf-8") + u" - " + time.ctime(os.path.getmtime(FilePath)) + u" - " + time.ctime(os.path.getctime(FilePath))+ u"\n", "INFO")

    	data['lastpathmod'] = time.ctime(os.path.getmtime(FilePath))
    	data['lastmetamod'] = time.ctime(os.path.getctime(FilePath))

    	all_data.append(data)

        NbStartupItems += 1
    if NbStartupItems == 0:
        log.PrintAndLog(StartupItemsPath.decode("utf-8") + u" is empty", "INFO")

    return all_data

def ParsePackagesDir(PackagesDirPath):
    all_data = []

    plistfile = "Info.plist"
    IgnoredFiles = [".DS_Store", ".localized"]

    PackagePlistPath = ""
    CFBundleExecutablepath = ""
    NbPackages = 0

    for PackagePath in os.listdir(PackagesDirPath):
        data = {}

        if PackagePath not in IgnoredFiles:
            if PackagePath[-4:] == ".app" or PackagePath[-5:] == ".kext":
                if os.path.isfile(os.path.join(PackagesDirPath, PackagePath, plistfile)):
                    PackagePlistPath = os.path.join(PackagesDirPath, PackagePath, plistfile)
                    CFBundleExecutablepath = ""
                elif os.path.isfile(os.path.join(PackagesDirPath, PackagePath, "Contents", plistfile)):
                    PackagePlistPath = os.path.join(PackagesDirPath, PackagePath, "Contents", plistfile)
                    print PackagePlistPath
                    print
                    CFBundleExecutablepath = "Contents/MacOS/"
                else:
                    log.PrintAndLog(os.path.join(PackagesDirPath, PackagePath).decode("utf-8"), "DEBUG")
                    log.PrintAndLog(u"Cannot find any Info.plist in " + PackagePath.decode("utf-8"), "ERROR")
                    continue

                log.PrintAndLog(os.path.join(PackagesDirPath, PackagePath).decode("utf-8"), "DEBUG")
                PackagePlist = UniversalReadPlist(PackagePlistPath)

                if PackagePlist:
                    if "CFBundleExecutable" in PackagePlist:
                        if PackagePlist["CFBundleExecutable"] != "":
                            FilePath = os.path.join(PackagesDirPath, PackagePath, CFBundleExecutablepath, PackagePlist["CFBundleExecutable"])
                            data['filepath'] = FilePath
                            data['dirpath'] = os.path.join(PackagesDirPath, PackagePath)

                            Md5 = crypto.BigFileMd5(FilePath)
                            if Md5:
                                if Md5 not in HASHES:
                                    data['hash'] = str(Md5)
                                    HASHES.append(Md5)
                                log.PrintAndLog(Md5 + u" "+ FilePath.decode("utf-8") + u" - " + time.ctime(os.path.getmtime(FilePath)) + u" - " + time.ctime(os.path.getctime(FilePath)) + u"\n", "INFO")
                                data['lastpathmod'] = time.ctime(os.path.getmtime(FilePath))
                                data['lastmetamod'] = time.ctime(os.path.getctime(FilePath))

                        else:
                            log.PrintAndLog(u"The CFBundleExecutable key in " + PackagePlistPath.decode("utf-8") + u" is empty\n", "ERROR")
                    else:
                        log.PrintAndLog(u"Cannot find the CFBundleExecutable key in " + PackagePlistPath.decode("utf-8") + u"\n", "ERROR")
            NbPackages += 1
            all_data.append(data)

            if os.path.isdir(os.path.join(PackagesDirPath, PackagePath)):
                ParsePackagesDir(os.path.join(PackagesDirPath, PackagePath))

        else: continue

    if NbPackages == 0:
        log.PrintAndLog(PackagesDirPath.decode("utf-8") + u" is empty (no package found)", "INFO")

    return all_data

def UniversalReadPlist(PlistPath):
    """ Try to read a plist depending of the plateform and the available libs. Good luck Jim... """

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

def ParseLaunchAgents(AgentsPath):
    """ Parse a LanchAgent plist and hash its program argument. Also look for suspicious keywords in the plist itself """
    all_data = []

    SuspiciousPlist = ["exec", "socket" ,"open", "connect", "/dev/tcp/", "/bin/sh"]
    LaunchAgentPlist = False

    NbLaunchAgents = 0
    for LaunchAgent in os.listdir(AgentsPath):
    	data = {}
        LaunchAgentPlistpath = os.path.join(AgentsPath, LaunchAgent)

        log.PrintAndLog(LaunchAgentPlistpath, "DEBUG")
        LaunchAgentPlist = UniversalReadPlist(LaunchAgentPlistpath)

        if LaunchAgentPlist:
            if "Program" in LaunchAgentPlist and "Label" in LaunchAgentPlist:
                FilePath = LaunchAgentPlist["Program"]
                data['filepath'] = FilePath
                Md5 = crypto.BigFileMd5(FilePath)
                if Md5:
                    if Md5 not in HASHES:
                        HASHES.append(Md5)
                        data['hash'] = str(Md5)

                    data['lastpathmod'] = time.ctime(os.path.getmtime(FilePath))
                    data['lastmetamod'] = time.ctime(os.path.getctime(FilePath))
                    log.PrintAndLog(Md5 + u" "+ FilePath.decode("utf-8") + u" - " + time.ctime(os.path.getmtime(FilePath)) + u" - " + time.ctime(os.path.getctime(FilePath)) + u"\n", "INFO")

                continue
            if "ProgramArguments" in LaunchAgentPlist and "Label" in LaunchAgentPlist:
                FilePath = LaunchAgentPlist["ProgramArguments"][0]
                data['filepath'] = FilePath
                Md5 = crypto.BigFileMd5(FilePath)
                if Md5:
                    if Md5 not in HASHES:
                        HASHES.append(Md5)
                        data['hash'] = str(Md5)

                    data['lastpathmod'] = time.ctime(os.path.getmtime(FilePath))
                    data['lastmetamod'] = time.ctime(os.path.getctime(FilePath))

                    log.PrintAndLog(Md5 + u" "+ FilePath.decode("utf-8") + u" - " + time.ctime(os.path.getctime(FilePath)) + u" - " + time.ctime(os.path.getmtime(FilePath)) + u"\n", "INFO")
                if len(LaunchAgentPlist["ProgramArguments"]) >= 3:
                    if any(x in LaunchAgentPlist["ProgramArguments"][2] for x in SuspiciousPlist):
                        log.PrintAndLog(LaunchAgentPlist["ProgramArguments"][2].decode("utf-8")+ u" in " + LaunchAgentPlistpath.decode("utf-8") + u" looks suspicious", "WARNING")

        NbLaunchAgents += 1
        all_data.append(data)

    if NbLaunchAgents == 0:
        log.PrintAndLog(AgentsPath.decode("utf-8") + u" is empty", "INFO")

    return all_data

def ParseStartup():
	all_data = []
	""" Parse the different LauchAgents and LaunchDaemons  """

	log.PrintAndLog(u"Startup", "SECTION")

	log.PrintAndLog(u"System agents", "SUBSECTION")
	all_data.append(ParseLaunchAgents(os.path.join(ROOT_PATH, "System/Library/LaunchAgents/")))

	log.PrintAndLog(u"System daemons", "SUBSECTION")
	all_data.append(ParseLaunchAgents(os.path.join(ROOT_PATH, "System/Library/LaunchDaemons/")))

	log.PrintAndLog(u"Third party agents", "SUBSECTION")
	all_data.append(ParseLaunchAgents(os.path.join(ROOT_PATH, "Library/LaunchAgents/")))

	log.PrintAndLog(u"Third party daemons", "SUBSECTION")
	all_data.append(ParseLaunchAgents(os.path.join(ROOT_PATH, "Library/LaunchDaemons/")))

	log.PrintAndLog(u"System ScriptingAdditions", "SUBSECTION")
	all_data.append(ParsePackagesDir(os.path.join(ROOT_PATH, "System/Library/ScriptingAdditions/")))

	log.PrintAndLog(u"Third party ScriptingAdditions", "SUBSECTION")
	all_data.append(ParsePackagesDir(os.path.join(ROOT_PATH, "Library/ScriptingAdditions/")))

	# Parse the old and deprecated Startup Items
	log.PrintAndLog(u"Deprecated system StartupItems", "SUBSECTION")
	all_data.append(ParseStartupItems(os.path.join(ROOT_PATH, "System/Library/StartupItems/")))

	log.PrintAndLog(u"Deprecated third party StartupItems", "SUBSECTION")
	all_data.append(ParseStartupItems(os.path.join(ROOT_PATH, "Library/StartupItems/")))

	log.PrintAndLog(u"Users\' agents", "SUBSECTION")
	for User in os.listdir(os.path.join(ROOT_PATH, "Users")):
		UserLAPath = os.path.join(ROOT_PATH, "Users", User, "Library/LaunchAgents/")
		if User[0] != "." and os.path.isdir(UserLAPath):
			log.PrintAndLog(User.decode("utf-8") + u"\'s agents", "SUBSECTION")
			ParseLaunchAgents(UserLAPath)

			log.PrintAndLog(u"Users\' LoginItems", "SUBSECTION")
	for User in os.listdir(os.path.join(ROOT_PATH, "Users")):
		LoginItemsPlistPath = os.path.join(ROOT_PATH, "Users", User, "Library/Preferences/com.apple.loginitems.plist")
		if User[0] != "." and os.path.isfile(LoginItemsPlistPath):
			log.PrintAndLog(User + u"\'s LoginItems", "SUBSECTION")
			log.PrintAndLog(LoginItemsPlistPath, "DEBUG")
			LoginItemsPlist = UniversalReadPlist(LoginItemsPlistPath)

			if "SessionItems" in LoginItemsPlist:
				CustomListItems = LoginItemsPlist["SessionItems"]["CustomListItems"]
				for CustomListItem in CustomListItems:
					log.PrintAndLog(CustomListItem["Name"].decode("utf-8") + u" - " + binascii.hexlify(CustomListItem["Alias"]).decode("hex").decode("utf-8", "ignore"), "INFO")
	return all_data