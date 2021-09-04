import os
import sys
import json
import string
import time
from discord.ext import commands

from support.Pokemon import Pokemon




if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

class Rank(commands.Cog, name='rank'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='great')
    async def great(self, ctx, argName, arg1: int, arg2: int, arg3: int):
        
        
        argName = string.capwords(argName)

        poke = Pokemon(argName, arg1, arg2, arg3)
        poke.get_selected_info()
        poke.find_nearest_level_great()
        poke.find_nearest_cpm()
        poke.find_statproduct()
        poke.sortby_statproduct()
        poke.find_user_choice_rank()


        await ctx.send('Great League\n' + poke.name + '\n' + 'IVs: ' + str(arg1) + ' ' + str(arg2) + ' ' + str(arg3) + '\n' +
                    'Rank: ' + str(poke.rank) + '\n' + 'Level: ' + str(poke.level) + '\n' + 'CP: ' + str(poke.CP))
                    
    @commands.command(name='ultra')
    async def ultra(self, ctx, argName, arg1: int, arg2: int, arg3: int):
        
        
        argName = string.capwords(argName)

        poke = Pokemon(argName, arg1, arg2, arg3)
        poke.get_selected_info()
        poke.find_nearest_level_ultra()
        poke.find_nearest_cpm()
        poke.find_statproduct()
        poke.sortby_statproduct()
        poke.find_user_choice_rank()


        await ctx.send('Ultra League\n' + poke.name + '\n' + 'IVs: ' + str(arg1) + ' ' + str(arg2) + ' ' + str(arg3) + '\n' +
                    'Rank: ' + str(poke.rank) + '\n' + 'Level: ' + str(poke.level) + '\n' + 'CP: ' + str(poke.CP))
                    


def setup(bot):
    bot.add_cog(Rank(bot))
