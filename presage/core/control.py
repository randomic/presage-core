import asyncio

from discord.ext import commands

from presage.cogs import OwnerCog


class Control(OwnerCog):
    @commands.command()
    async def stop(self, ctx: commands.Context):
        await ctx.send("Goodbye, World!")
        asyncio.run_coroutine_threadsafe(self.bot.close(), self.bot.loop)
