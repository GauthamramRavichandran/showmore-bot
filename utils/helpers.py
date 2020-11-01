from apscheduler.schedulers.asyncio import AsyncIOScheduler
import re

from const import CONSTANTS


def split(delimiters, string, maxsplit=0):
	regexPattern = '|'.join(map(re.escape, delimiters))
	return re.split(regexPattern, string, maxsplit)


def calculate_read_time( message_text: str ) -> int:
	return len(split(CONSTANTS.DELIMS, message_text)) // 100 or 1  # roughly 265words/minute given by medium.com


class Edit:
	@staticmethod
	def create_trunc_text(got_msg):
		entites_to_add = []
		if got_msg.entities:
			for entity in got_msg.entities:
				if entity.offset + entity.length > CONSTANTS.TRUNC:
					entites_to_add.append('```')
		return f"{got_msg.text[:CONSTANTS.TRUNC]} {''.join(ent for ent in entites_to_add)}**...**" \
		       f"\n\n__ {calculate_read_time(got_msg.raw_text)} minutes read__"
	

scheduler = AsyncIOScheduler()
scheduler.start()
