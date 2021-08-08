async def register(ctx):
    username = ctx.message.author


async def remove(ctx):
    await ctx.send(f"{ctx.message.author.mention}, okay we are removing you")


async def tier(ctx):
    await ctx.send(f"{ctx.message.author.mention}, Your tier is one")
