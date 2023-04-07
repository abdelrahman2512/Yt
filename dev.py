from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from youtubesearchpython import VideosSearch
from pytube import YouTube
from asSQL import Client as c
import os, re, yt_dlp, asyncio, wget, asSQL

save_id = int(-1001982856776) # ايدي القناه
user = "YtLogs2" # يوزر القناه
####
SQL = c("virus")
db = SQL["main"]
db.create_table()
bot = Client(
        "youtube",
        api_id = 9028013,
        api_hash = "cc894fc40424f9c8bbcf06b7355bd69d",
        bot_token = "5817789987:AAFsPnLmIh-tAgcARu5ms1oMFLsdbORav5E" # توكنك
)
@bot.on_message(filters.private & filters.text)
async def main(bot, msg):
	if msg.text == "/start":
		await bot.send_message(msg.chat.id, f"• مرحبا بك 《 {msg.from_user.mention} 》\n\n• في بوت اليوتيوب الاول علي التليجرام\n• يدعم التحميل حتي 2GB")
	if msg.text != "/start" and not re.findall(r"(.*?)dl(.*?)", msg.text):
		wait = await bot.send_message(msg.chat.id, f'🔎︙البحث عن "{msg.text}"...')
		search = VideosSearch(msg.text).result()
		txt = ''
		for i in range(9):
			title = search["result"][i]["title"]
			channel = search["result"][i]["channel"]["name"]
			duration = search["result"][i]["duration"]
			views = search["result"][i]["viewCount"]["short"]
			id = search["result"][i]["id"].replace("-","virus")
			txt += f"🎬 [{title}](https://youtu.be/{id})\n👤 {channel}\n🕑 {duration} - 👁 {views}\n🔗 **/dl_**{id}\n\n"
		await wait.edit(f'🔎︙نتائج البحث لـ "{msg.text}"\n\n{txt}', disable_web_page_preview=True, parse_mode=enums.ParseMode.MARKDOWN)
	if re.findall(r"^/dl_(.*?)", msg.text):
		vid_id = msg.text.replace("virus","-").replace("/dl_","").replace("dl_","").replace("/","")
		wait = await bot.send_message(msg.chat.id, f'🔎︙البحث عن "https://youtu.be/{vid_id}"...', disable_web_page_preview=True)
		info = YouTube(f"https://youtu.be/{vid_id}")
		keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("مقطع فيديو 🎞",callback_data=f"video&&{vid_id}"),InlineKeyboardButton("ملف صوتي 📼",callback_data=f"audio&&{vid_id}")
		],[
		InlineKeyboardButton("بصمه صوتية 🎙",callback_data=f"voice&&{vid_id}")
		]])
		await bot.send_photo(msg.chat.id,
		photo=f"https://youtu.be/{vid_id}",
		caption=f"🎬 [{info.title}](https://youtu.be/{vid_id})\n👤 {info.author}\n👁 {info.views}",
		reply_markup=keyboard
		)
		await wait.delete()

@bot.on_callback_query(filters.regex("&&") , group = 24)
async def download(bot, query: CallbackQuery) :
	video_id = query.data.split("&&")[1]
	if query.data.split("&&")[0] == "video":
		await bot.delete_messages(query.message.chat.id, query.message.id)
		if db.get(f"{video_id}&video") == None:
			wait = await bot.send_message(query.message.chat.id, "🚀 جار التحميل ....")
			video_link = f"https://youtu.be/{video_id}"
			with yt_dlp.YoutubeDL({"format": "best","keepvideo": True,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.%(ext)s","quite": True}) as ytdl:
				info = ytdl.extract_info(video_link, download=False)
				video = ytdl.prepare_filename(info)
				ytdl.process_info(info)
			information = YouTube(video_link)
			thumb = wget.download(information.thumbnail_url)
			await wait.edit("⬆️ جاري الرفع ....")
			msg = await bot.send_video(save_id,
			video=video,
			duration=information.length,
			thumb=thumb,
			caption="By : @V_IRUuS")
			db.set(f"{video_id}&video", int(msg.id))
			await bot.send_video(query.message.chat.id,
			video=f"https://t.me/{user}/{msg.id}",
			caption="By : @V_IRUuS")
			await wait.delete()
			try :
				os.remove(video)
				os.remove(thumb)
			except:
				pass
		else:
			wait = await bot.send_message(query.message.chat.id, "⬆️ جاري الرفع ....")
			msg_id = int(db.get(f"{video_id}&video"))
			await bot.send_video(query.message.chat.id,
			video=f"https://t.me/{user}/{msg_id}",
			caption="By : @V_IRUuS")
			await wait.delete()

	if query.data.split("&&")[0] == "audio":
		await bot.delete_messages(query.message.chat.id, query.message.id)
		if db.get(f"{video_id}&audio") == None:
			wait = await bot.send_message(query.message.chat.id, "🚀 جار التحميل ....")
			video_link = f"https://youtu.be/{video_id}"
			with yt_dlp.YoutubeDL({"format": "bestaudio[ext=m4a]"}) as ytdl:
				info = ytdl.extract_info(video_link, download=False)
				audio = ytdl.prepare_filename(info)
				ytdl.process_info(info)
			information = YouTube(video_link)
			thumb = wget.download(information.thumbnail_url)
			await wait.edit("⬆️ جاري الرفع ....")
			msg = await bot.send_audio(save_id,
			audio=audio,
			caption="By : @V_IRUuS",
			title=information.title,
			duration=information.length,
			thumb=thumb,
			performer=information.author)
			db.set(f"{video_id}&audio", int(msg.id))
			await bot.send_audio(query.message.chat.id,
			audio=f"https://t.me/{user}/{msg.id}",
			caption="By : @V_IRUuS")
			await wait.delete()
			try:
				os.remove(audio)
				os.remove(thumb)
			except:
				pass
		else:
			wait = await bot.send_message(query.message.chat.id, "⬆️ جاري الرفع ....")
			msg_id = int(db.get(f"{video_id}&audio"))
			await bot.send_audio(query.message.chat.id,
			audio=f"https://t.me/{user}/{msg_id}",
			caption="By : @V_IRUuS")
			await wait.delete()
	if query.data.split("&&")[0] == "voice":
		await bot.delete_messages(query.message.chat.id, query.message.id)
		if db.get(f"{video_id}&voice") == None:
			wait = await bot.send_message(query.message.chat.id, "🚀 جار التحميل ....")
			video_link = f"https://youtu.be/{video_id}"
			with yt_dlp.YoutubeDL({"format": "bestaudio[ext=m4a]"}) as ytdl:
				info = ytdl.extract_info(video_link, download=False)
				voice = ytdl.prepare_filename(info)
				ytdl.process_info(info)
			information = YouTube(video_link)
			thumb = wget.download(information.thumbnail_url)
			await wait.edit("⬆️ جاري الرفع ....")
			msg = await bot.send_voice(save_id,
			voice=voice,
			caption="By : @V_IRUuS",
			duration=information.length)
			db.set(f"{video_id}&voice", int(msg.id))
			await bot.send_voice(query.message.chat.id,
			voice=f"https://t.me/{user}/{msg.id}",
			caption="By : @V_IRUuS",
			duration=information.length)
			await wait.delete()
			try:
				os.remove(voice)
				os.remove(thumb)
			except:
				pass
		else:
			wait = await bot.send_message(query.message.chat.id, "⬆️ جاري الرفع ....")
			msg_id = int(db.get(f"{video_id}&voice"))
			await bot.send_voice(query.message.chat.id,
			voice=f"https://t.me/{user}/{msg_id}",
			caption="By : @V_IRUuS")
			await wait.delete()

print("اشتغل")
bot.run()
