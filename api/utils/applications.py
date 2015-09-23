import os
import log
import core
import time
import crypto

HASHES = []

ROOT_PATH = '/'

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
                PackagePlist = core.UniversalReadPlist(PackagePlistPath)

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

def ParseInstalledApps():
    return ParsePackagesDir(os.path.join(ROOT_PATH, "Applications"))