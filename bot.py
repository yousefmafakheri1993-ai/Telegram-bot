# -*- coding: utf-8 -*-
import re
import asyncio
from collections import defaultdict
from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = "8526472606:AAHXSHp1C5CNjTOfMv2sekfNcR4b6iqQNhA"

OWNER_ID = 441555530

ORDER_ID = "@bane_tell"
PHONE = "09185553405"
MAIN_CHANNEL = "https://t.me/+SX5jPFOIHpHypd8X"

media_groups = defaultdict(list)

def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'09\d{9}', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def increase_price(price):
    if price < 10000: return price + 1000
    elif price < 20000: return price + 2000
    elif price < 30000: return price + 2000
    elif price < 40000: return price + 3000
    elif price < 50000: return price + 4000
    elif price < 90000: return price + 5000
    elif price < 210000: return price + 10000
    elif price < 300000: return price + 15000
    elif price < 400000: return price + 20000
    elif price < 500000: return price + 30000
    elif price < 900000: return price + 40000
    elif price < 1500000: return price + 60000
    elif price < 2000000: return price + 90000
    elif price < 3000000: return price + 100000
    elif price < 5000000: return price + 200000
    elif price < 8000000: return price + 300000
    elif price < 15000000: return price + 400000
    else: return price

def build_caption(text):
    text = clean_text(text)
    match = re.search(r'(\d[\d,]*)', text)
    price_line = ""
    if match:
        old_price = int(match.group(1).replace(',', ''))
        new_price = increase_price(old_price)
        price_line = f"{new_price:,} تومان"

    lines = text.split('\n')
    title = lines[0] if lines else ""
    description = "\n".join(lines[1:4]) if len(lines) > 1 else "کيفيت عالي و ضمانت تست"

    caption = f"""{title}
{description}

{price_line}

?? {ORDER_ID}
?? {PHONE}
{MAIN_CHANNEL}
"""
    return caption

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    message = update.message

    if message.media_group_id:
        media_groups[message.media_group_id].append(message)
        await asyncio.sleep(1)

        group = media_groups.pop(message.media_group_id)
        caption_text = group[0].caption or ""
        new_caption = build_caption(caption_text)

        media_list = []

        for i, msg in enumerate(group):
            if msg.photo:
                media_list.append(
                    InputMediaPhoto(
                        msg.photo[-1].file_id,
                        caption=new_caption if i == 0 else None
                    )
                )
            elif msg.video:
                media_list.append(
                    InputMediaVideo(
                        msg.video.file_id,
                        caption=new_caption if i == 0 else None
                    )
                )

        await message.reply_media_group(media_list)

    else:
        caption_text = message.caption or message.text or ""
        new_caption = build_caption(caption_text)

        if message.photo:
            await message.reply_photo(message.photo[-1].file_id, caption=new_caption)
        elif message.video:
            await message.reply_video(message.video.file_id, caption=new_caption)
        else:
            await message.reply_text(new_caption)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("پست رو بفرست.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_message))

app.run_polling()