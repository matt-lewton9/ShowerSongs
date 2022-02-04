import discord
from discord.ext import commands
from coronaHelper import *
import os

class Sounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='$t /text/ -> Text to speech') #text to speech
    async def t(self, ctx, *args):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #get voice client

        if voice.is_playing(): #stop audio currently being played
            voice.stop()
        
        text = makeString(args)

        filename = "tts.mp3" #make mp3 filename
        tts(text, filename) #make audiofile

        audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="C:/Users/black/ffmpeg/bin/ffmpeg.exe", source=filename))

        if not voice.is_playing():
            voice.play(audio_source, after = None) #play file

    @commands.command(brief = 'Join voice call') #join VC
    async def join(self, ctx):
        await ctx.guild.voice_channels[0].connect() #Join VC, make voice client

    @commands.command(brief='$play /filename/ -> Play soundboard file, do not add .mp3') #play mp3
    async def play(self, ctx, *args):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #get voice client
        if voice == None: #if voice client doesn't exist, print error message
            await ctx.send("I am not in the call!!!")
        else:
            if voice.is_playing(): #stop audio currently being played
                voice.stop()

            filename = args[0] #get filename
            filename = "./audio/"+filename+".mp3" #make path

            if os.path.exists(filename): #check if file exists
                audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="C:/Users/black/ffmpeg/bin/ffmpeg.exe", source=filename))
                if not voice.is_playing():
                    voice.play(audio_source, after = None) #play file
            else:
                await ctx.send("Impossible. Perhaps the archives are incomplete.") #if it doesn't exist, play error message

    @commands.command(brief = 'Display list of current sound files')
    async def soundboard(self, ctx):
        files = os.listdir('audio/') #get file list
        file_string = "" #string of filenames
        for file in files: # add newlines between the filenames
            file_string += file + "\n"
        await ctx.send(f"**Soundboard Files**:```\n{file_string}```") #send filenames   

    @commands.command(brief = 'Leave voice call') #leave call
    async def leave(self, ctx, description='Leave VC'):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #get voice client
        await voice.disconnect() #disconnect voice client
        await ctx.send("Farewell Comrades :flag_al:") #send leaving message

    @commands.command(brief = 'Stop audio playing') #stop audio
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #get voice client
        await voice.stop() #stop audio

def setup(bot):
    bot.add_cog(Sounds(bot))