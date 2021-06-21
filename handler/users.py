from telethon import custom, events
from garnet import FSMContext, MessageText
from garnet.router import Router
import logging
from const import CONSTANTS

logging.basicConfig(level=logging.ERROR)

user_router = Router(event=events.NewMessage())


@user_router.on(MessageText.commands("start"))
async def start_rout_hndlr(update: custom.Message, context: FSMContext):
    await update.reply(
        "__Currently, bot is in beta version__"
        "\n\n**Usage:**"
        "\n\t➕ Add this bot to the channel (preferrably, a test channel)"
        "\n\n**Inspiration,**"
        "\n\tLike in blogs/sites, I will add a showmore button at the bottom of posts. "
        "if user is interested in reading the full posts, they can read it by pressing 'ShowMore' button"
        f"\n\n**Note**: "
        f"\n\t✅ Bot will only shrunk the posts if the post length is greater than {CONSTANTS.TRUNC+20}words",
        buttons=[
            [
                custom.Button.url(
                    text="🤖 Other Awesome bots", url="https://t.me/ys0seri0us_bots/2"
                )
            ],
            [
                custom.Button.url(text="🛠", url="https://t.me/PostAppender_Bot"),
                custom.Button.url(text="🔊", url="https://t.me/PostBroadcasterobot"),
                custom.Button.url(text="🧹", url="https://t.me/ClearURLs_Bot"),
                custom.Button.url(text="👨‍💻", url="https://t.me/contactorobot"),
            ],
            [
                custom.Button.url(
                    text="📝 Source",
                    url="https://github.com/GauthamramRavichandran/showmore-bot",
                )
            ],
        ],
    )
