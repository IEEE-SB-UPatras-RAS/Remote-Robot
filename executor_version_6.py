from os import listdir
from os.path import isfile, join
import subprocess
import time
path='/home/pi/Projects/remote_bot/execBot/'
print("executor")
def execute(filename):
  print("running:",filename)
  process_to_execute=subprocess.Popen(["python3", path+"codes/{}".format(filename)])
  process_to_execute.wait()
  #return process_to_execute
  return


while(True):
  time.sleep(0.5)
  #print('hi')
  file= open(path+"registry/total_back_index.txt","r")
  total_index=int(file.read())
  file.close()
  mypath='codes/'
  code_list = [f for f in listdir(path+mypath) if isfile(join(path+mypath, f))]
  code_list=sorted(code_list, key=lambda x: int(x.split(" ")[0]))
  #print(code_list)
  for i in code_list:

    if int(i.split(" ")[0])> total_index:
      time.sleep(0.1)
      file= open(path+"registry/total_back_index.txt","w")
      total_index=total_index+1
      file.write(str(total_index))
      file.close()
      execute(i)
      
  
      
  
  
  
