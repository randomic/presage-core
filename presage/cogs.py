import logging

from discord.ext import commands


class BasePresageCog(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger, extension: str):
        self.bot = bot
        self.logger = logger.getChild(self.qualified_name)
        self.extension = extension


class OwnerCog(BasePresageCog):
    async def cog_check(self, ctx: commands.Context):
        return await commands.is_owner().predicate(ctx)
