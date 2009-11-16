import time
import sys
from subprocess import Popen, PIPE, STDOUT



def runTest(args):
    cmd="python "+args    
    if sys.platform == "linux2":
        close_fds = True
    else:
        close_fds = False  
    pipe = Popen(cmd, bufsize=1,stdin=PIPE, stdout=PIPE, stderr=PIPE, shell = True, close_fds=close_fds)
    test, testerr=pipe.communicate()

    
def timer(function, *args):
    start=time.time()
    function(*args)
    stop=time.time()
    return (stop-start)
    
print timer(runTest,'patLayer1_fromAOD_fast_cfg.py')
print timer(runTest,'patLayer1_fromAOD_fast_ParameterSet_patch_cfg.py')
