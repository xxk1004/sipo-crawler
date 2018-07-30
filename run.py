import os, sys
import time, datetime
import subprocess, signal
import psutil
import database


def get_process_id(name):
    """Return process ids found by (partial) name or regex.

	>>> get_process_id('kthreadd')
	[2]
	>>> get_process_id('watchdog')
	[10, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 61]  # ymmv
	>>> get_process_id('non-existent process')
	[]
	"""
    child = subprocess.Popen(['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    return [int(pid) for pid in response.split()]


def TIMEOUT_COMMAND(command, timeout):
    """call shell-command and either return its output or kill it
	if it doesn't normally exit within timeout seconds and return None"""
    cmd = command.split(" ")
    start = datetime.datetime.now()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
        time.sleep(0.2)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            for pid in get_process_id('python'):
                try:
                    p = psutil.Process(pid)
                    if p.ppid() == process.pid:
                        try:
                            os.kill(pid, signal.SIGKILL)
                        except Exception as e:
                            print("Exception: " + repr(e), flush=True)
                except psutil.NoSuchProcess:
                    print("no process found with pid=" + str(pid), flush=True)
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return None
    return process.stdout.readlines()


count = 0
while True:
    timeout = 900
    count = count + 1
    year = sys.argv[1]
    strSources = sys.argv[2]
    month = count % 12
    order = count // 12
    if month == 0:
        month = 12
    if 1 <= month <= 9:
        month_str = '0' + str(month)
    else:
        month_str = str(month)
    if count % 10 == 1:
        count_str = str(count) + 'st'
    elif count % 10 == 2:
        count_str = str(count) + 'nd'
    elif count % 10 == 3:
        count_str = str(count) + 'rd'
    else:
        count_str = str(count) + 'th'
    startTime = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    print(startTime + ", start " + count_str + " crawling, date: " + str(year) + '.' + month_str, flush=True)
    # print("Current records number of " + year + ": " + str(database.countRecords(year)), flush=True)
    result = TIMEOUT_COMMAND('python3 crawl.py ' + str(year) + '.' + month_str + ' '+startTime+'.log ' + str(order) + ' ' + strSources, timeout)
    if result is None:
        print("Timeout occurred", flush=True)
    records = str(database.countRecords(year))
    print("Current records number of " + year + ": " + records, flush=True)
    database.addTrace(year, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), records)
    endTime = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    seconds = (datetime.datetime.strptime(endTime, "%Y-%m-%d_%H:%M:%S") - datetime.datetime.strptime(startTime,
                                                                                                     "%Y-%m-%d_%H:%M:%S")).seconds
    print("From {0} to {1}, finished {2} crawling, cost {3} seconds\n\n".format(startTime, endTime, count_str,
                                                                               str(seconds)), flush=True)
    time.sleep(60)
