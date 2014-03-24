import jpype
import os
from sfilter.bloomfilter import bf
import ywbweb.settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ywbweb.settings")
from merchant.models import *

if __name__ == "__main__":
  classpath = ".:./sfilter/IKAnalyzer2012_u6.jar" 
  jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % classpath)
  print(os.getcwd())
  checkclass = jpype.JClass("Segmenter")

  #contentcol = Commercial.objects.all()
  #o1=checkclass("hello, my name is xueyu")
  #b=o1.CutWord()
  #print(b)
  #print(type(b))
  #for i in range(len(b)):
  #  print(b[i])
  

  for obj in Commercial.objects.all():
    checkobj = checkclass(obj.content)
    isvalid = True
    words = checkobj.CutWord()
    for i in range(len(words)):
    #for item in checkobj.CutWord():
      item = words[i]
      print(item)
      if bf.lookup(item.encode('utf-8')):
        isvalid = False
        break
    if not isvalid:
      print("contain sensitive infomation")
      #obj.content = ""
      #obj.save()
    else:
      print(obj.content)

 
   
