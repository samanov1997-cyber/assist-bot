"""
Assist Telegram Bot — Registration & Payment
@ownassistregbot

Handles: welcome → product info → payment → license generation → Supabase
"""

import os
import logging
import string
import random
from datetime import datetime, timedelta, timezone

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)

# ═══ CONFIG ═══
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8615181875:AAF_YfKpDmlDR6eaIcuTbxtmbbaL_wur5Fw")
SUPA_URL = os.environ.get("SUPA_URL", "https://hbzkaenywrybfuriavzw.supabase.co")
SUPA_KEY = os.environ.get("SUPA_KEY", "sb_publishable_5U7Ddy46KpfXItCveLazrQ_rw51W4Jj")
SITE_URL = "https://ownassist.app"
PRICE = 315_000  # UZS
ADMIN_ID = None  # Set your Telegram ID to receive notifications

# ═══ SUPABASE ═══
import httpx

async def supa_insert(table: str, data: dict) -> dict:
    """Insert a row into Supabase table."""
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{SUPA_URL}/rest/v1/{table}",
            json=data,
            headers={
                "apikey": SUPA_KEY,
                "Authorization": f"Bearer {SUPA_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
        )
        return r.json()

async def supa_update(table: str, match: dict, data: dict) -> dict:
    """Update rows in Supabase table."""
    params = "&".join(f"{k}=eq.{v}" for k, v in match.items())
    async with httpx.AsyncClient() as client:
        r = await client.patch(
            f"{SUPA_URL}/rest/v1/{table}?{params}",
            json=data,
            headers={
                "apikey": SUPA_KEY,
                "Authorization": f"Bearer {SUPA_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
        )
        return r.json()

async def supa_select(table: str, match: dict) -> list:
    """Select rows from Supabase table."""
    params = "&".join(f"{k}=eq.{v}" for k, v in match.items())
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{SUPA_URL}/rest/v1/{table}?{params}",
            headers={
                "apikey": SUPA_KEY,
                "Authorization": f"Bearer {SUPA_KEY}",
            }
        )
        return r.json()


# ═══ HELPERS ═══
def generate_code() -> str:
    """Generate unique license code like AST-7X9K2M."""
    chars = string.ascii_uppercase + string.digits
    part = ''.join(random.choices(chars, k=6))
    return f"AST-{part}"


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ═══ HANDLERS ═══

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message with product info."""
    user = update.effective_user
    
    text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "🌿 *Assist* — личный планер нового поколения.\n\n"
        "Что внутри:\n"
        "🎯 Цели с прогресс-трекером\n"
        "✅ Матрица задач Эйзенхауэра\n"
        "💪 Трекер привычек\n"
        "💰 Финансы: план / факт\n"
        "📊 Дашборд с KPI\n"
        "😊 Трекер настроения\n\n"
        "💵 *Цена: 315 000 сум* — разовая оплата, доступ навсегда.\n"
        "Без подписки. Без скрытых платежей.\n\n"
        "Нажмите кнопку ниже 👇"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 Купить доступ — 315 000 сум", callback_data="buy")],
        [InlineKeyboardButton("👀 Демо-версия", url=f"{SITE_URL}/app/?demo=1")],
        [InlineKeyboardButton("🌐 Сайт", url=SITE_URL),
         InlineKeyboardButton("❓ FAQ", callback_data="faq")],
    ]
    
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def faq_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """FAQ answers."""
    query = update.callback_query
    await query.answer()
    
    text = (
        "❓ *Часто задаваемые вопросы*\n\n"
        "*Что я получаю за 315 000 сум?*\n"
        "Пожизненный доступ к веб-приложению Assist: "
        "дашборд, привычки, задачи, цели, финансы.\n\n"
        "*Это подписка?*\n"
        "Нет. Одна оплата — доступ навсегда.\n\n"
        "*Как получить доступ после оплаты?*\n"
        "После оплаты бот отправит вам ссылку для регистрации. "
        "Нажимаете → заполняете имя, email, пароль → готово.\n\n"
        "*Работает на телефоне?*\n"
        "Да, Assist адаптирован под мобильные устройства.\n\n"
        "*Могу вернуть деньги?*\n"
        "Да, в течение 14 дней после покупки.\n\n"
        "*Есть демо?*\n"
        "Да! Нажмите «Демо-версия» чтобы посмотреть планер."
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 Купить доступ", callback_data="buy")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_to_start")],
    ]
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show payment options."""
    query = update.callback_query
    await query.answer()
    
    text = (
        "💳 *Оплата доступа к Assist*\n\n"
        "Сумма: *315 000 сум*\n"
        "Доступ: *пожизненный*\n\n"
        "Выберите способ оплаты:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📱 Payme", callback_data="pay_payme")],
        [InlineKeyboardButton("📱 Click", callback_data="pay_click")],
        [InlineKeyboardButton("💳 Перевод на карту", callback_data="pay_card")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back_to_start")],
    ]
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def pay_card_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manual card transfer instructions."""
    query = update.callback_query
    await query.answer()
    
    text = (
        "💳 *Оплата переводом на карту*\n\n"
        "Переведите *315 000 сум* на карту:\n\n"
        "`9860 **** **** 3556`\n"
        "Samanov Jakhongir\n"
        "Aloqabank (Humo)\n\n"
        "После перевода отправьте скриншот чека в этот чат.\n"
        "Мы проверим и отправим вам ссылку для регистрации "
        "в течение 15 минут (в рабочее время)."
    )
    
    keyboard = [
        [InlineKeyboardButton("✅ Я оплатил, отправляю чек", callback_data="sent_receipt")],
        [InlineKeyboardButton("◀️ Назад к способам оплаты", callback_data="buy")],
    ]
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def pay_payme_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Payme payment — redirect or instructions."""
    query = update.callback_query
    await query.answer()
    
    # TODO: Replace with real Payme merchant link when approved
    # Format: https://checkout.paycom.uz/MERCHANT_ID?amount=31500000&account[user_id]=TELEGRAM_ID
    
    text = (
        "📱 *Оплата через Payme*\n\n"
        "⏳ Payme мерчант в процессе подключения.\n\n"
        "Пока вы можете оплатить переводом на карту "
        "или через Click.\n\n"
        "_Как только Payme будет подключен, этот способ "
        "станет доступен автоматически._"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 Перевод на карту", callback_data="pay_card")],
        [InlineKeyboardButton("◀️ Назад", callback_data="buy")],
    ]
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def pay_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Click payment — redirect or instructions."""
    query = update.callback_query
    await query.answer()
    
    # TODO: Replace with real Click merchant link when approved
    # Format: https://my.click.uz/services/pay?service_id=SID&merchant_id=MID&amount=315000&transaction_param=TELEGRAM_ID
    
    text = (
        "📱 *Оплата через Click*\n\n"
        "⏳ Click мерчант в процессе подключения.\n\n"
        "Пока вы можете оплатить переводом на карту.\n\n"
        "_Как только Click будет подключен, этот способ "
        "станет доступен автоматически._"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 Перевод на карту", callback_data="pay_card")],
        [InlineKeyboardButton("◀️ Назад", callback_data="buy")],
    ]
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def sent_receipt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User says they sent receipt."""
    query = update.callback_query
    await query.answer()
    
    text = (
        "📎 *Отправьте скриншот чека* прямо в этот чат.\n\n"
        "Мы проверим оплату и отправим ссылку "
        "для регистрации."
    )
    
    context.user_data["awaiting_receipt"] = True
    
    await query.edit_message_text(text, parse_mode="Markdown")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle receipt photo — generate license."""
    if not context.user_data.get("awaiting_receipt"):
        return
    
    user = update.effective_user
    context.user_data["awaiting_receipt"] = False
    
    # Generate license code
    code = generate_code()
    reg_link = f"{SITE_URL}/auth/?code={code}"
    
    # Save to Supabase
    try:
        await supa_insert("licenses", {
            "code": code,
            "telegram_id": user.id,
            "telegram_username": user.username or "",
            "status": "active",
            "amount": PRICE,
            "payment_method": "card_transfer",
            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat(),
        })
        logger.info(f"License created: {code} for @{user.username} (ID: {user.id})")
    except Exception as e:
        logger.error(f"Supabase error: {e}")
    
    # Send registration link
    text = (
        "✅ *Чек получен!*\n\n"
        "Мы проверим оплату в ближайшее время. "
        "А пока — вот ваша ссылка для регистрации:\n\n"
        f"🔗 [Зарегистрироваться в Assist]({reg_link})\n\n"
        f"Или скопируйте:\n`{reg_link}`\n\n"
        "⚠️ Ссылка одноразовая и действует 24 часа.\n\n"
        "После регистрации вы сможете входить "
        "через email и пароль с любого устройства."
    )
    
    await update.message.reply_text(text, parse_mode="Markdown")
    
    # Notify admin
    if ADMIN_ID:
        admin_text = (
            f"🔔 Новая оплата!\n\n"
            f"Пользователь: {user.first_name} (@{user.username})\n"
            f"Telegram ID: {user.id}\n"
            f"Код: {code}\n"
            f"Метод: перевод на карту\n"
            f"Сумма: {PRICE:,} сум"
        )
        try:
            await context.bot.send_message(ADMIN_ID, admin_text)
        except:
            pass


async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to main menu."""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    
    text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "🌿 *Assist* — личный планер нового поколения.\n\n"
        "Что внутри:\n"
        "🎯 Цели с прогресс-трекером\n"
        "✅ Матрица задач Эйзенхауэра\n"
        "💪 Трекер привычек\n"
        "💰 Финансы: план / факт\n"
        "📊 Дашборд с KPI\n"
        "😊 Трекер настроения\n\n"
        "💵 *Цена: 315 000 сум* — разовая оплата, доступ навсегда.\n"
        "Без подписки. Без скрытых платежей.\n\n"
        "Нажмите кнопку ниже 👇"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 Купить доступ — 315 000 сум", callback_data="buy")],
        [InlineKeyboardButton("👀 Демо-версия", url=f"{SITE_URL}/app/?demo=1")],
        [InlineKeyboardButton("🌐 Сайт", url=SITE_URL),
         InlineKeyboardButton("❓ FAQ", callback_data="faq")],
    ]
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ═══ ADMIN COMMANDS ═══

async def admin_generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to manually generate a license. Usage: /generate"""
    user = update.effective_user
    
    code = generate_code()
    reg_link = f"{SITE_URL}/auth/?code={code}"
    
    try:
        await supa_insert("licenses", {
            "code": code,
            "telegram_id": user.id,
            "telegram_username": user.username or "",
            "status": "active",
            "amount": PRICE,
            "payment_method": "admin_manual",
            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=72)).isoformat(),
        })
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")
        return
    
    text = (
        f"✅ Лицензия создана!\n\n"
        f"Код: `{code}`\n"
        f"Ссылка: {reg_link}\n"
        f"Действует: 72 часа"
    )
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to view stats. Usage: /stats"""
    try:
        all_licenses = await supa_select("licenses", {})
        # supa_select with no match returns all — we need a different approach
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{SUPA_URL}/rest/v1/licenses?select=status",
                headers={"apikey": SUPA_KEY, "Authorization": f"Bearer {SUPA_KEY}"}
            )
            data = r.json()
        
        total = len(data)
        active = sum(1 for d in data if d["status"] == "active")
        used = sum(1 for d in data if d["status"] == "used")
        
        text = (
            f"📊 *Статистика Assist*\n\n"
            f"Всего лицензий: {total}\n"
            f"Активных: {active}\n"
            f"Использовано: {used}\n"
            f"Выручка: {used * PRICE:,} сум"
        )
        
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any text message."""
    if context.user_data.get("awaiting_receipt"):
        await update.message.reply_text(
            "📎 Пожалуйста, отправьте *скриншот чека* (фото).",
            parse_mode="Markdown"
        )
        return
    
    # Default response
    keyboard = [
        [InlineKeyboardButton("💳 Купить доступ", callback_data="buy")],
        [InlineKeyboardButton("👀 Демо-версия", url=f"{SITE_URL}/app/?demo=1")],
    ]
    
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ═══ MAIN ═══

def main():
    """Start the bot."""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", admin_generate))
    app.add_handler(CommandHandler("stats", admin_stats))
    
    # Callbacks
    app.add_handler(CallbackQueryHandler(buy_handler, pattern="^buy$"))
    app.add_handler(CallbackQueryHandler(faq_handler, pattern="^faq$"))
    app.add_handler(CallbackQueryHandler(pay_payme_handler, pattern="^pay_payme$"))
    app.add_handler(CallbackQueryHandler(pay_click_handler, pattern="^pay_click$"))
    app.add_handler(CallbackQueryHandler(pay_card_handler, pattern="^pay_card$"))
    app.add_handler(CallbackQueryHandler(sent_receipt_handler, pattern="^sent_receipt$"))
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="^back_to_start$"))
    
    # Messages
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    logger.info("Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
