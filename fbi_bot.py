import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

FBI_API = "https://api.fbi.gov/wanted/v1/list"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔎 FBI Search Bot\n\n"
        "Use:\n"
        "/search robbery\n"
        "/search fraud\n"
        "/search fugitive"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /search <keyword>")
        return

    query = " ".join(context.args)

    params = {
        "query": query,
        "pageSize": 1  # send one result to avoid spam
    }

    res = requests.get(FBI_API, params=params)
    data = res.json()

    if not data.get("items"):
        await update.message.reply_text("No results found.")
        return

    person = data["items"][0]

    name = person.get("title", "Unknown")
    desc = person.get("description", "No description")
    reward = person.get("reward_text", "N/A")
    url = person.get("url")

    image = None
    if person.get("images"):
        image = person["images"][0].get("original")

    caption = (
        f"👤 *{name}*\n\n"
        f"📝 {desc[:800]}...\n\n"
        f"💰 Reward: {reward}\n\n"
        f"🔗 {url}"
    )

    if image:
        await update.message.reply_photo(
            photo=image,
            caption=caption,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(caption, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    print("🤖 FBI Telegram Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
