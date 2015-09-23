import log
import crypto
import os
import hashlib
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# Knock this down
import optparse
import sys
import logging
from logging.handlers import SysLogHandler
import sqlite3
import socket
import time
import json
import zipfile
import codecs                                                   #binary plist parsing does not work well in python3.3 so we are stuck in 2.7 for now
from functools import partial
import re
import bz2
import binascii
import platform

from utils import database

HASHES = []
LOCAL_HASHES_DB = {}

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