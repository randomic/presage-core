import argparse
import logging

from discord.ext import commands


class Presage:
    def __init__(self, command_prefix: str):
        self.logger = logging.getLogger("presage")
        self.logger.info("Initialising Presage...")
        self.bot = commands.Bot(commands.when_mentioned_or(command_prefix))
        self.bot.load_extension("presage.core")

    def run(self, token):
        self.bot.run(token)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("token", type=str)
    parser.add_argument("command_prefix", type=str, nargs="?", default="!")
    parser.add_argument("--debug")

    args = parser.parse_args()
    logging.basicConfig(
        format="%(asctime)s - %(levelname)8s - %(name)s - %(message)s",
        level=logging.DEBUG if args.debug else logging.INFO
    )
    Presage(args.command_prefix).run(args.token)
