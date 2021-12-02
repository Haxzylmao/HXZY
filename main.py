import os
import discord
from discord.ext import commands
from server import keep_alive
from discord_components import *
from discord_components import DiscordComponents
from discord_slash import SlashCommand
from discord_slash import *
from server import keep_running


EXTENSIONS = ['extensions.General', 'extensions.Errors', 'extensions.Moderation', 'extensions.Ready', 'extensions.Message', 'extensions.Music', 'extensions.Help', 'extensions.Slash']
intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = "*",
            help_command = None,
            intents = intents
        )

        self.owner_id = 720590595839754340
        self.bot_id = 879819844537692160
        self.token = os.environ['TOKEN']
        DiscordComponents(self)
        slash = SlashCommand(self, sync_commands = True)
        for extension in EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e: # Returns an error if the bot is unable to load an extension
                print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))



        async def on_ready(self): # On ready stuff
            print('Online! as:')
            print('Username | ' + self.user.name)
            print('ID | ' + self.user.id)


        async def run(self):
            super().run(self.token)

if __name__ == '__main__':
    HXZY = Bot()
    keep_running()
    HXZY.run(os.environ['TOKEN'])
