import os
import log
import hashlib

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

HASHES = []

def BigFileMd5(FilePath):
    Md5 = hashlib.md5()
    try:
        with open(FilePath, 'rb') as f:
            for Chunk in iter(partial(f.read, 1048576), ''):
                Md5.update(Chunk)
            return Md5.hexdigest()
    except:
        log.PrintAndLog(u"Cannot hash " + FilePath.decode("utf-8"), "ERROR")
        
        return False

def HashDir(Title, Path):
    all_data = []

    NbFiles = 0
    for Root, Dirs, Files in os.walk(Path):
        data = {}

        for File in Files:
            FilePath = os.path.join(Root, File)
            Md5 = BigFileMd5(FilePath)

            data['filepath'] = FilePath

            if Md5:
                if Md5 not in HASHES:
                    HASHES.append(Md5)
                    data['hash'] = Md5
                data['lastpathmod'] = time.ctime(os.path.getmtime(FilePath))
                data['lastmetamod'] = time.ctime(os.path.getctime(FilePath))

                all_data.append(data)
                log.PrintAndLog(Md5 +" "+ FilePath.decode("utf-8") + u" - " + time.ctime(os.path.getmtime(FilePath)) + u" - " + time.ctime(os.path.getctime(FilePath)) + u"\n", "INFO")
            NbFiles += 1

    if NbFiles == 0:
        log.PrintAndLog(Path.decode("utf-8") + u" is empty", "INFO")

    return all_data