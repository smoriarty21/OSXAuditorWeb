import os

import log
import sql
import core
import error

ADMINS = []
all_user_act_data = []

ROOT_PATH = '/'

def ParseSysUsers():
    global ADMINS

    for User in os.listdir(os.path.join(ROOT_PATH, "private/var/db/dslocal/nodes/Default/users")):
        if User[0] != ".":
            SysUserPlistPath = os.path.join(ROOT_PATH, "private/var/db/dslocal/nodes/Default/users", User)
            log.PrintAndLog(User[:-6] + u"\'s system account details", "SUBSECTION")

            SysUserPlist = core.UniversalReadPlist(SysUserPlistPath)

            UserDetails =""
            if "name" in SysUserPlist:
                Names = u""
                for Name in SysUserPlist["name"]:
                    Names += Name
                    if Name in ADMINS:
                        Names += u" (is Admin)"
                    Names += u"\n"
                UserDetails += u"Name(s): " + Names

            if "realname" in SysUserPlist:
                UserDetails += u"Real Name(s): " + core.StringFromDic(SysUserPlist["realname"])

            if "shell" in SysUserPlist:
                UserDetails += u"Shell(s): " + core.StringFromDic(SysUserPlist["shell"])

            if "home" in SysUserPlist:
                UserDetails += u"Home(s): " + core.StringFromDic(SysUserPlist["home"])

            if "uid" in SysUserPlist:
                UserDetails += u"UID(s): " + core.StringFromDic(SysUserPlist["uid"])

            if "gid" in SysUserPlist:
                UserDetails += u"GID(s): " + core.StringFromDic(SysUserPlist["gid"])

            if "generateduid" in SysUserPlist:
                Generateduids = u""
                for Generateduid in SysUserPlist["generateduid"]:
                    Generateduids += Generateduid
                    if Generateduid in ADMINS:
                        Generateduids += u" (is Admin)"
                    Generateduids += u"\n"
                UserDetails += u"generated UID(s): " + Generateduids

            if "LinkedIdentity" in SysUserPlist:
                UserDetails += u"LinkedIdentities have been found. Extraction of LinkedIdentities is not implemented yet."

            log.PrintAndLog(UserDetails, "INFO_RAW")

def ParseUsersRecentItems(RecentItemsAccountPlistPath):
    recent = []
    RecentItemsAccountPlist = core.UniversalReadPlist(RecentItemsAccountPlistPath)

    if "RecentServers" in RecentItemsAccountPlist:
        recent_servers = {}
        RecentServers = RecentItemsAccountPlist["RecentServers"]["CustomListItems"]
        if len(RecentServers) != 0:
            recent_servers['recent_servers'] = []

            for RecentServer in RecentServers:
                recent_servers['recent_servers'].append(RecentServer['name']) 
        else:
            recent_servers['info'] = error.NO_RECENT_SERVERS

        recent.append(recent_servers)

    if "RecentDocuments" in RecentItemsAccountPlist:
        recent_documents = {}
        RecentDocuments = RecentItemsAccountPlist["RecentDocuments"]["CustomListItems"]

        if len(RecentDocuments) != 0:
            recent_documents['recent_documents'] = []

            for RecentDocument in RecentDocuments:
                recent_documents['recent_documents'].append(RecentDocument["Name"])
        else:
            recent_documents['info'] = error.NO_RECENT_DOCS
        recent.append(recent_documents)

    if "RecentApplications" in RecentItemsAccountPlist:
        recent_applicatons = {}
        RecentApplications = RecentItemsAccountPlist["RecentApplications"]["CustomListItems"]

        if len(RecentApplications) != 0:
            recent_applicatons['recent_applications'] = []

            for RecentApplication in RecentApplications:
                recent_applicatons['recent_applications'].append(RecentApplication["Name"])
        else:
            recent_application['INFO'] = error.NO_RECENT_APPS
        recent.append(recent_applicatons)

    if "Hosts" in RecentItemsAccountPlist:
        RecentHostsList = ""
        RecentHosts = RecentItemsAccountPlist["Hosts"]["CustomListItems"]
        if len(RecentHosts) != 0:
            for RecentHost in RecentHosts:
                RecentHostsList += RecentHost["Name"] + " -> " + RecentHost["URL"] + " | "
            log.PrintAndLog("Recent hosts : " + RecentHostsList, "INFO")
        else:
            log.PrintAndLog("No recent hosts", "INFO")

    return recent

def ParseMailAppAccount(MailAccountPlistPath):
    mail_accounts = []
    MailAccountPlist = False
    NbMailAccounts = 0
    NbSmtpAccounts = 0

    MailAccountPlist = core.UniversalReadPlist(MailAccountPlistPath)

    if MailAccountPlist:
        if "MailAccounts" in MailAccountPlist:
            MailAccounts = MailAccountPlist["MailAccounts"]

            for MailAccount in MailAccounts:
                new_mail_act = {}
                MAccountPref = ""

                if "AccountName" in MailAccount:
                    MAccountPref = "AccountName: " + MailAccount["AccountName"] + " - "
                    new_mail_act['account_name'] = MailAccount["AccountName"]

                    if "AccountType" in MailAccount:
                        new_mail_act['account_type'] = MailAccount["AccountType"]
                        MAccountPref += "AccountType: " + MailAccount["AccountType"] + " - "

                    if "SSLEnabled" in MailAccount:
                        new_mail_act['ssl_enabled'] = MailAccount["SSLEnabled"]
                        MAccountPref += "SSLEnabled: " + MailAccount["SSLEnabled"] + " - "

                    if "Username" in MailAccount:
                        new_mail_act['username'] = MailAccount["Username"]
                        MAccountPref += "Username: " + MailAccount["Username"]  + " - "

                    if "Hostname" in MailAccount:
                        new_mail_act['hostname'] = MailAccount["Hostname"]
                        MAccountPref += "Hostname: " + MailAccount["Hostname"]  + " - "

                    if "PortNumber" in MailAccount:
                        new_mail_act['port'] = MailAccount["PortNumber"]
                        MAccountPref += "(" + MailAccount["PortNumber"]  + ") - "

                    if "SMTPIdentifier" in MailAccount:
                        new_mail_act['smtp_identifier'] = MailAccount["SMTPIdentifier"]
                        MAccountPref += "SMTPIdentifier: " + MailAccount["SMTPIdentifier"]  + " - "

                    if "EmailAddresses" in MailAccount:
                        new_mail_act['email_addresses'] = []

                        for EmailAddresse in MailAccount["EmailAddresses"]:
                            new_mail_act['email_addresses'].append(EmailAddresse)
                            MAccountPref += "EmailAddresse: " + EmailAddresse + " - "
                NbMailAccounts += 1
                mail_accounts.append(new_mail_act)
        if len(mail_accounts):
            return mail_accounts
        else:
            ex = {
                'ERROR': error.NO_EMAIL_ACCOUNTS
            }
            return ex

        #log.PrintAndLog(u"SMTP accounts", "SUBSECTION")
        if "DeliveryAccounts" in MailAccountPlist:
            DeliveryAccounts = MailAccountPlist["DeliveryAccounts"]
            for DeliveryAccount in DeliveryAccounts:
                DAccountPref = ""
                if "AccountName" in DeliveryAccount:
                    DAccountPref = "AccountName: " + DeliveryAccount["AccountName"] + " - "
                    if "AccountType" in DeliveryAccount: DAccountPref += "AccountType: " + DeliveryAccount["AccountType"] + " - "
                    if "SSLEnabled" in DeliveryAccount: DAccountPref += "SSLEnabled: " + DeliveryAccount["SSLEnabled"] + " - "
                    if "Username" in DeliveryAccount: DAccountPref += "Username: " + DeliveryAccount["Username"]  + " - "
                    if "Hostname" in DeliveryAccount: DAccountPref += "Hostname: " + DeliveryAccount["Hostname"]  + " - "
                    if "PortNumber" in DeliveryAccount: DAccountPref += "(" + MailAccount["PortNumber"]  + ") - "
                    log.PrintAndLog(DAccountPref.decode("utf-8"), "INFO")
                NbSmtpAccounts += 1
            if NbSmtpAccounts == 0:
                log.PrintAndLog(u"No SMTP account)","INFO")

def ParseSysAdminsGroup():
    global ADMINS

    #log.PrintAndLog(u"System\'s admins", "SUBSECTION")

    SysAdminsPlistPath = os.path.join(ROOT_PATH, "private/var/db/dslocal/nodes/Default/groups/admin.plist")
    SysAdminsPlist = core.UniversalReadPlist(SysAdminsPlistPath)

    if "groupmembers" in SysAdminsPlist:
        for Admin in SysAdminsPlist["groupmembers"]:
            ADMINS.append(Admin)

    if "users" in SysAdminsPlist:
        for Admin in SysAdminsPlist["users"]:
            ADMINS.append(Admin)

    return ADMINS
    #Admins = u""
    #for Admin in ADMINS:
    #    Admins += Admin + u"\n"
    #log.PrintAndLog(Admins, "INFO_RAW")

def ParseUsersAccounts():
    social_acts = None

    for User in os.listdir(os.path.join(ROOT_PATH, "Users")):
        user_social_account = {}
        UsersAccountPath = os.path.join(ROOT_PATH, "Users", User, "Library/Accounts/Accounts3.sqlite")

        if User[0] != ".":
            user_social_account['user'] = User
            user_social_account['users_account_path'] = UsersAccountPath

            if os.path.isfile(UsersAccountPath):
                social_acts = sql.DumpSQLiteDb(UsersAccountPath)
                user_social_account['social_acts'] = social_acts
            else:
                user_social_account['social_acts'] = {
                    'user': User,
                    'ERROR': User + ' ' + error.NO_SOCIAL_ACCOUNTS
                }

            all_user_act_data.append(user_social_account)

    for User in os.listdir(os.path.join(ROOT_PATH, "Users")):
        mail_tmp = {}
        MailAccountPlistPath = os.path.join(ROOT_PATH, "Users", User, "Library/Containers/com.apple.mail/Data/Library/Mail/V2/MailData/Accounts.plist")

        if User[0] != ".":
            if os.path.isfile(MailAccountPlistPath):
                mail_tmp['user'] = User
                mail_tmp['mail_account_plist_path'] = MailAccountPlistPath
                mail_tmp['mail_accounts'] = ParseMailAppAccount(MailAccountPlistPath)
            else:
                mail_tmp = {
                    'user': User,
                    'ERROR': User + ' ' + error.NO_MAIL_APP
                }
            all_user_act_data.append(mail_tmp)

    for User in os.listdir(os.path.join(ROOT_PATH, "Users")):
        recent_items_tmp = {}
        RecentItemsAccountPlistPath = os.path.join(ROOT_PATH, "Users", User, "Library/Preferences/com.apple.recentitems.plist")

        if User[0] != ".":
            if os.path.isfile(RecentItemsAccountPlistPath):
                recent_items_tmp['recent_items_account_plist_path'] = RecentItemsAccountPlistPath
                recent_items_tmp['user'] = User
                recent_items_tmp['recent_items'] = ParseUsersRecentItems(RecentItemsAccountPlistPath)
            else:
                ex = {
                    'user': User,
                    'INFO': User + ' ' + error.NO_RECENT_ITEMS
                }
            all_user_act_data.append(recent_items_tmp)

    admins_obj = {
        'admins': ParseSysAdminsGroup()
    }
    #admins_list = ParseSysAdminsGroup()
    all_user_act_data.append(admins_obj)

    # TODO: Complete this
    ParseSysUsers()

    return all_user_act_data