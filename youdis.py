#!/usr/bin/env python3
'''
youdis v1.1
bot for downloading youtube videos using yt-dlp
discord-py-interactions 5.11.0 has new option
   requires python>=3.9
'''
# match_filter: info_dict -> Raise utils.DownloadCancelled(msg) ? interrupt

import interactions
from os import getenv
from pathlib import Path
import yt_dlp
import json
import asyncio
import threading

userFile = Path('/config/users.json')
userFile.touch(exist_ok=True)

bot = interactions.Client(intents=interactions.Intents.DEFAULT,default_scope=2147491904)

userFile.parent.mkdir(exist_ok=True, parents=True)
try:
    with open(userFile, 'x') as f:
        print(f'users.json not found; saving to {userFile}')    
except FileExistsError:
    with open(userFile, 'r') as f:
        authorized_users = json.load(f).get('authorized_users')
    print(f'authorized_users:{authorized_users}')
    
title = ''

async def send_message(ctx, message):
    await ctx.author.send(message)

def download_video(url, options):
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(url)
        
def create_hook(ctx,loop):
    def hook(d):
        global title
        status = d.get('status')
        if status == 'error':
            msg = f'error; video probably already exists, have you checked archive.txt'
            asyncio.run_coroutine_threadsafe(send_message(ctx,msg),loop)
        elif d.get('info_dict').get('title') != title:
            title = d.get('info_dict').get('title')
            playlist_index = d.get('info_dict').get('playlist_index')
            playlist_count = d.get('info_dict').get('playlist_count')
            filename = d.get('filename')
            url = d.get('info_dict').get('webpage_url')
            msg = f'{status} {playlist_index} of {playlist_count}: {filename} <{url}>'
            asyncio.run_coroutine_threadsafe(send_message(ctx,msg),loop)
    return hook

@interactions.slash_command(name="youtube",description="download video from youtube to server")
@interactions.slash_option(
    name='url',
    opt_type=interactions.OptionType.STRING,
    required=True,
    description='url target'
)
async def youtube(ctx: interactions.SlashContext, url:str):
    print(f'{ctx.author.id} requested {url}')
    loop = asyncio.get_running_loop()
    hook = create_hook(ctx,loop)
    msg = ''
    # use api_to_cli and paste cli options to get the output you need
    yoptions = {
        'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'fragment_tries': 10,
        'restrictfilenames':True,
        'paths': {'home':'/downloads'},
        'retries':10,
        'writeinfojson':False,
        'allow_playlist_files':True,
        'noplaylist':True,
        'download_archive':'/config/archive.txt',
        'progress_hooks':[hook],
        'outtmpl': '%(uploader)s/%(playlist_title)s/%(playlist_index)s%(playlist_index& - )s%(title)s.%(ext)s',
        'outtmpl_na_placeholder':'',
    }
    # check that user is authorized
    if ctx.author.id not in authorized_users:
        if ctx.author.id == 127831327012683776:
            await ctx.author.send('potato stop')
        await ctx.author.send('you are not authorized to use this command. message my owner to be added.')
        return
    else:
        await ctx.channel.send(f'Downloading from <{url}>. Status updates via DM.')
        #await ctx.defer()  #if you need up to 15m to respond

        # 1/2 - download in separate thread, else progress_hook blocks downstream async ctx.send
        download_thread = threading.Thread(target=download_video, args=(url,yoptions))
        download_thread.start()
        await asyncio.to_thread(download_thread.join)

        # 2/2 - replace the above with this next try:
        #try:
        #    await asyncio.to_thread(download_video, url, yoptions)
        #except Exception as e:
        #    print(f"download failed: {e}")
        #    await ctx.author.send(f"download failed: {str(e)}")


@interactions.slash_command(name="interrupt",description="cancel current job")
@interactions.check(interactions.is_owner())
async def _interrupt(ctx):
    # interrupt here
    print('interrupting current job - not implemented')
    await ctx.author.send('interrupting current job - not implemented')
    
@interactions.slash_command(name="adduser",description="authorize target user")
@interactions.slash_option(
    name="user",
    opt_type=interactions.OptionType.USER,
    required=True,
    description='enable this bot for target user',
)
@interactions.check(interactions.is_owner())
async def _adduser(ctx: interactions.SlashContext, user:interactions.OptionType.USER):
    if str(user.id) not in authorized_users:
        authorized_users.append(str(user.id))
        with open(userFile,'w') as f:  #overwrite file - fix later if other params come up
            json.dump({'authorized_users':authorized_users})
        print('react:checkmark')
        await ctx.message.add_reaction('✅')

@interactions.slash_command(name="removeuser",description="deauthorize target user")
@interactions.slash_option(
    name="user",
    opt_type=interactions.OptionType.USER,
    required=True,
    description='disable this bot for target user',
)
@interactions.check(interactions.is_owner())
async def _removeuser(ctx: interactions.SlashContext, user:interactions.OptionType.USER):
    if str(user.id) in authorized_users:
    # ? ? ? fix pls
        i = index(authorized_users(str(user.id)))

        # update list, rewrite json
            
        print('react:checkmark')
        await ctx.message.add_reaction('✅')

async def dl_hook(d):
    msg = f'{d["status"]} {d["filename"]}'
    print(msg)
    await ctx.author.send(msg)

api_token = getenv('api_token')
if not api_token:
    raise ValueError('API token not set. Retrieve from your Discord bot.')
bot.start(api_token)
