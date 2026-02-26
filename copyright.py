import os
import re
import sys
import time
import datetime
import random 
import asyncio
from dotenv import load_dotenv
from pytz import timezone
from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.raw.types import UpdateEditMessage, UpdateEditChannelMessage
import traceback

from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

bot = Client(
    "mybot",
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN")
)

DEVS = [8531043812]
BOT_USERNAME = "editguardsrobot" # change your bot username without @
PING_IMG_URL = "https://files.catbox.moe/qrv1xs.jpg"

ALL_GROUPS = []
TOTAL_USERS = []
MEDIA_GROUPS = []
DISABLE_CHATS = []
GROUP_MEDIAS = {}

DELETE_MESSAGE = [
"「 1 」 𝟙 𝙃𝙤𝙪𝙧 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚, 𝙄'𝙢 𝘿𝙤𝙞𝙣𝙜 𝙈𝙮 𝙒𝙤𝙧𝙠...",
"「 2 」 𝑰𝒕’𝒔 𝑻𝒊𝒎𝒆 𝑻𝒐 𝑫𝒆𝒍𝒆𝒕𝒆 𝑨𝒍𝒍 𝑴𝒆𝒅𝒊𝒂𝒔!",
"「 3 」 𝙉𝙤 𝙊𝙣𝙚 𝘾𝙖𝙣 𝘾𝙤𝙥𝙮𝙧𝙞𝙜𝙝𝙩 𝙐𝙣𝙩𝙞𝙡 𝙄’𝙢 𝘼𝙡𝙞𝙫𝙚 😤",
"「 4 」 𝐇𝐮𝐞 𝐇𝐮𝐞, 𝐋𝐞𝐭’𝐬 𝐃𝐞𝐥𝐞𝐭𝐞 𝐌𝐞𝐝𝐢𝐚...",
"「 5 」 𝕀’𝕞 ℍ𝕖𝕣𝕖 𝕋𝕠 𝔻𝕖𝕝𝕖𝕥𝕖 𝕄𝕖𝕕𝕚𝕒𝕤 🙋",
"「 6 」 😮‍💨 𝙁𝙞𝙣𝙖𝙡𝙡𝙮 𝙄 𝘿𝙚𝙡𝙚𝙩𝙚 𝙈𝙚𝙙𝙞𝙖𝙨",
"「 7 」 𝙂𝙧𝙚𝙖𝙩 𝙒𝙤𝙧𝙠 𝘿𝙤𝙣𝙚 𝘽𝙮 𝙈𝙚 🥲",
"「 8 」 𝘼𝙡𝙡 𝙈𝙚𝙙𝙞𝙖 𝘾𝙡𝙚𝙖𝙧𝙚𝙙!",
"「 9 」 𝓗𝓾𝓮 𝓗𝓾𝓮 𝓜𝓮𝓭𝓲𝓪𝓼 𝓓𝓮𝓵𝓮𝓽𝓮𝓭 𝓑𝔂 𝓜𝓮 😮‍💨",
"「10」 𝕄𝕖𝕕𝕚𝕒𝕤....",
"「11」 𝙄𝙩’𝙨 𝙃𝙖𝙧𝙙 𝙏𝙤 𝘿𝙚𝙡𝙚𝙩𝙚 𝘼𝙡𝙡 𝙈𝙚𝙙𝙞𝙖𝙨 🙄",
]
START_VIDEO = "https://files.catbox.moe/ty42li.mp4"
START_MESSAGE = """
**ʜᴇʟʟᴏ {}, ɪ'ᴍ ᴀɴᴛɪ-ᴄᴏᴘʏʀɪɢʜᴛ ʙᴏᴛ 🛡️**

> **ɪ ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ sᴀғᴇ ғʀᴏᴍ ᴄᴏᴘʏʀɪɢʜᴛ sᴛʀɪᴋᴇs 😉**

━━━━━━━━━━━━━━━━━━
**⚙ ᴡᴏʀᴋ ᴍᴏᴅᴇ**

➤ ɪ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇᴅɪᴀ ғɪʟᴇs  
➤ ᴇᴠᴇʀʏ 𝟷 ʜᴏᴜʀ ᴡɪᴛʜᴏᴜᴛ ғᴀɪʟ  
➤ ᴘʜᴏᴛᴏs • ᴠɪᴅᴇᴏs • ᴅᴏᴄᴜᴍᴇɴᴛs • ᴀᴜᴅɪᴏ  
➤ ᴋᴇᴇᴘs ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʟᴇᴀɴ ᴀɴᴅ sᴀғᴇ ➰

━━━━━━━━━━━━━━━━━━
**❓ ʜᴏᴡ ᴛᴏ ᴜsᴇ**

➊ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ  
➋ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀᴅᴍɪɴ  
➌ ɢɪᴠᴇ “ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs” ᴘᴇʀᴍɪssɪᴏɴ  

ᴀɴᴅ ʟᴇᴛ ᴍᴇ ʜᴀɴᴅʟᴇ ᴛʜᴇ ʀᴇsᴛ 😌

━━━━━━━━━━━━━━━━━━
**♻ ᴀᴜᴛᴏ • ғᴀsᴛ • sᴇᴄᴜʀᴇ • ʀᴇʟɪᴀʙʟᴇ**
"""

BUTTON = [
           [
            InlineKeyboardButton("➕ ᴧᴅᴅ ϻє ᴛσ ɢʀσᴜᴘ ➕", url=f"http://t.me/{BOT_USERNAME}?startgroup=s&admin=delete_messages"),
            InlineKeyboardButton("✦ ˹ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ˼ 🎧  🚫🔥", url=f"https://t.me/dark_musictm"),
           ]
         ] 


def add_user(user_id):
   if user_id not in TOTAL_USERS:
      TOTAL_USERS.append(user_id)

@bot.on_message(filters.command(["ping", "speed"]))
async def ping(_, e: Message):
   start = datetime.datetime.now()
   add_user(e.from_user.id)
   rep = await e.reply_text("**Pong !!**")
   end = datetime.datetime.now()
   ms = (end-start).microseconds / 1000
   await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"].format(app.mention),
   )

@bot.on_message(filters.command(["help", "start"]))
async def start_message(_, message: Message):
   add_user(message.from_user.id)
   await message.reply(
        f"{text}\n\n<a href='{START_VIDEO}'>๏ ɪ ᴡᴀɴɴᴀ ʙᴇ ʏᴏᴜʀꜱ ♡ 🌷</a>",
        reply_markup=keyboard,
   )

@bot.on_message(filters.user(DEVS) & filters.command(["restart", "reboot"]))
async def restart_(_, e: Message):
   await e.reply("**Restarting.....**")
   try:
      await bot.stop()
   except Exception:
      pass
   args = [sys.executable, "copyright.py"]
   os.execl(sys.executable, *args)
   quit()

@bot.on_message(filters.user(DEVS) & filters.command(["stat", "stats"]))
async def status(_, message: Message):
   wait = await message.reply("Fetching.....")
   stats = "**Here is total stats of me!** \n\n"
   stats += f"Total Chats: `{len(ALL_GROUPS)}` \n"
   stats += f"Total users: `{len(TOTAL_USERS)}` \n"
   stats += f"Disabled chats: `{len(DISABLE_CHATS)}` \n"
   stats += f"Total Media active chats: `{len(MEDIA_GROUPS)}` \n\n"
   #stats += f"**© @Lemonade0_0**"
   await wait.edit_text(stats)


   
@bot.on_message(filters.command(["anticopyright", "copyright"]))
async def enable_disable(bot: bot, message: Message):
   chat = message.chat
   if chat.id == message.from_user.id:
      await message.reply("Use this command in group!")
      return
   txt = ' '.join(message.command[1:])
   if txt:
      member = await bot.get_chat_member(chat.id, message.from_user.id)
      if re.search("on|yes|enable".lower(), txt.lower()):
         if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or member.user.id in DEVS:
            if chat.id in DISABLE_CHATS:
               await message.reply(f"Enabled anti-copyright! for {chat.title}")
               DISABLE_CHATS.remove(chat.id)
               return
            await message.reply("Already enabled!")

      elif re.search("no|off|disable".lower(), txt.lower()):
         if member.status == ChatMemberStatus.OWNER or member.user.id in DEVS:
            if chat.id in DISABLE_CHATS:
               await message.reply("Already disabled!")
               return
            DISABLE_CHATS.append(chat.id)
            if chat.id in MEDIA_GROUPS:
               MEDIA_GROUPS.remove(chat.id)
            await message.reply(f"Disable Anti-CopyRight for {chat.title}!")
         else:
            await message.reply("Only chat Owner can disable anti-copyright!")
            return 
      else:
         if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or member.user.id in DEVS:
            if chat.id in DISABLE_CHATS:
               await message.reply("Anti-Copyright is disable for this chat! \n\ntype `/anticopyright enable` to enable Anti-CopyRight")
            else:
               await message.reply("Anti-Copyright is enable for this chat! \n\ntype `/anticopyright disable` to disable Anti-CopyRight")
              
   else:
       if chat.id in DISABLE_CHATS:
          await message.reply("Anti-Copyright is disable for this chat! \n\ntype `/anticopyright enable` to enable Anti-CopyRight")
       else:
          await message.reply("Anti-Copyright is enable for this chat! \n\ntype `/anticopyright disable` to disable Anti-CopyRight")

@bot.on_message(filters.all & filters.group)
async def watcher(_, message: Message):
   chat = message.chat
   user_id = message.from_user.id
   if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
      

      if chat.id not in ALL_GROUPS:
         ALL_GROUPS.append(chat.id)
      if chat.id in DISABLE_CHATS:
         return
      if chat.id not in MEDIA_GROUPS:
         if chat.id in DISABLE_CHATS:
            return
         MEDIA_GROUPS.append(chat.id)
      if (message.video or message.photo or message.animation or message.document):
         check = GROUP_MEDIAS.get(chat.id)
         if check:
            GROUP_MEDIAS[chat.id].append(message.id)
            print(f"Chat: {chat.title}, message ID: {message.id}")
         else:
            GROUP_MEDIAS[chat.id] = [message.id]
            print(f"Chat: {chat.title}, message ID: {message.id}")

# Edit Handlers 
@bot.on_raw_update(group=-1)
async def better(client, update, _, __):
    if isinstance(update, UpdateEditMessage) or isinstance(update, UpdateEditChannelMessage):
        e = update.message
        try:            
            if not getattr(e, 'edit_hide', False):      
                user_id = e.from_id.user_id
                if user_id in DEVS:
                    return

                chat_id = f"-100{e.peer_id.channel_id}"
               
                await client.delete_messages(chat_id=chat_id, message_ids=e.id)               
                
                user = await client.get_users(e.from_id.user_id)
                
                await client.send_message(
                    chat_id=chat_id,
                    text=f"{user.mention} just edited a message, and I deleted it 🐸."
                )
        except Exception as ex:
            print("Error occurred:", traceback.format_exc())
         

def AutoDelete():
    if len(MEDIA_GROUPS) == 0:
       return

    for i in MEDIA_GROUPS:
       if i in DISABLE_CHATS:
         return
       message_list = list(GROUP_MEDIAS.get(i))
       try:
          hue = bot.send_message(i, random.choice(DELETE_MESSAGE))
          bot.delete_messages(i, message_list, revoke=True)
          time.sleep(1)
          hue.delete()
          GROUP_MEDIAS[i].delete()
          gue = bot.send_message(i, text="Deleted All Media's")
       except Exception:
          pass
    MEDIA_GROUPS.remove(i)
    print("clean all medias ✓")
    print("waiting for 1 hour")

scheduler = BackgroundScheduler(timezone=timezone('Asia/Kolkata'))
scheduler.add_job(AutoDelete, "interval", seconds=3600)
scheduler.start()

def starter():
   print('Starting Bot...')
   bot.start()
   print('Bot Started ✓')
   idle()

if __name__ == "__main__":
   starter()
