import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), BaseHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ADMIN_ID = 8491918083 

WELCOME_MESSAGE = """👋 እንኳን ወደ Wollo KIOT Exam Support ቦት በሰላም መጡ!
ለፈተናዎ በጥራት ለመዘጋጀትና ውጤታማ ለመሆን ትክክለኛው ቦታ ላይ ነዎት! 🚀

________

📚 ስለ ፈተናዎቹ
እነዚህ ፈተናዎች በደንብ የተደራጁና የተለያዩ ዓመታትን የሚያካትቱ የወሎ ዩኒቨርሲቲ ብቻ የሆኑ Mid እና Final Exam ጥያቄዎች ናቸው።

👉 በዚህ ግሩፕ ውስጥ ከ 2011 ዓ.ም ጀምሮ በደንብ የተደራጁ Mid እና Final Exam ጥያቄዎች እና መልሶች ይገኛሉ!

በየዓመቱ ተመሳሳይ ወይም ተደጋጋሚ ጥያቄዎች ስለሚኖሩ፣ እነዚህን የበርካታ ዓመታት ጥያቄዎች ማግኘታችሁና በደንብ መለማመዳችሁ በዚህ ዓመት በምትፈተኑት Mid እና Final Exam ላይ ከፍተኛ ውጤት እንድታመጡ ይረዳችኋል።

🎯 ዛሬ የምታስመዘግቡት GPA የወደፊት ህይወታችሁ ነው! 🧑‍🎓📈🔥
📝📚 Study Hard → Score High → Build Your Future! 🚀🏆

________

💰 የአባልነት ክፍያ፦ 200 ብር ብቻ

💳 የክፍያ አማራጮች፦
• CBE (የኢትዮጵያ ንግድ ባንክ): 1000757377199 (ሀሚድ ታደሠ)
• Telebirr: 0953499240 (ሀሚድ ታደሠ)

📌 የአባልነት ሂደቱን ለማጠናቀቅ፦
200 ብር ክፍያውን ፈፅመው ሲጨርሱ የከፈሉበትን የባንክ ደረሰኝ (Screenshot ወይም ፎቶ) እዚሁ ቦት ላይ ይላኩልን። 
መረጃው እንደተረጋገጠ ወዲያውኑ የ VIP Exam Group መግቢያ ሊንክ ይደርስዎታል።

"ዛሬ የምታደርገው ጥረት የነገ ስኬትህ መሠረት ነው!" 📚✨"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # parse_mode ሳይጠቀም ቀጥታ ይልካል፤ ስለዚህ መልእክቱ በፍጹም አይቆረጥም
    await update.message.reply_text(WELCOME_MESSAGE)

async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ፎቶ ወይም ፋይል ሲላክ ብቻ ቀጥታ ወደ እርስዎ ይልካል
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )
    await update.message.reply_text("ደረሰኝዎ ደርሶናል! የ 200 ብር ክፍያዎ ተመዝግቧል። መረጃውን እያጣራን ስለሆነ በአጭር ጊዜ ውስጥ የ VIP ግሩፕ ሊንክ እንልክልዎታለን። አመሰግናለሁ! 🙏")

if __name__ == '__main__':
    TOKEN = "8810349395:AAE1BIKgfzGRGzMEphotfttUC2iTuqUeK8I"
    
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .pool_timeout(30.0)
        .build()
    )
    
    app.add_handler(CommandHandler("start", start))
    # ፎቶ ወይም Document ብቻ ሲላክ ወደ handle_receipt ይመራል፤ ጽሁፍ ከሆነ ግን አይመልስም
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_receipt))
    
    print("ቦቱ በትክክል እየሰራ ነው...")
    app.run_polling()
