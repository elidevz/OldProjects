import discord
from discord.ext import commands
import asyncio
import time
import os
from discord.ext.commands import cooldown, BucketType
from discord.ext import commands
from discord.utils import get
import requests
from discord import CategoryChannel
import json




prefix = '?'
client = commands.Bot(command_prefix=prefix)
TOKEN = ''
SELLIXAPI = ''
MERCHANT = ''

with open('product_config.json', 'r') as f:
    PRODUCTDATA = json.load(f)

@client.event
async def on_ready():
    os.system('cls')
    print('Bot launched as {0.user}'.format(client))
    print('Prefix is {prefix}'.format(prefix))

@client.command()
async def claim(ctx, *, arg):
    if ctx.channel.type == discord.ChannelType.private:

        with open('oldorders.txt', 'r') as f:
            if arg in f.read():
            
                await ctx.send('Order already claimed!')
                await ctx.send('Verifying order...')

                headers = {
                    'Authorization': 'Bearer ' + SELLIXAPI,
                    'X-Sellix-Merchant': MERCHANT
                }
                
                r = requests.get('https://dev.sellix.io/v1/orders/' + arg, headers=headers)
                sellix = r.json()


                if sellix['error'] == 'Invoice Not Found':
                    await ctx.send('Order not found.')
                else:
                    if sellix['status'] == 200:

                        order_product = sellix['data']['order']['product_title']

                        for i in PRODUCTDATA:
                            if i['product'] == order_product:
                                await ctx.send('Order found, claiming...')
                                await ctx.send('Order is for {product}'.format(product=order_product))
                                with open('oldorders.txt', 'a') as f:
                                    f.write(arg + '\n')
                                filename = i['file']
                                await ctx.send(file=discord.File(filename)) 
                                await ctx.send('Enjoy!')

                    else:
                        await ctx.send('Failure while checking order, please contact support. Error code: ' + sellix['status'])
    else:
        await ctx.send('Please DM me to claim!')



client.run(TOKEN)
