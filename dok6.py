print("bot")

#########################################_IMPORTS_#####################################
from datetime import datetime
import discord
import os
from os.path import exists
import time
import requests
import shutil

print('first step')

####################################################################_DEFS_############################
def stbi(path,message):
        msg = message.content
        file= open(path+"registry/total_back_index.txt","r")
        data=file.read()
        if data.isdigit():
                data=int(data)
        else:
                data=0
                print('tbi was corrupted')
        while(True):
                try:
                        file= open(path+"registry/total_back_index.txt","w")
                        break
                except:
                        continue
        if '*' in msg:
                file.write(str(0))
                print('stbi set to 0')
        elif 'decrease by' in msg:
                file.write(str(data-int(msg.split(" ")[3])))
                print('stbi set to {}'.format(str(data-int(msg.split(" ")[3]))))
        elif 'increase by' in msg:
                file.write(str(data+int(msg.split(" ")[3])))
                print('stbi set to {}'.format(str(data+int(msg.split(" ")[3]))))
        elif 'to' in msg:
                file.write(msg.split(" ")[2])
                print('stbi set to {}'.format(msg.split(" ")[2]))
        else:
                file.write(str(data))
                print('failed to change tbi')
                
        file.close()
        
        return

def stfi(path,message):
        msg = message.content
        file= open(path+"registry/total_front_index.txt","r")
        data=file.read()
        if data.isdigit():
                data=int(data)
        else:
                data=0
                print('tbi was corrupted')
        while(True):
                try:
                        file= open(path+"registry/total_front_index.txt","w")
                        break
                except:
                        continue
        if '*' in msg:
                file.write(str(0))
                print('stfi set to 0')
        elif 'decrease by' in msg:
                file.write(str(data-int(msg.split(" ")[3])))
                print('stfi set to {}'.format(str(data-int(msg.split(" ")[3]))))
        elif 'increase by' in msg:
                file.write(str(data+int(msg.split(" ")[3])))
                print('stfi set to {}'.format(str(data+int(msg.split(" ")[3]))))
        elif 'to' in msg:
                file.write(msg.split(" ")[2])
                print('stfi set to {}'.format(msg.split(" ")[2]))
        else:
                file.write(str(data))
                print('failed to change tfi')
                
        file.close()
        
        return 

def get_contestants(path):
        file= open(path+"registry/contestants.txt","r")
        data=file.read()
        contestants=data.split("\n")
        file.close()
        
        return contestants

def manage_attempt(path,contents,message):
        if len(message.attachments)==0:
                print('no attachment')
                return
        if message.attachments[0].url[-3:]!='.py':
                print('not a python file')
                return
        file= open(path+"registry/total_front_index.txt","r")
        data=int(file.read())
        while(True):
                try:
                        file= open(path+"registry/total_front_index.txt","w")
                        break
                except:
                        continue
        file.write(str(data+1))
        file.close()
        total_index=str(data+1)
        save_code(total_index+' '+contents[0],message,path)

        return

def add_contestant(path,msg):
        file= open(path+"registry/contestants.txt","a")
        file.write(msg.split(" ")[2]+'\n')
        file.close()
        file= open(path+"registry/contestants.txt","r")
        data=file.read()
        contestants=data.split("\n")
        file.close()
        print('contestant {} was added'.format(msg.split(" ")[2]))
        
        return

def flush(queue_name,message,path):
        watchdog=0
        print("flushing {} ...".format(queue_name))
        while (True):
            try:
                if exists(path+"temp/{}.txt".format(queue_name)):
                        os.remove(path+"temp/{}.txt".format(queue_name))
            except:
                continue
            try :
                text_file_1= open(path+"temp/{}.txt".format(queue_name),"a")
            except:
                continue
            try :
                if watchdog==0:
                    date=datetime.now()
                    metadata="datetime of last flush:{}|user who flushed:{}|user id:{}".format(date.strftime("%d/%m/%Y %H:%M:%S"),message.author, message.author.id)
                    text_file_1.write("START of {} //info: {}\n".format(queue_name,metadata))
                    watchdog=1
            except BaseException as e:
                print(e)
            try :
                text_file_1.close()
                print("{} flushed and ready to use".format(queue_name))
                break
            except:
                continue
        return

def record_message(message,queue_name,msg,path):
        watchdog=0
        print('record')
        while (True):
                try :
                        if exists(path+"temp/{}.txt".format(queue_name)):
                                text_file_1= open(path+"temp/{}.txt".format(queue_name),"a")
                        else:
                                text_file_1= open(path+"temp/{}.txt".format(queue_name),"a")
                                date=datetime.now()
                                metadata="datetime:{}|user who flushed:{}|user id:{}".format(date.strftime("%d/%m/%Y %H:%M:%S"),"initialisation", "initialisation")
                                text_file_1.write("START of {} //info: {}\n".format(queue_name,metadata))

                except Exception as ex:
                    print(ex.message)
                    continue
                try :
                    if watchdog==0:
                        date=datetime.now()
                        metadata="{}|{}|{}".format(date.strftime("%d/%m/%Y %H:%M:%S"),message.author, message.author.id)
                        text_file_1.write("$"+"metadata:"+metadata+"\n"+msg+"$"+'\n')
                        watchdog=1
                except Exception as ex:
                    print(ex.message)
                    continue
                try :
                    text_file_1.close()
                    print("message pushed in {}".format(queue_name))
                    break
                except Exception as ex:
                    print(ex.message)
                    continue
        return


def save_code(name,message,path):
        string_url=message.attachments[0].url
        r = requests.get(string_url, stream = True)
        with open(path+"codes/{}.py".format(name),'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
        print('code saved')
        return









########################_front_end_#######################################
print('2 step')
### dunno ###
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
guild = discord.Guild
###
print('3 step')
### initialize specific to application variables ###
path='/home/pi/Projects/remote_bot/execBot/'
channel_id_commands = 869497291889844304
admins=[861659870809948210,385342519853973504]
file= open(path+"registry/contestants.txt","r")
data=file.read()
contestants=data.split("\n")
file.close()

###

print('4 step')

@client.event
async def on_message(message):
        
        ### get message's text content ###
        msg = message.content
        ###
        
        ### check if message is from admin ###
        admin=False
        if message.author.id in admins:
                admin=True
        ###

        ### ignore unrelated messages that the bot is receiving ###
        if admin==False:
                if message.author == client.user:
                        return
                if not message.guild:
                        return
                if message.channel.id != channel_id_commands:
                        return
        
        if len(msg)==0:
                return
        ###




        ### push the message in the temp buffer (Queue1) and in the history (Log1) ###
        record_message(message,"Queue1",msg,path)
        record_message(message,"Log1",msg,path)
        ###
            
        ### check if an admin wants to flush a buffer/log (specified from admin's message in ""flush ''buffer's_name''"" formated message) ###
        if msg[0:5]=="flush" and admin==True:
                flush(msg.split(" ")[1],message,path)
        ###

        ### check if an admin wants to modify the total_front_index a.k.a. TFI (set total front index -> stfi)  ###
        if ("stfi" in msg) and admin==True:
                stfi(path,message)

        ###

        ### check if an admin wants to modify the total_back_index a.k.a. TBI (set total back index -> stfi)  ###
        if ("stbi" in msg) and admin==True:
                stbi(path,message)

        ###
                
        ### check for an attempt and if there is one store the code and increase the TFI ###
        contents=''
        try:
                contents=msg.split(" ")
        except:
                pass
        if len(contents) >=2:
                contestants=get_contestants(path)
            
                if contents[0] in contestants and contents[1]=="attempt" :
                        manage_attempt(path,contents,message)       
        ###
                        
        ### check if an admin wants to add a contestant  ###
        if "add contestant" in msg and admin==True:
                add_contestant(path,msg)

        ###

        ### check if an admin wants to add a new admin ###
        if "add new admin" in msg and admin==True:
                add_admin(path,msg[3])

        ###
                    

        return


     
def bot():
  client.run('ODY5NDk1NzA0NjY0NTM5MjI2.YP_C-g.lbtXG7Dgl1c-bXdJXUJ8nE6Bmcs')



      
      
##MAIN###


bot()




















  
