import os
import sqlite3

def DumpSQLiteDb(SQLiteDbPath):
    all_rows = []

    if os.path.isfile(SQLiteDbPath):
        try:
            DbConnection = sqlite3.connect(SQLiteDbPath)
            DbCursor = DbConnection.cursor()
            DbCursor.execute("SELECT * from sqlite_master WHERE type = 'table'")
            Tables =  DbCursor.fetchall()

            for Table in Tables:
                DbCursor.execute("SELECT * from " + Table[2])
                Rows = DbCursor.fetchall()
                if len(Rows) == 0:
                    error = {
                        'ERROR': u"Table " + Table[2].decode("utf-8") + u" is empty"
                    }

                    DbConnection.close()

                    return error
                else:
                    for Row in Rows:
                        all_rows.append(Row)
            DbConnection.close()

            return all_rows
        except Exception as e:
            error = {
                'ERROR': u"Error with " + SQLiteDbPath.decode("utf-8") + u": " + str(e.args).decode("utf-8")
            }
            return error
    else:
        error = {
            'ERROR': SQLiteDbPath.decode("utf-8") + u" not found"
        }
        return error