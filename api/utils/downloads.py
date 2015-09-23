import os
import log
import crypto

ROOT_PATH = '/'

def ParseDownloads():
    all_data = []

    for User in os.listdir(os.path.join(ROOT_PATH, "Users")):
        if User[0] != ".":
            DlUserPath = os.path.join(ROOT_PATH, "Users", User, "Downloads")
            if os.path.isdir(DlUserPath):
                all_data.append(crypto.HashDir(User + u"\'s downloads", DlUserPath))
            else:
                log.PrintAndLog(DlUserPath + u" does not exist", "DEBUG")

            OldEmailUserPath = os.path.join(ROOT_PATH, "Users", User, "Library/Mail Downloads/")
            if os.path.isdir(OldEmailUserPath):
                all_data.append(crypto.HashDir(User + u"\'s old email downloads", OldEmailUserPath))
            else:
                log.PrintAndLog(OldEmailUserPath + u" does not exist", "DEBUG")

            EmailUserPath = os.path.join(ROOT_PATH, "Users", User, "Library/Containers/com.apple.mail/Data/Library/Mail Downloads")
            if os.path.isdir(EmailUserPath):
                all_data.append(crypto.HashDir(User + u"\'s email downloads", EmailUserPath))
            else:
                log.PrintAndLog(EmailUserPath + u" does not exist", "DEBUG")

    return all_data