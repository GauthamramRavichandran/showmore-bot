from datetime import datetime, timedelta
from telethon import custom

from telethon.tl.types import Channel, KeyboardButtonCallback
from garnet import FSMContext, MessageText, Filter
from garnet.router import Router
from garnet import events
import logging
import short_url

logging.basicConfig(level = logging.INFO)
from const.CONFIG import FULL_POSTS_CHNLD_ID, FULL_CHNL_INVTE_LNK, FULL_POSTS_CHNLD_ID_no_100
from const import CONSTANTS

from utils import calculate_read_time, scheduler, Edit


my_router = Router(event = events.NewMessage())


def only_chnls(event):
	# print(event)
	if isinstance(event.message.chat, Channel) \
					and event.fwd_from is None \
					and event.message.to_id.channel_id != FULL_POSTS_CHNLD_ID_no_100:
		# TODO get fullid including -100
		# TODO check if chnl in db before trimming
		return True
	return False
	
# fixme ALBUMS wont work


@my_router.on(Filter(only_chnls) & (MessageText.Len >= CONSTANTS.TRUNC + 10))
async def start_rout_hndlr(event):
	sent_message = await event.client.send_message(entity = FULL_POSTS_CHNLD_ID, message = event.message)
	data = short_url.encode_url(sent_message.id, min_length = 10)
	await event.client.edit_message(entity = event.message.to_id, message = event.message.id,
	                                 buttons = custom.Button.inline(text = "Show More>>", data = f"op_{data}_0_0"),
	                                 text = Edit.create_trunc_text(event.message))
	raise events.StopPropagation
	
	
async def pre_close_message(update):
	to_close = False
	got_msg = await update.client.get_messages(update.query.peer, ids = update.query.msg_id)
	for row in got_msg.reply_markup.rows:
		for btn in row.buttons:
			if isinstance(btn, KeyboardButtonCallback):
				to_decode = btn.data.decode("utf-8")
				if to_decode.startswith('cl'):
					to_close = True
					break
	if to_close:
		to_decode = update.query.data.decode("utf-8")
		action, code, user_id, views = to_decode.split('_')  # userid = 0 if "ShowMore" is pressed
		message_id = short_url.decode_url(code)
		got_msg = await update.client.get_messages(FULL_POSTS_CHNLD_ID, ids = message_id)
		
		await update.client.edit_message(entity = update.query.peer,
		                                 text = Edit.create_trunc_text(got_msg),
		                                 buttons = custom.Button.inline(text = "Show More>>",
		                                                                data = f"op_{code}_0_{int(views)+1}"),
		                                 message = update.query.msg_id)


@my_router.on(event = events.CallbackQuery)
async def all_call_hndlr(update):
	try:
		to_decode = update.query.data.decode("utf-8")
		action, code, user_id, views = to_decode.split('_')  # userid = 0 if "ShowMore" is pressed
		"""
		action:
				cl => close button
				op => open button (ShowMore>>)
				vw => show number of views
		"""
		if action == "cl":
			await update.client.edit_message(entity = update.query.peer,
			                                 text = CONSTANTS.LOGO,
			                                 buttons = custom.Button.inline(text = "Show More>>",
			                                                                data = f"op_{code}_0_{views}"),
			                                 message = update.query.msg_id)
			if update.query.user_id == int(user_id):
				message_id = short_url.decode_url(code)
				got_msg = await update.client.get_messages(FULL_POSTS_CHNLD_ID, ids = message_id)
				await update.client.edit_message(entity = update.query.peer,
				                                 text = Edit.create_trunc_text(got_msg),
				                                 buttons = custom.Button.inline(text = "Show More>>",
				                                                                data = f"op_{code}_0_{views}"),
				                                 message = update.query.msg_id)
			else:
				await update.answer("Someone else is reading this!", alert = True)
				# TODO read me in Private, url = "t.me/ShowMore_Bot?start=xyz")
		elif action == "op":
			await update.answer("Loading full version..,")
			message_id = short_url.decode_url(code)
			got_msg = await update.client.get_messages(FULL_POSTS_CHNLD_ID, ids = message_id)
			await update.client.edit_message(entity = update.query.peer,
			                                 text = got_msg.text,
			                                 buttons = [
				                                 [custom.Button.inline(text = f"{views} Views 👁️‍🗨",
			                                                         data = f"vw_{code}_0_{views}"),
                                         custom.Button.inline(text = "Close ❌",
                                                              data = f"cl_{code}_{update.query.user_id}_{int(views)+1}")],
                                         [custom.Button.url(text = "Created by ShowMore bot",
                                                            url = 't.me/ShowMore_Bot')]],
			                                 message = update.query.msg_id)
			scheduler.add_job(pre_close_message, kwargs = {"update": update},
												run_date = datetime.now()+timedelta(minutes = calculate_read_time(got_msg.raw_text)))
		elif action == "vw":
			await update.answer(f"👁️‍🗨️ {views} subscribers have read it!")
	except Exception as e:
		print(e)
