from helper.cTime import MyDate

# ------------------ [ elog() ] ------------------ #
    # Logs the error message into the "error_log.log" file
    # States what file, call and exception created the error log
def elog(ex, stk):
    fs = open("./logs/error_log.log", "a")
    frame = str(stk[0][0]).strip('<>').split(',')
    path = frame[1][8:-1].split('/')
    _file = '/'.join(path[3:])
    call = frame[3][6:] + '()'
    fs.write(MyDate().footer() + " " + _file + " CALL " + call + " ERROR-MSG " + str(ex) + '\n') 
    fs.close()

# ------------------ [ alog() ] ------------------ #
    # Clears "activity_log.log" and writes when the exception was called
def alog(ex):
    fs = open("./logs/activity_log.log", "a")
    fs.write(MyDate().footer() + " " + str(ex) + '\n') 
    fs.close()