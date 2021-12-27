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
    
    url = {}
    if info['_type'] == 'playlist':
        url['audio'] =  info['entries'][0]['url']
        url['title'] =  info['entries'][0]['title']
        url['webpage'] = info['entries'][0]['webpage_url']
    else:
        url['audio'] =  info['entries']['url']
        url['title'] =  info['entries']['title']
        url['webpage'] = info['entries']['webpage_url']
    return url
    
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
