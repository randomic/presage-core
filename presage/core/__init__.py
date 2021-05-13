import logging

from .control import Control
from .extensions import Extensions


logger = logging.getLogger(__name__)


def setup(bot):
    bot.add_cog(Control(bot, logger, __name__))
    bot.add_cog(Extensions(bot, logger, __name__))
