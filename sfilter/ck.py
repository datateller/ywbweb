import jpype
from multiprocessing import Process, Pipe
from bloomfilter import bf
import os

def java_loop(pipe):
    classpath = ".:IKAnalyzer2012_u6.jar"
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % classpath) 
    print os.getcwd()
    checkclass = jpype.JClass("Segmenter")
    while True:
        checkobj = checkclass(pipe.recv())
        for item in checkobj.CutWord(): 
            print item 
            if bf.lookup(item.encode('utf-8')):
                pipe.send("false")
                break
        else:
            pipe.send("true")

parent, child = Pipe()
p = Process(target=java_loop, args=(child,))
p.daemon = True
p.start()
                
       
    
