#!/usr/env/python

import threading
import datetime
import time
import os
import asyncio
from dotenv import load_dotenv

from discord.ext import tasks, commands
import discord

import ships

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class PrimeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.ship_list = ships.VehicleList()
        self.msg_list = []
        self.update_ship_msg.start()
    async def on_ready(self):
        pass

    @tasks.loop(seconds=3)
    async def update_ship_msg(self):
        for msg in self.msg_list:
            await msg.edit(content=str(self.ship_list))

    @update_ship_msg.before_loop
    async def wait_for_bot(self):
        await self.wait_until_ready()

activity = discord.Activity(name='Male Vieras', type=discord.ActivityType.watching)
client = PrimeBot(command_prefix='!primebot ',activity=activity)

@client.command()
async def test_cmd(ctx):
    await ctx.send("bot command worked lol :thumbup:")

@client.command()
async def clear_ships(ctx):
    client.ship_list.clear()
    for msg in client.msg_list:
        await msg.edit(content=str(client.ship_list))

@client.command()
async def add_airship(ctx, name: str, rank: int):
    new_ship = ships.Vehicle(name, rank)
    current_ships = client.ship_list.airships
    current_ships.append(new_ship)
    client.ship_list.update_airships(current_ships)
    for msg in client.msg_list:
        await msg.edit(content=str(client.ship_list))

@client.command()
async def list_ships(ctx):
    new_message = await ctx.send(str(client.ship_list))
    client.msg_list.append(new_message)

@client.command()
async def male_viera(ctx):
    viera_date = datetime.datetime(2021,11,23,6)
    time_delta = str(viera_date - datetime.datetime.now())
    await ctx.send("Bunny boi countdown: {}".format(time_delta))

client.run(TOKEN)
