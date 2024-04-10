from pyrogram import Client, filters as ay
from pyrogram.types import *
import asyncio
import os, wget
import requests
from pyromod import listen
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
MONGO = "mongodb+srv://devfraon:devfraon@devfraon.sg3sijf.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(MONGO)
mongodb = mongo.bot
usersdb = mongodb.users


async def is_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True
    
async def get_users() -> list:
 	users_list = []
 	async for user in usersdb.find({"user_id": {"$gt": 0}}):
 	  users_list.append(user)
 	return users_list
    
async def add_user(user_id: int):
    is_served = await is_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})   
    
NEW_MEMBER = """
♡• 
مرحبا بك دخل شخص جديد الي الروبوت .

- Name : {} 
- ID : {}

- Users : {} 

✦✧✦✧✦✧
"""
api_id = 12822843
api_hash = "689f3bfcefe86a6a3dffe6830baf1010"
token = "6338542187:AAHbDSRIxc6sMT1LbYjwf9_2_wKr6FpuSw0"
OWNER_NAME = "𝗔 𝗵 𝗠 𝗲 𝗱"

app = Client("yt", bot_token=token, api_id = api_id, api_hash = api_hash)
BOT_TOKEN = token
CHANNEL = "pyth_on3"
OWNER = 5449190469
con3 = +201014024429

@app.on_message(ay.command("start"))
async def st(client,message):
	if message.from_user.id != OWNER:
		user_id = message.from_user.id
		if not await is_user(user_id=user_id):
			await add_user(user_id=user_id)
			a = message.from_user.mention
			b = message.from_user.id
			c = len(await get_users())
			await app.send_message(
			OWNER,
			NEW_MEMBER.format(a,b,c)
			)
		do = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id=@{CHANNEL}&user_id={message.from_user.id}").text
		if do.count("left") or do.count("Bad Request: user not found"):
			await app.send_message(
			message.chat.id,
			"**⌁ عليك الاشتراك في القناه لاستخدام البوت .**",
			reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="- Channel .",url=f"https://t.me/{CHANNEL}")],]),
			reply_to_message_id=message.id
			)
		else:
			key = ReplyKeyboardMarkup(
	[
		[
			KeyboardButton("اࢪسال جهة اتصالي 🍃",request_contact= True),
			KeyboardButton("اࢪسال موقعي 🍃",request_location= True)],
		[
			KeyboardButton("تعليمات الاستخدام 🍃")],
		[
			KeyboardButton("جهة اتصال المالك 🍃"),
			KeyboardButton("بروفايل المالك 🍃")],
		[
			KeyboardButton("القوانين ⚠️"),
			KeyboardButton("جديدنا 🔥")],
		[
			KeyboardButton("لتنصيب بوت مثل هاذا ✨")],],
			resize_keyboard=True
			)
			await app.send_message(message.chat.id,
			"**مرحبا بك {} **\n\nانا بوت تواصل خاص بـ {} \n\nفقط ارسل رسالتك✨**".format(message.from_user.mention,OWNER_NAME),
			reply_markup=key,
			reply_to_message_id=message.id
			)

	else:
		await app.send_message(
		chat_id=message.chat.id,
		text="**مرحبا بك عزيزى المالك \nلعمل اذاعه ارسل (`اذاعه`)\nلمعرفه عدد الاعضاء ارسل (`الاحصائيات`)\nلجلب نسخه احتياطيه ارسل (`نسخه`او`احتياطيه`)\n♕**"
		)
		
			

@app.on_message(ay.command(['تعليمات الاستخدام 🍃'],prefixes=""))
async def help(client,message):
	message.forward(
	OWNER
	)
	m = await message.reply(
	"""
	**اليك قائمه تعليمات استخدام البوت **
	
	- **زر ارسال جهة اتصالي ** ✦ هذا الزر اذا كنت تريد ارسال جهة اتصالك لصاحب البوت .
	- ** زر ارسال موقعي ** ✦ استخدمه اذا كنت في حاجه لارسال موقعك لصاحب البوت .
	- ** زر تعليمات الاستخدام ** ✦ يظهر لك هذة القائمه ف بعض الناس لا يعرفون طريقه استخدام البوت .
	- ** زر جهة اتصال المالك ** ✦ اذا اراد المالك وضع جهة اتصاله لكي تتواصل معه عن طريقها .
	- ** زر بروفايل المالك ** ✦ يرسل لك حساب المالك علي التليجرام للتواصل معه مباشرة دون الحاجه للبوت .
	- ** زر القوانين ** ✦ يرسل لك القوانين التي قام المالك بوضعها لتجنب الحظر من البوت .
	- ** زر جديدنا ** ✦ يرسل لك مجموته قنواتنا التي يمكنها افادتك بشكل كبير .
	- ** زر لتنصيب بوت مثل هذا ** ✦ يرسل لك رابط جروب الدعم يمكنك من خلاله التواصل مع تيم Em لتنصيب بوت مثل هذا .
	
	قناه ااسورس : @D2_RK 
	"""
	, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("اغلاق",callback_data='ex')]]))
	
@app.on_callback_query(ay.regex("ex"))
async def reg(_,query:CallbackQuery):
	await app.delete_messages(
	chat_id=query.message.chat.id,
	message_ids=query.message.id
	)
	
@app.on_message(ay.command(["جهة اتصال المالك 🍃"],prefixes=""))
async def con(client,message):
	message.forward(
	OWNER
	)
	if con3:
		await app.send_contact(
		chat_id=message.chat.id,
		phone_number=con3,
		first_name="مالك البوت 👀")
	else:
		await message.reply(
		"**لم يقم المالك بوضع جهة اتصاله .**")
		
@app.on_message(ay.command(["بروفايل المالك 🍃"],prefixes=""))
async def admm(client,message):
	message.forward(
	OWNER
	)
	x = (await app.get_users(OWNER)).mention
	await message.reply(
	"** يمگنك التواصل مع مالك الࢪوبوت مباشࢪةً من هنا \n\n{}**".format(x))
	
@app.on_message(ay.command(["القوانين ⚠️"],prefixes=""))
async def cmd(client,message):
	message.forward(
	OWNER
	)
	crv = """
	**قوانين البوت **⚠️
	- يسمح لك بارسال التالي ...
	- صور 
	- فيديوهات 
	- روابط 
	- ملفات 
	- استيكر 
	- ملصقات Gif 
	- العاب 
	- فويس صوت 
	- مواقع 
	- جهات اتصال 
	
	- لتخطي الحظر لا يسمح لك بارسال اى كلمات خارجه .
	
	⚠️ كلمه خارجه == بلوك من البوت .
	
	"""
	
	await message.reply(crv)
	
@app.on_message(ay.command(['جديدنا 🔥'],prefixes=""))
async def neww(client,message):
	message.forward(
	OWNER
	)
	xrb3 = """
	✦ [قناه السورس](https://t.me/D2_RK)
	
	انضم فضلا 🖤
	"""
	await message.reply(xrb3,
	reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("اغلاق",callback_data='ex')]]),
	disable_web_page_preview=True,disable_notification=False
	)
	
@app.on_message(ay.command(["لتنصيب بوت مثل هاذا ✨"],prefixes=""))
async def tanc(client,message):
	await message.forward(
	OWNER
	)
	await message.reply(
	"**يمكنك الدخول لمطور البوت**\n\n**مطور البوت : @A7_M3",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("-Channel",url="https://t.me/D2_RK")]]))
	
@app.on_message(ay.command(["اذاعه","اذاعة"],prefixes="")&ay.user(OWNER))
async def brodcast(client,message):
	if message.from_user.id == OWNER:
		if not message.reply_to_message:
			pass
		else:
			x = message.reply_to_message.id
			y = message.chat.id
			sent = 0
			users = []
			hah = await get_users()
			for user in hah:
				users.append(int(user["user_id"]))
				for i in users:
					try:
						m = await client.forward_messages(i,y,x)
						await asyncio.sleep(.3)
						sent += 1
					except Exception:
						pass
				await message.reply("**تمت الاذاعه بنجاح الي {} عضو **".format(sent))
				return
			if len(message.command)<2:
				await message.reply(
				"**استخدام خاطئ \n\nاذاعه + النص الذى تريد اذاعته \n\nاو اذاعه بالرد علي رساله لاذاعتها .")
				return
			text = message.text.split(None,1)[1]
			sent = 0
			users = []
			hah = await get_users()
			for user in hah:
				users.append(int(user["user_id"]))
			for i in users:
				try:
					await client.send_message(i,text=text)
					await asyncio.sleep(.3)
					sent += 1
				except Exception:
					pass
			await message.reply("**تمت الاذاعه بنجاح الي {} عضو **".format(sent))
			
@app.on_message(ay.command(['الاحصائيات','احصائيات','/stats'],prefixes="")&ay.user(OWNER))
async def gety(client,message):
	stats = len(await get_users())
	await app.send_message(
	message.chat.id,
	"**عدد اعضاء بوتك ...\n{} **".format(stats))
	

@app.on_message(ay.command(['نسخه','نسخة','نسخه احتياطيه','نسخة احتياطية','احتياطيه','احتياطية'],prefixes="")&ay.user(OWNER))
async def getl(client,message):
	m = await message.reply("**prossing...**")
	filename = "@A7_M3-users.txt"
	with open(filename, "w+", encoding="utf8") as out_file:
		out_file.write(str(await get_users()))
	stats = len(await get_users())
	await app.send_document(
	message.chat.id,
	document=filename,
	caption="**users Stats {}".format(stats)
	)
	await m.delete()
	os.remove(filename)
	
@app.on_message(ay.text)
async def fome(client,message):
	await message.forward(
	OWNER
	)
	await app.send_message(
	message.chat.id,
	"""❖ المستخدم ← {}
❖ تم ارسال رسالتك الى المطور""".format(message.from_user.mention)
)

@app.on_message(ay.contact)
async def con(client,message):
	await message.forward(
	OWNER
	)
	await app.send_message(
	message.chat.id,
	"""❖ المستخدم ← {}
❖ تم ارسال رسالتك الى المطور""".format(message.from_user.mention)
)
	
@app.on_message(ay.location)
async def lo(client,message):
	await message.forward(
	OWNER
	)
	await app.send_message(
	message.chat.id,
	"""❖ المستخدم ← {}
❖ تم ارسال رسالتك الى المطور""".format(message.from_user.mention)
)
	
@app.on_message(ay.audio)
async def au(client,message):
	await message.forward(
	OWNER
	)
	await app.send_message(
	message.chat.id,
	"""❖ المستخدم ← {}
❖ تم ارسال رسالتك الى المطور""".format(message.from_user.mention)
)
	
@app.on_message(ay.sticker)
async def sttt(client,message):
	await message.forward(
	OWNER
	)
	await app.send_message(
	message.chat.id,
	"""❖ المستخدم ← {}
❖ تم ارسال رسالتك الى المطور""".format(message.from_user.mention)
)
	
@app.on_message(ay.photo)
async def ph(client,message):
	await message.forward(OWNER)
	await app.send_message(
	message.chat.id,
	"""❖ المستخدم ← {}
❖ تم ارسال رسالتك الى المطور""".format(message.from_user.mention)
)
	
@app.on_message(ay.video)
async def vd(client,message):
	await message.forward(
	OWNER
	)
	await app.send_message(
	message.chat.id,
	"""❖ المستخدم ← {}
❖ تم ارسال رسالتك الى المطور""".format(message.from_user.mention)
)
	
@app.on_message(ay.game)
async def gm(client,message):
	await message.forward(
	OWNER 
	)
	await app.send_message(
	message.chat.id,
	"""❖ المستخدم ← {}
❖ تم ارسال رسالتك الى المطور""".format(message.from_user.mention)
)
	
@app.on_message(ay.media)
async def med(xlient,message):
	await message.forward(
	OWNER 
	)
	await app.send_message(
	message.chat.id,
	"""❖ المستخدم ← {}
❖ تم ارسال رسالتك الى المطور""".format(message.from_user.mention)
)
	
@app.on_message(ay.document)
async def docc(client,message):
	await message.forward(
	OWNER 
	)
	await app.send_message(
	message.chat.id,
	"""❖ المستخدم ← {}
❖ تم ارسال رسالتك الى المطور""".format(message.from_user.mention)
)
	
app.run()
	
	#
	
	
	#[⛥ .✘𓏺 𝗔 𝗵 𝗠 𝗲 𝗱
	
	
	#
