"""
Assist Telegram Bot v2 — Registration, Payment & Broadcasting
@ownassistregbot
"""
import os,logging,string,random,httpx
from datetime import datetime,timedelta,timezone
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application,CommandHandler,CallbackQueryHandler,ContextTypes,MessageHandler,filters

BOT_TOKEN=os.environ.get("BOT_TOKEN","8615181875:AAF_YfKpDmlDR6eaIcuTbxtmbbaL_wur5Fw")
SUPA_URL=os.environ.get("SUPA_URL","https://hbzkaenywrybfuriavzw.supabase.co")
SUPA_KEY=os.environ.get("SUPA_KEY","sb_publishable_5U7Ddy46KpfXItCveLazrQ_rw51W4Jj")
SITE_URL="https://ownassist.app"
PRICE=315000
ADMIN_IDS=[]
H={"apikey":SUPA_KEY,"Authorization":f"Bearer {SUPA_KEY}","Content-Type":"application/json","Prefer":"return=representation"}

async def supa_insert(t,d):
    async with httpx.AsyncClient() as c: return (await c.post(f"{SUPA_URL}/rest/v1/{t}",json=d,headers=H)).json()
async def supa_get(t,q=""):
    async with httpx.AsyncClient() as c: return (await c.get(f"{SUPA_URL}/rest/v1/{t}?{q}&select=*",headers=H)).json()

async def save_sub(user):
    try:
        ex=await supa_get("bot_subscribers",f"telegram_id=eq.{user.id}")
        if not ex or len(ex)==0:
            await supa_insert("bot_subscribers",{"telegram_id":user.id,"username":user.username or "","first_name":user.first_name or "","is_active":True})
    except:pass

def gen_code():return f"AST-{''.join(random.choices(string.ascii_uppercase+string.digits,k=6))}"
logging.basicConfig(format="%(asctime)s-%(levelname)s-%(message)s",level=logging.INFO)
L=logging.getLogger(__name__)

# ═══ /start ═══
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    u=update.effective_user;await save_sub(u)
    t=("🌿 *ASSIST*\n_Own your life_\n\n"
       "━━━━━━━━━━━━━━━━━━\n\n"
       "Ты контролируешь свою жизнь?\nИли жизнь контролирует тебя?\n\n"
       "Узнай, как один инструмент может\nизменить всё 👇")
    kb=[[InlineKeyboardButton("🔥 Что такое Assist?",callback_data="about")],
        [InlineKeyboardButton("💳 Купить доступ — 315 000 сум",callback_data="buy")],
        [InlineKeyboardButton("🌐 Сайт",url=SITE_URL),InlineKeyboardButton("❓ FAQ",callback_data="faq")]]
    await update.message.reply_text(t,parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))

# ═══ About page 1 ═══
async def about(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query;await q.answer()
    t=("🌿 *ASSIST — Личный планер нового поколения*\n\n━━━━━━━━━━━━━━━━━━\n\n"
       "Представь: одно приложение, где собрана\nвся твоя жизнь. Не 5 разных приложений.\n"
       "Не Google таблица с формулами.\nОдин инструмент. Всё автоматически.\n\n"
       "📊 *ДАШБОРД*\nУтром открываешь — и видишь полную\nкартину дня: KPI, задачи, привычки,\nфинансы, настроение. Один экран.\n\n"
       "🎯 *ЦЕЛИ*\nКаждая цель с дедлайном, прогресс-баром\nи привязанными задачами. Видишь, как\nприближаешься к мечте каждый день.")
    kb=[[InlineKeyboardButton("Дальше →",callback_data="about2")],[InlineKeyboardButton("◀️ Назад",callback_data="back")]]
    await q.edit_message_text(t,parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))

# ═══ About page 2 ═══
async def about2(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query;await q.answer()
    t=("✅ *ЗАДАЧИ — Матрица Эйзенхауэра*\n\nВсе задачи распределяются по 4 квадрантам:\n"
       "🔴 Важно и срочно\n🟢 Важно, не срочно\n🟡 Срочно, не важно\n⚪ Не важно, не срочно\n\n"
       "Быстрое добавление, дедлайны, привязка к целям.\n\n"
       "💪 *ПРИВЫЧКИ*\n\nТрекер привычек в стиле календаря.\n"
       "Серии дней подряд 🔥, статистика выполнения,\nграфики прогресса за 30 дней.\n\n"
       "13 привычек? 30? Assist справится.")
    kb=[[InlineKeyboardButton("Дальше →",callback_data="about3")],[InlineKeyboardButton("◀️ Назад",callback_data="about")]]
    await q.edit_message_text(t,parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))

# ═══ About page 3 ═══
async def about3(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query;await q.answer()
    t=("💰 *ФИНАНСЫ — План / Факт*\n\nДоходы, расходы, долги, накопления —\nвсё в одном месте.\n\n"
       "• 16 категорий расходов\n• План и факт рядом\n• Диаграммы и графики\n"
       "• Выбор валюты: UZS, USD, RUB, KZT\n• Автоматические итоги\n\n"
       "Забудь про ручные формулы. Assist считает за тебя.\n\n"
       "━━━━━━━━━━━━━━━━━━\n\n"
       "💵 *Цена: 315 000 сум*\nОдна оплата. Доступ навсегда.\nБез подписки.\n\n"
       "Notion + Todoist + YNAB + Habitica =\n= *$396 каждый год* 😱\n\n"
       "Assist = *315 000 сум ОДИН РАЗ* 🎉\n\nЭкономия *$371* в первый год 💸")
    kb=[[InlineKeyboardButton("💳 Купить доступ сейчас",callback_data="buy")],[InlineKeyboardButton("◀️ В начало",callback_data="back")]]
    await q.edit_message_text(t,parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))

# ═══ FAQ ═══
async def faq(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query;await q.answer()
    t=("❓ *Часто задаваемые вопросы*\n\n"
       "*Что я получаю?*\nПожизненный доступ: дашборд, привычки,\nзадачи, цели, финансы.\n\n"
       "*Это подписка?*\nНет. Одна оплата — навсегда.\n\n"
       "*Как получить доступ?*\nОплатили → получили ссылку →\nзарегистрировались → пользуетесь.\n\n"
       "*Работает на телефоне?*\nДа.\n\n"
       "*Чем лучше Google Sheets?*\nВсё автоматически. Одно приложение\nвместо трёх файлов. Графики. KPI.")
    kb=[[InlineKeyboardButton("💳 Купить доступ",callback_data="buy")],[InlineKeyboardButton("◀️ Назад",callback_data="back")]]
    await q.edit_message_text(t,parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))

# ═══ Buy ═══
async def buy(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query;await q.answer()
    t="💳 *Оплата доступа к Assist*\n\nСумма: *315 000 сум*\nДоступ: *пожизненный* ♾\n\nВыберите способ оплаты:"
    kb=[[InlineKeyboardButton("📱 Payme",callback_data="payme")],[InlineKeyboardButton("📱 Click",callback_data="click")],
        [InlineKeyboardButton("💳 Перевод на карту",callback_data="card")],[InlineKeyboardButton("◀️ Назад",callback_data="back")]]
    await q.edit_message_text(t,parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))

# ═══ Pay card ═══
async def card(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query;await q.answer()
    t="💳 *Оплата переводом*\n\nПереведите *315 000 сум* на карту:\n\n`9860120102703556`\nSamanov Jaxongir\n\nПосле перевода отправьте скриншот чека 📎"
    kb=[[InlineKeyboardButton("✅ Я оплатил, отправляю чек",callback_data="receipt")],[InlineKeyboardButton("◀️ Назад",callback_data="buy")]]
    await q.edit_message_text(t,parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))

async def payme(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query;await q.answer()
    kb=[[InlineKeyboardButton("💳 Перевод на карту",callback_data="card")],[InlineKeyboardButton("◀️ Назад",callback_data="buy")]]
    await q.edit_message_text("📱 *Payme*\n\n⏳ Подключение в процессе.\nПока доступна оплата переводом.",parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))

async def click(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query;await q.answer()
    kb=[[InlineKeyboardButton("💳 Перевод на карту",callback_data="card")],[InlineKeyboardButton("◀️ Назад",callback_data="buy")]]
    await q.edit_message_text("📱 *Click*\n\n⏳ Подключение в процессе.\nПока доступна оплата переводом.",parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))

# ═══ Receipt ═══
async def receipt(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query;await q.answer()
    context.user_data["awaiting_receipt"]=True
    await q.edit_message_text("📎 *Отправьте скриншот чека* в этот чат.",parse_mode="Markdown")

async def photo(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_receipt"):return
    u=update.effective_user;context.user_data["awaiting_receipt"]=False
    code=gen_code();link=f"{SITE_URL}/auth/?code={code}"
    try:
        await supa_insert("licenses",{"code":code,"telegram_id":u.id,"telegram_username":u.username or "","status":"active","amount":PRICE,"payment_method":"card_transfer","expires_at":(datetime.now(timezone.utc)+timedelta(hours=24)).isoformat()})
    except Exception as e:L.error(f"Supabase: {e}")
    await update.message.reply_text(f"✅ *Чек получен!*\n\nСсылка для регистрации:\n🔗 [Зарегистрироваться]({link})\n\nИли скопируйте:\n`{link}`\n\n⚠️ Одноразовая, 24 часа.\nПосле регистрации входите через email+пароль.",parse_mode="Markdown")
    for a in ADMIN_IDS:
        try:await context.bot.send_message(a,f"🔔 Оплата! {u.first_name} (@{u.username})\nКод: {code}")
        except:pass

# ═══ Back ═══
async def back(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query;await q.answer()
    t=("🌿 *ASSIST*\n_Own your life_\n\n━━━━━━━━━━━━━━━━━━\n\n"
       "Ты контролируешь свою жизнь?\nИли жизнь контролирует тебя?\n\nУзнай, как один инструмент может\nизменить всё 👇")
    kb=[[InlineKeyboardButton("🔥 Что такое Assist?",callback_data="about")],
        [InlineKeyboardButton("💳 Купить доступ — 315 000 сум",callback_data="buy")],
        [InlineKeyboardButton("🌐 Сайт",url=SITE_URL),InlineKeyboardButton("❓ FAQ",callback_data="faq")]]
    await q.edit_message_text(t,parse_mode="Markdown",reply_markup=InlineKeyboardMarkup(kb))

# ═══ Admin ═══
async def cmd_generate(update:Update,context:ContextTypes.DEFAULT_TYPE):
    code=gen_code();link=f"{SITE_URL}/auth/?code={code}"
    try:await supa_insert("licenses",{"code":code,"telegram_id":update.effective_user.id,"telegram_username":update.effective_user.username or "","status":"active","amount":PRICE,"payment_method":"admin","expires_at":(datetime.now(timezone.utc)+timedelta(hours=72)).isoformat()})
    except Exception as e:await update.message.reply_text(f"Ошибка: {e}");return
    await update.message.reply_text(f"✅ Код: `{code}`\nСсылка: {link}\n72ч",parse_mode="Markdown")

async def cmd_stats(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        lic=await supa_get("licenses");subs=await supa_get("bot_subscribers")
        total=len(lic) if isinstance(lic,list) else 0
        used=sum(1 for d in lic if d.get("status")=="used") if isinstance(lic,list) else 0
        sc=len(subs) if isinstance(subs,list) else 0
        await update.message.reply_text(f"📊 *Статистика*\n\nПодписчики: {sc}\nЛицензий: {total}\nИспользовано: {used}\nВыручка: {used*PRICE:,} сум",parse_mode="Markdown")
    except Exception as e:await update.message.reply_text(f"Ошибка: {e}")

async def cmd_broadcast(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if not context.args:await update.message.reply_text("/broadcast Текст");return
    msg=" ".join(context.args)
    try:
        subs=await supa_get("bot_subscribers","is_active=eq.true")
        s=f=0
        for sub in subs:
            try:await context.bot.send_message(sub["telegram_id"],msg,parse_mode="Markdown");s+=1
            except:f+=1
        await update.message.reply_text(f"📤 Отправлено: {s}, ошибок: {f}")
    except Exception as e:await update.message.reply_text(f"Ошибка: {e}")

async def txt(update:Update,context:ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_receipt"):await update.message.reply_text("📎 Отправьте *фото чека*.",parse_mode="Markdown");return
    kb=[[InlineKeyboardButton("🔥 Что такое Assist?",callback_data="about")],[InlineKeyboardButton("💳 Купить доступ",callback_data="buy")]]
    await update.message.reply_text("Выберите:",reply_markup=InlineKeyboardMarkup(kb))

def main():
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("generate",cmd_generate))
    app.add_handler(CommandHandler("stats",cmd_stats))
    app.add_handler(CommandHandler("broadcast",cmd_broadcast))
    for name,fn in [("about",about),("about2",about2),("about3",about3),("buy",buy),("faq",faq),("payme",payme),("click",click),("card",card),("receipt",receipt),("back",back)]:
        app.add_handler(CallbackQueryHandler(fn,pattern=f"^{name}$"))
    app.add_handler(MessageHandler(filters.PHOTO,photo))
    app.add_handler(MessageHandler(filters.TEXT&~filters.COMMAND,txt))
    L.info("Bot v2 starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__=="__main__":main()
