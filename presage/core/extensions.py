from discord.ext import commands

from presage.cogs import OwnerCog


class CannotUnloadCoreExtension(commands.ExtensionError):
    def __init__(self, name):
        super().__init__("Cannot unload the core extension.".format(name), name=name)


class Extensions(OwnerCog):
    @commands.group(invoke_without_command=True)
    async def ext(self, ctx: commands.Context):
        group_command_names = (
            command.name for command in ctx.command.commands
        )
        await ctx.send(f"usage: {ctx.prefix}ext {{{','.join(group_command_names)}}}")

    @ext.command(name="list")
    async def ext_list(self, ctx: commands.Context):
        loaded_extension_names = [
            extension_name for extension_name in ctx.bot.extensions
            if not self.is_core_extension(extension_name)
        ]
        await ctx.send(
            "Currently loaded extensions:```"
            + "\n".join(loaded_extension_names)
            + "```"
            if loaded_extension_names
            else "No extensions currently loaded."
        )

    @ext.command(name="load")
    async def ext_load(self, ctx: commands.Context, *, extension_names: str = ""):
        extensions_to_load = extension_names.split()
        if extensions_to_load:
            load_status = {
                extension_name: f"Loading `{extension_name}`..."
                for extension_name in extensions_to_load
            }
            message = await ctx.send(
                "\n".join(status for _, status in load_status.items())
            )
            for extension_name in extensions_to_load:
                try:
                    self.bot.load_extension(f"presage.{extension_name}")
                    load_status[extension_name] = f"Successfully loaded `{extension_name}`"
                except (commands.ExtensionError, ModuleNotFoundError) as cause:
                    load_status[extension_name] = f"Failed to load `{extension_name}`: {cause}"

                await message.edit(
                    content="\n".join(status for _, status in load_status.items())
                )
        else:
            await ctx.send(f"usage: {ctx.prefix}{ctx.command} extension [extension ...]")

    @ext.command(name="unload")
    async def ext_unload(self, ctx: commands.Context, *, extension_names: str = ""):
        extensions_to_unload = extension_names.split()
        if extensions_to_unload:
            unload_status = {
                extension_name: f"Unloading `{extension_name}`..."
                for extension_name in extensions_to_unload
            }
            message = await ctx.send(
                "\n".join(status for _, status in unload_status.items())
            )
            for extension_name in extensions_to_unload:
                try:
                    if self.is_core_extension(f"presage.{extension_name}"):
                        raise CannotUnloadCoreExtension(extension_name)
                    self.bot.unload_extension(f"presage.{extension_name}")
                    unload_status[extension_name] = f"Successfully unloaded `{extension_name}`"
                except commands.ExtensionError as cause:
                    unload_status[extension_name] = f"Failed to unload `{extension_name}`: {cause}"

                await message.edit(
                    content="\n".join(status for _, status in unload_status.items())
                )
        else:
            await ctx.send(f"usage: {ctx.prefix}{ctx.command} extension [extension ...]")

    @ext.command(name="reload")
    async def ext_reload(self, ctx: commands.Context, *, extension_names: str = ""):
        extensions_to_reload = extension_names.split() or [
            extension_name for extension_name in ctx.bot.extensions
            if not self.is_core_extension(extension_name)
        ]
        if extensions_to_reload:
            reload_status = {
                extension_name: f"Reloading `{extension_name}`..."
                for extension_name in extensions_to_reload
            }
            message = await ctx.send(
                "\n".join(status for _, status in reload_status.items())
            )
            for extension_name in extensions_to_reload:
                try:
                    self.bot.reload_extension(f"presage.{extension_name}")
                    reload_status[extension_name] = f"Successfully reloaded `{extension_name}`"
                except commands.ExtensionError as cause:
                    reload_status[extension_name] = f"Failed to reload `{extension_name}`: {cause}"

                await message.edit(
                    content="\n".join(status for _, status in reload_status.items())
                )
        else:
            await ctx.send("No extensions to reload.")

    def is_core_extension(self, extension_name: str) -> bool:
        return commands.bot._is_submodule(self.extension, extension_name)
