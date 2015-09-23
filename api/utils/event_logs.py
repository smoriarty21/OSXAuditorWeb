import os
import re
import log
import time

ROOT_PATH = '/'

all_events = []

def ParseSystemlogFile(SystemLogPath, Year, Bzip2ed=False):
    global HTML_EVENTS_LANES
    global HTML_EVENTS_ITEMS
    global HTML_EVENTS_LANES_CPT

    AllEvents = []
    HTML_EVENTS_LANES = []
    HTML_EVENTS_ITEMS = u""

    try:
        with open(SystemLogPath, 'r') as SystemLogFile:
            SystemLogData = SystemLogFile.read()

            if Bzip2ed: SystemLogData = bz2.decompress(SystemLogData)

            DateRegex = "^(\w{3}\s{1,2}\d{1,2}\s[\d:]{8})"

            BootTimesRegExp = re.compile(DateRegex + ".+BOOT_TIME", re.MULTILINE)
            ShutDownTimesRegExp = re.compile(DateRegex + ".+\sSHUTDOWN_TIME", re.MULTILINE)

            HibernationInTimesLRegExp = re.compile(DateRegex + ".+\sPMScheduleWakeEventChooseBest", re.MULTILINE)       #Lion
            HibernationInTimesMLRegExp = re.compile(DateRegex + ".+\shibernate_setup\(0\)\stook", re.MULTILINE)     #Mountain Lion
            HibernationOutTimesLRegExp = re.compile(DateRegex + ".+\sMessage\sWake", re.MULTILINE)                      #Lion TOFIX (in SYSLOG)
            HibernationOutTimesMLRegExp = re.compile(DateRegex + ".+\sWake\sreason", re.MULTILINE)                      #Mountain Lion

            LockedSessionsLRegExp = re.compile(DateRegex + ".+\sloginwindow", re.MULTILINE)                         #Lion
            LockedSessionsMLRegExp = re.compile(DateRegex + ".+\sApplication\sApp:\"loginwindow\"", re.MULTILINE)       #Mountain Lion

            SessionsUnlockFailRegExp = re.compile(DateRegex + ".+\sThe\sauthtok\sis\sincorrect", re.MULTILINE)          #Lion and Mountain Lion
            SessionsUnlockOkRegExp = re.compile(DateRegex + ".+\Establishing\scredentials", re.MULTILINE)               #Lion and Mountain Lion

            SudosOkRegExp = re.compile(DateRegex + ".+\ssudo\[", re.MULTILINE)                                          #Lion and Mountain Lion
            SudosFailRegExp = re.compile(DateRegex + ".+\sincorrect\spassword\sattempts", re.MULTILINE)             #Lion and Mountain Lion

            USBKernelRegExp = re.compile(DateRegex + ".+\sUSBMSC\sIdentifier", re.MULTILINE)                                            #Lion and Mountain Lion
            USBFsEventRegExp = re.compile(DateRegex + ".+\sfseventsd\[35\]:\slog\sdir:\s/Volumes/.+getting\snew\suuid", re.MULTILINE)   #Lion and Mountain Lion

            TTYOpenedRegExp = re.compile(DateRegex + ".+\sUSER_PROCESS:\s\d+\sttys", re.MULTILINE)                      #Lion and Mountain Lion
            TTYClosedRegExp = re.compile(DateRegex + ".+\sDEAD_PROCESS:\s\d+\sttys", re.MULTILINE)                      #Lion and Mountain Lion

            NetUPKernelRegExp = re.compile(DateRegex + ".+\skernel\[\d\+]:\sEthernet.+Link\up", re.MULTILINE)           #Lion and Mountain Lion
            NetChangeLRegExp = re.compile(DateRegex + ".+\sconfigd\[\d+]:\snetwork\sconfiguration\schanged", re.MULTILINE)          #Lion
            NetChangeMLRegExp = re.compile(DateRegex + ".+\sconfigd\[\d+]:\snetwork\schanged:", re.MULTILINE)           #Mountain Lion

            BootTimes = BootTimesRegExp.findall(SystemLogData)
            for Item in BootTimes: AllEvents.append([Item, "Boot", 1])

            ShutDownTimes = ShutDownTimesRegExp.findall(SystemLogData)
            for Item in ShutDownTimes: AllEvents.append([Item, "Shutdown", 2])

            HibernationInTimesL = HibernationInTimesLRegExp.findall(SystemLogData)
            for Item in HibernationInTimesL: AllEvents.append([Item, "Hibernation in", 3])

            HibernationInTimesML = HibernationInTimesMLRegExp.findall(SystemLogData)
            for Item in HibernationInTimesML: AllEvents.append([Item, "Hibernation in", 3])

            HibernationOutTimesL = HibernationOutTimesLRegExp.findall(SystemLogData)
            for Item in HibernationOutTimesL: AllEvents.append([Item, "Hibernation out", 4])

            HibernationOutTimesML = HibernationOutTimesMLRegExp.findall(SystemLogData)
            for Item in HibernationOutTimesML: AllEvents.append([Item, "Hibernation out", 4])

            SessionsUnlockFail = SessionsUnlockFailRegExp.findall(SystemLogData)
            for Item in SessionsUnlockFail: AllEvents.append([Item, "Sessions unlock FAIL", 6])

            SessionsUnlockOk = SessionsUnlockOkRegExp.findall(SystemLogData)
            for Item in SessionsUnlockOk: AllEvents.append([Item, "Sessions unlock OK", 7])

            SudosOk = SudosOkRegExp.findall(SystemLogData)
            for Item in SudosOk: AllEvents.append([Item, "Sudo OK", 8])

            SudosFail = SudosFailRegExp.findall(SystemLogData)
            for Item in SudosFail: AllEvents.append([Item, "Sudo FAIL", 9])

            USBsKernel = USBKernelRegExp.findall(SystemLogData)
            for Item in USBsKernel: AllEvents.append([Item, "USB device (kernel)", 10])

            USBFsEvents = USBFsEventRegExp.findall(SystemLogData)
            for Item in USBFsEvents: AllEvents.append([Item, "USB device (filesystem)", 11])

            TTYsOpened = TTYOpenedRegExp.findall(SystemLogData)
            for Item in TTYsOpened: AllEvents.append([Item, "TTY opened", 12])

            TTYsClosed = TTYClosedRegExp.findall(SystemLogData)
            for Item in TTYsClosed: AllEvents.append([Item, "TTY closed", 13])

            AllEvents.sort(key=lambda a:a[0])

            for Events in AllEvents:
                event = {}

                if Events[1] not in HTML_EVENTS_LANES:
                    HTML_EVENTS_LANES.append(Events[1])

                SplittedTime = Events[0].split(" ")

                if len(SplittedTime) == 3:
                    EventTimeWithYear = " ".join(SplittedTime[0:2]) + ", " + Year + " " + SplittedTime[2]
                elif len(SplittedTime) == 4:
                    EventTimeWithYear = " ".join(SplittedTime[0:3]) + ", " + Year + " " + SplittedTime[3]
                else:
                    EventTimeWithYear = "Error"

                event['event'] = Events[1]
                event['timestamp'] = EventTimeWithYear

                all_events.append(event)
    except:
        log.PrintAndLog("Failed to open " + SystemLogPath.decode("utf-8"), "ERROR")

def ParseEventLogs():
    """ Extract events from the event logs """

    global HTML_EVENTS_TL
    global HTML_LOG_CONTENT
    global HTML_EVENTS_LANES

    SystemLogsPath = os.path.join(ROOT_PATH, "var/log/")

    for LogFile in os.listdir(SystemLogsPath):
        print 'go'
        LogFilePath = os.path.join(SystemLogsPath, LogFile)
        Year = time.strftime("%Y", time.localtime(os.path.getctime(LogFilePath)))                                   #nasty hack because the syslog format sucks

        if re.match("^system\.log$", LogFile):
            print 'parse 1'
            ParseSystemlogFile(LogFilePath, Year)
        if re.match("^system\.log\.\d\.bz2$", LogFile):
            print 'parse 2'
            ParseSystemlogFile(LogFilePath, Year, True)

    return { 'system': all_events }