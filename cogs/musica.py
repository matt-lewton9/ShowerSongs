import discord
from discord.ext import commands
from showerHelper import *
import os

#hexidecimal color code constants
GREEN= 0x00D31F

class Musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot #make bot
        self.queue = [] #empty queue
        self.now_playing = "None" #init no song playing

    @commands.command(brief='Play song from Youtube, or add it to the Queue', aliases=['play'])
    async def p(self, ctx, *args):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #get voice client
        if voice == None: #if voice client doesn't exist, print error message
            voice = await ctx.guild.voice_channels[0].connect() #Join VC, make voice client

        song_url = {}
        query = makeString(args) #get text string from message
        song_url = get_song(query) #get song url from ytdl

        self.queue.append(song_url) #add song url to queue
        embed = embedBuilder(title=f"{song_url['title']} Added to Queue", url=song_url['webpage'])#make embed
        await ctx.send(embed = embed) #send embed

        await self.play_next(ctx) #play next queued

    @commands.command(brief = 'Show queue', aliases=['queue']) #clear queue
    async def q(self, ctx):
        
        fields = [] #fields array
        if len(self.queue) != 0:
            i = 0 #song counter
            for song in self.queue:
                i += 1 #append to song counter
                fields.append([f"{i}: {song['title']}", song['webpage'], False]) #add to fields array
            embed = embedBuilder(title="Queue", fields=fields)#make embed with filds
        else:
            embed = embedBuilder(title="Queue", description="None")#make embed for empty queue
        await ctx.send(embed = embed) #send embed

    @commands.command(brief = 'Clear queue') #clear queue
    async def clear(self, ctx):
        self.queue = []
        embed = embedBuilder(title="Queue Cleared!")#make embed
        await ctx.send(embed = embed) #send embed
    
    @commands.command(brief='Skip to next song', aliases=['skip'])
    async def s(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #get voice client
        embed = embedBuilder(title=f"{self.now_playing['title']} Skipped!", url=self.now_playing['webpage'])#make embed
        await ctx.send(embed = embed) #send embed
        voice.stop() #stop audio
        if len(self.queue) != 0: #if queue is not empty:
            await self.play_next(ctx) #play next song

    @commands.command(brief = 'Display song now playing') #clear queue
    async def np(self, ctx):
        if self.now_playing == 'None':
            embed = embedBuilder(title='**Now Playing**', description="None") #if nothing is playing, np is none
        else:
            embed = embedBuilder(title=f'**Now Playing: {self.now_playing["title"]}**\n{self.now_playing["webpage"]}', url=self.now_playing['webpage'])#make embed
        await ctx.send(embed = embed) #send embed

    @commands.command(brief = 'Leave voice call') #leave call
    async def leave(self, ctx, description='Leave VC'):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #get voice client
        await voice.disconnect() #disconnect voice client
        embed = embedBuilder(title="Farewell Comrades :flag_al:", url="https://www.youtube.com/watch?v=Yg03q100E4g")#make embed
        await ctx.guild.channels[-1].send(embed = embed) #send leaving message

    @commands.command(brief = 'Pause audio playing') #pause audio
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #get voice client
        embed = embedBuilder(title=f"{self.now_playing['title']} Paused", url=self.now_playing['webpage'])#make embed
        await ctx.send(embed = embed) #send embed
        await voice.pause() #pause audio

    @commands.command(brief='!rm /#/ -> Remove a song from queue', aliases =['remove'])
    async def rm(self, ctx, *args):
        target = int(args[0]) #get target song from args
        mortal = self.queue[target - 1] #get song to be removed
        self.queue.pop(target - 1) #remove song from queue
        embed = embedBuilder(title=f"{mortal['title']}, song #{target} removed from Queue", url=mortal['webpage'])#make embed
        await ctx.send(embed = embed) #send embed
        await self.q(ctx) #show current queue

    @commands.command(brief = 'Resume audio playing') #resume audio
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #get voice client
        embed = embedBuilder(title=f"{self.now_playing['title']} Resumed", url=self.now_playing['webpage'])#make embed
        await ctx.send(embed = embed) #send embed
        await voice.resume() #resume audio

    async def play_next(self, ctx): #play next song in queue
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) #get voice client

        if len(self.queue) == 0: #if queue is empty, say so
            await ctx.send("Queue is empty")
            self.now_playing = 'None'
            await self.leave(ctx)
        else:
            if not voice.is_playing():
                self.now_playing = self.queue[0] #set now playing
                self.queue.pop(0) #remove song from queue
                audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="C:/Users/black/ffmpeg/bin/ffmpeg.exe", source=self.now_playing['audio'])) #get audio source
                voice.play(audio_source, after = lambda error: self.bot.loop.create_task(self.play_next(ctx))) #play file
                embed = embedBuilder(title="Now Playing:", fields=[[self.now_playing['title'], self.now_playing['webpage'], False]]) #create embedded message
                await ctx.send(embed = embed) #send embed message

def setup(bot): #set up cog
    bot.add_cog(Musica(bot))