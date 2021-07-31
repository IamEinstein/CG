import discord
from discord.ext import commands
import itertools


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            "help": "Show help about the bot, a command, or a category."})

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    def make_page_embed(self, commands, title="Chronic Help", description=discord.Embed.Empty):
        embed = discord.Embed(
            color=0xFE9AC9, title=title, description=description)
        embed.set_footer(
            text=f'Use "cg!help command" for more info on a command.'
        )

    def make_default_embed(self, cogs, title="Categories", description=discord.Embed.Empty):
        embed = discord.Embed(
            color=0xFE9AC9, title=title, description=description)
        counter = 0
        for cog in cogs:
            cog = cog
            description = cog.description
            description = f"{description or 'No Description'} \n {''.join([f'`{command.qualified_name}` ' for command in cog.commands])}"
            embed.add_field(name=cog.qualified_name,
                            value=description, inline=False)
            counter += 1

        return embed

    async def send_bot_help(self, mapping):
        cogs = []
        for cog in mapping:
            print(cog)
            # await self.get_destination().send(f'{cog.qualified_name}:{[command.name for command in mapping[cog]]}')
            if isinstance(cog, commands.Bot):
                pass
            else:
                cogs.append(cog)

        embed = self.make_default_embed(cogs,
                                        title=f"CG Bot Command Categories )",
                                        description=(
                                            f"Use `cg!help <command>` for more info on a command.\n"
                                            f"Use `cg!help <category>` for more info on a category."
                                        ),
                                        )
        return await self.bot.send(embed=embed)

    async def send_cog_help(self, cog):
        ctx = self.context
        ctx.invoked_with = "help"
        bot = ctx.bot
        commands = bot.commands

        filtered = await self.filter_commands(cog.get_commands(), sort=True)

        embed = self.make_page_embed(
            filtered,
            title=(cog and cog.qualified_name or "Other") + " Commands",
            description=discord.Embed.Empty if cog is None else cog.description,
        )

        await ctx.send(embed=embed)

    async def send_group_help(self, group):
        ctx = self.context
        ctx.invoked_with = "help"
        bot = ctx.bot

        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        filtered = await self.filter_commands(subcommands, sort=True)

        embed = self.make_page_embed(
            filtered,
            title=group.qualified_name,
            description=f"{group.description}\n\n{group.help}"
            if group.description
            else group.help or "No help found...",
        )

        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            color=0xFE9AC9, title=f"cg!{command.qualified_name}"
        )

        if command.description:
            embed.description = f"{command.description}\n\n{command.help}"
        else:
            embed.description = command.help or "No help found..."

        embed.add_field(name="Signature",
                        value=self.get_command_signature(command))

        await self.context.send(embed=embed)


def setup(bot):
    bot.old_help_command = bot.help_command
    bot.help_command = CustomHelpCommand()


def teardown(bot):
    bot.help_command = bot.old_help_command
