from telethon import custom

from garnet import TelegramClient

from const.CONFIG import BOT_TOKEN, API_ID, API_HASH
from handler.channel import my_router
from handler.users import user_router


# /*
#  * get configurations from environment variable
#  * look garnet.TelegramClient::Env for more
#  */
bot = TelegramClient.from_env(default_api_id = API_ID, default_api_hash = API_HASH,
                              bot_token = BOT_TOKEN)

if __name__ == '__main__':
	@bot.on_start()
	async def main(_):
		bot.bind_routers(my_router, user_router)
		
		await bot.start_as_bot()
		print(await bot.get_me())
	bot.run_until_disconnected()
