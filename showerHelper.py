import discord
from discord.utils import get
from icecream import ic
import youtube_dl

def get_song(query):
    ytdl_format_options = {
        'format': 'bestaudio/best',
        'restrictfilenames': True,
        'noplaylist': True,
        'key': 'FFmpegExtractAudio',
        'extractaudio': True,
        'audioformat': 'mp3',
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
        }
    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
    info = ytdl.extract_info(query, download=False)
    
    url = {} #make url object to store info abt video
    if info['_type'] == 'playlist': #if it is a playlist pick the top one
        url['audio'] =  info['entries'][0]['url'] #get vid url
        url['title'] =  info['entries'][0]['title'] #get vid title
        url['webpage'] = info['entries'][0]['webpage_url'] #get vid title
        url['duration'] = info['entries'][0]['duration'] #get vid duration
    else:
        url['audio'] =  info['entries']['url'] #get vid url
        url['title'] =  info['entries']['title'] #get vid title
        url['webpage'] = info['entries']['webpage_url'] #get vid title
        url['duration'] = info['entries'][0]['duration'] #get vid duration

    return url #return url with vid info
    
def makeString(args):
    text = "" #get text string from args
    for arg in args: 
        text = text + " " + arg #add to text string
    return text

def embedBuilder(title = None, description = None, fields = None, colour = 0x00D31F, image = None, url = None, type = 'rich'):
    
    embed = discord.Embed( #make embed object
            title = title, #set title
            type = type, #set type
            colour=colour) #set color
    if description != None: #if there is a description, add it
        embed.description = description

    if url != None: #if there is a url, add it
        embed.url=url

    if fields != None: #if there are fields add them
        for entry in fields: #for each field
            embed.add_field(name=entry[0], value=entry[1], inline=entry[2]) #title, value, inline? (T/F)
    return embed #return embed

def timeFormat(sec): #format seconds to HH:MM:SS
    timeObjects = [sec / 3600, sec / 60, sec % 60]

    timeObjects = [sec / 3600, sec / 60, sec % 60]

    for idx in range(3):  #add zeros to time objects and save as strings
        time = timeObjects[idx]
        if time < 10: #if less than 10, add 0 in front
            timeObjects[idx] = "0" + str(int(time))
        else: 
            timeObjects[idx] = str(time)

    if int(timeObjects[0]) > 0: # if there are hours include them, otherwise omit
        format = f'{timeObjects[0]}:{timeObjects[1]}:{timeObjects[2]}'
    else:
        format = f'{timeObjects[1]}:{timeObjects[2]}'

    return format #return formatted time string