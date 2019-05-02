__copyright__ = """
Copyright 2008 Henryk Modzelewski
"""
__license__ =  """
This file is part of SLIMpy .

SLIMpy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SLIMpy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with SLIMpy . If not, see <http://www.gnu.org/licenses/>.
"""

'''
A simple parallel execution of arbitrary commands
'''

# imports
import os
import sys
if sys.version_info < (2,4,0):
        print "FATAL ERROR: Too old version of python. Use 2.4 or newer."
        sys.exit(1)
import time
import subprocess
import threading
from datetime import timedelta,datetime

# default options
RSH = 'ssh'
TIMEOUT = timedelta(0,3600L)
TIMECHECK = 10
SHOWTIMES = False
VERBOSE = False
KILL = True

def ExecCMD(nodes,cmd,
    RSH=RSH,TIMEOUT=TIMEOUT,TIMECHECK=TIMECHECK,SHOWTIMES=SHOWTIMES,VERBOSE=VERBOSE,KILL=KILL):
    '''
    Execute a command on the remote nodes

    Requires:
        Standard python modules.

    Parameters:
        nodes: list of nodes (user@hostname or hostname)
        cmd: a command string (with &&, ||, ;, or pipes)

    Keyword parameters (optional):
        RSH: command to execute remote shell
        TIMEOUT: timedelta object with timeout for each command
        TIMECHECK: how often to check for progress in seconds
        SHOWTIMES: show start, end, and wall times
        VERBOSE: be verbose
        KILL: kill the command exceeding the timeout

    Returns:
        Cumulative status of all nodes (0 is OK)

    Notes:
        None so far

    Bugs:
        None so far
    '''
    if VERBOSE:
        print 'Nodes:',nodes
        print 'Command:',cmd
        print 'RSH:',RSH
        print 'TIMEOUT:',TIMEOUT
        print 'TIMECHECK:',TIMECHECK
        print 'SHOWTIMES:',SHOWTIMES
        print 'KILL:',KILL

    # predefine necessary variables
    status = 0
    threads = {}

    # start execution
    try:
        # spawn threads
        for key in range(len(nodes)):
            threads[key] = RemoteCMD(RSH,nodes[key],cmd)
            threads[key].start()
            if VERBOSE:
                while not threads[key].pid: time.sleep(1)
                print threads[key].remote, '\n\t@', threads[key].stime,
                print 'PPID:', threads[key].ppid, 'PID:', threads[key].pid
        # wait to finish
        while ( check_active(threads,TIMEOUT,KILL) > 0 ):
            while ( check_passive(threads,TIMEOUT,KILL) < 1 ): time.sleep(TIMECHECK)
            printlist = get_passive(threads)
            for key in printlist:
                status += printout(threads[key],SHOWTIMES)
                del threads[key]
    except KeyboardInterrupt:
        # clean if exceptions
        print '\rException KeyboardInterrupt requested.'
        print '\tKilling all active remote threads.'
        for key in threads.keys():
            print '\t\tKilling ', threads[key].remote
            threads[key].abort()

    # printout whatever is left from exceptions
    if len(threads.keys()) > 0:
        print 'Showing leftovers'
        for key in threads.keys():
            status += printout(threads[key],SHOWTIMES)
            del threads[key]
    
    return status

def ExecCMDs(nodes,cmds,
    RSH=RSH,TIMEOUT=TIMEOUT,TIMECHECK=TIMECHECK,SHOWTIMES=SHOWTIMES,VERBOSE=VERBOSE,KILL=KILL):
    '''
    Execute a set of commands on the remote nodes

    Requires:
        Standard python modules.

    Parameters:
        nodes: list of nodes (user@hostname or hostname)
        cmds: a list of commands (separated by &&, ||, ;, or pipes) per element

    Keyword parameters (optional):
        RSH: command to execute remote shell
        TIMEOUT: timedelta object with timeout for each command
        TIMECHECK: how often to check for progress in seconds
        SHOWTIMES: show start, end, and wall times
        VERBOSE: be verbose
        KILL: kill the command exceeding the timeout

    Returns:
        Cumulative status of all commands (0 is OK)

    Notes:
        None so far

    Bugs:
        None so far
    '''
    if VERBOSE:
        print 'Nodes:',nodes
        print 'Commands:',cmds
        print 'RSH:',RSH
        print 'TIMEOUT:',TIMEOUT
        print 'TIMECHECK:',TIMECHECK
        print 'SHOWTIMES:',SHOWTIMES
        print 'KILL:',KILL

    # predefine necessary variables
    status = 0
    passive = list(range(len(nodes)))
    passive.reverse()
    threads = {}

    # start execution
    try:
        # spawn threads
        for i in range(len(cmds)):
            try: key=passive.pop()
            except:
                while ( check_passive(threads,TIMEOUT,KILL) < 1 ): time.sleep(TIMECHECK)
                passive.extend(get_passive(threads))
                for key in passive:
                    status += printout(threads[key],SHOWTIMES)
                    del threads[key]
                key=passive.pop()
            threads[key] = RemoteCMD(RSH,nodes[key],cmds[i])
            threads[key].start()
            if VERBOSE:
                while not threads[key].pid: time.sleep(1)
                print threads[key].remote, '\n\t@', threads[key].stime,
                print 'PPID:', threads[key].ppid, 'PID:', threads[key].pid
        # wait to finish
        while ( check_active(threads,TIMEOUT,KILL) > 0 ):
            while ( check_passive(threads,TIMEOUT,KILL) < 1 ): time.sleep(TIMECHECK)
            printlist = get_passive(threads)
            for key in printlist:
                status += printout(threads[key],SHOWTIMES)
                del threads[key]
    except KeyboardInterrupt:
        # clean if exceptions
        print '\rException KeyboardInterrupt requested.'
        print '\tKilling all active remote threads.'
        for key in threads.keys():
            print '\t\tKilling ', threads[key].remote
            threads[key].abort()

    # printout whatever is left from exceptions
    if len(threads.keys()) > 0:
        print 'Showing leftovers'
        for key in threads.keys():
            status += printout(threads[key],SHOWTIMES)
            del threads[key]
    
    return status

class RemoteCMD(threading.Thread):
    '''
    Remote command definitions and execution
    '''
    def __init__(self,rsh,host,cmd):
        threading.Thread.__init__(self)
        self.host = host
        self.contents = ['NULL'+'\n']
        self.account = host
        if self.host == 'localhost':
            self.cmd = cmd
            self.remote = self.cmd
        else:
            self.cmd = '\''+cmd+'\''
            self.remote = ' '.join([rsh,self.account,self.cmd])
        self.ppid = None
        self.pid = None
        self.stime = None
        self.etime = None
        self.status = None
        self.contents = None
    def run(self):
        # this is the part that can take a while
        self.ppid = os.getpid()
        self.stime = datetime.now()
        pout = os.tmpfile()
        sP = subprocess.Popen([self.remote], shell=True, bufsize=-1,
                stdin=None, stdout=pout, stderr=subprocess.STDOUT, close_fds=False)
                #stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        self.pid = sP.pid
        self.status = sP.wait()
        self.etime = datetime.now()
        pout.flush()
        pout.seek(0,0)
        self.contents = pout.readlines()
        pout.close()
        # when this method returns, the thread exits
    def abort(self):
        while not self.pid: time.sleep(1)
        try: os.kill(self.pid,9)
        except: pass
        else: self.join(30)

def check_active(t,tout,kill):
    '''
    returns the number of RSH threads that are active
    and kill threads exceeding WALTIME
    '''
    now = datetime.now()
    active = 0
    for key in t.keys():
        if t[key].isAlive():
            if ( now-t[key].stime > tout) :
                print 'WALL-TIME EXCEEDED for PID', t[key].pid, ':', t[key].remote
                if kill: t[key].abort()
            active += 1
    return active

def check_passive(t,tout,kill):
    '''
    returns the number of RSH threads that are passive
    and kill threads exceeding WALTIME
    '''
    now = datetime.now()
    passive = 0
    for key in t.keys():
        passive += 1
        if t[key].isAlive():
            if ( now-t[key].stime > tout ):
                print 'WALL-TIME EXCEEDED for PID', t[key].pid, ':', t[key].remote
                if kill: t[key].abort()
            passive -= 1
    return passive

def get_passive(t):
    '''
    returns the list of RSH threads that are passive
    '''
    passive = []
    for key in t.keys():
        if not t[key].isAlive():
            passive.append(key)
    return passive

def printout(res,shawtime):
    '''
    print thread results
    '''
    if res.isAlive():
        print 'WARNING: trying to kill again the process that should be gone by now'
        print ' / '.join([res.remote,str(res.ppid),str(res.pid)])
        res.abort()
    dummy = res.host.split()
    if ( len(dummy) > 1 ): dummy = '@'.join(dummy[1:])
    else: dummy = dummy[0]
    hostname = dummy
    hostcmd = res.cmd
    hostout = res.contents
    timing = res.etime-res.stime
    if shawtime:
        print
        print hostname+':','COMMAND:',hostcmd
        print hostname+':','START-TIME:',res.stime
    for line in hostout:
        print hostname+':',line,
    if shawtime:
        print hostname+':','END-TIME:',res.etime
        print hostname+':','WALL-TIME:',timing
    sys.stdout.flush()
    return res.status

def get_nodes(nodelist):
    '''
    get list of nodes from the file
    '''
    try:
        nodes = open(nodelist,'r').readlines()
    except:
        print 'FATAL ERROR: file',nodelist,'not found'
        sys.exit(1)
    nodes = (''.join(nodes)).splitlines()
    # fix nodes syntax if users specified
    for i in range(len(nodes)):
        dummy = nodes[i].split('@')
        if ( len(dummy) > 1 ):
            nodes[i] = ' '.join(['-l']+dummy)
    return nodes

def get_cmds(cmdlist,exedir):
    '''
    get list of commands from the file
    end append common execution directory if not None
    '''
    try:
        cmds = open(cmdlist,'r').readlines()
    except:
        print 'FATAL ERROR: file',cmdlist,'not found'
        sys.exit(1)
    cmds = (''.join(cmds)).splitlines()
    # add execution directory
    if exedir:
        for i in range(len(cmds)):
            cmds[i] = 'cd '+exedir+' && '+cmds[i]
    return cmds

