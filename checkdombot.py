from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# 🔑 Token bot và API key
BOT_TOKEN = "7546640675:AAGh1YW8aifzIm1YJnFprR4a9iSY74tKbL8"
CMC_API_KEY = "64dc7e84-d42b-4a0c-95e4-c8644e0eac91"

# 📊 Lấy dữ liệu Dominance từ CoinMarketCap
def get_dominance_from_cmc():
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()['data']

    btc_dominance = data['btc_dominance']
    eth_dominance = data['eth_dominance']
    alt_dominance = 100 - btc_dominance
    total_market_cap = data['quote']['USD']['total_market_cap']

    return btc_dominance, eth_dominance, alt_dominance, total_market_cap

# 📩 Xử lý lệnh /dominance
async def get_dominance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        btc, eth, alt, market_cap = get_dominance_from_cmc()
        market_cap_billion = market_cap / 1_000_000_000

        # 🚦 Xác định Season theo công thức BTC Dominance
        if btc >= 51:
            season = f"⚡ Bitcoin Season ({btc:.2f}%)"
        elif btc <= 50:
            season = f"🔥 Altcoin Season ({btc:.2f}%)"
        else:
            season = f"📉 Neutral Season ({btc:.2f}%)"

        message = (
            f"📊 *Chỉ số thị trường hiện tại:*\n\n"
            f"• Dominance BTC: *{btc:.2f}%*\n"
            f"• Dominance ETH: *{eth:.2f}%*\n"
            f"• Dominance Altcoin: *{alt:.2f}%*\n"
            f"• Tổng vốn hoá thị trường: *${market_cap_billion:,.2f} tỷ USD*\n\n"
            f"🚀 *Trạng thái thị trường:* _{season}_"
        )
        await update.message.reply_text(message, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi lấy dữ liệu: {e}")

# 🚀 Khởi động bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler(["dominance", "dom"], get_dominance))
    print("🤖 Bot đang chạy...")
    app.run_polling()
