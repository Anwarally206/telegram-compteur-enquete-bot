from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os

# 🔐 TOKEN DU BOT
TOKEN = "8996673753:AAE-6TlNB4GvImu17jHn6Z8NR_LCFLdAd0I"

DATA_FILE = "data.json"

# Créer le fichier de données s'il n'existe pas
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Codes des établissements
CODES = {
    "medecine": "01",
    "egs": "02",
    "droit": "03",
    "lettres": "04",
    "sciences": "05",
    "ens": "06",
    "essa": "07",
    "espa": "08"
}

# Codes des années
ANNEES = {
    "L1": "01",
    "L2": "02",
    "L3": "03",
    "M1": "04",
    "M2": "05",
    "D": "D",      # Doctorant
    "INT7": "07",
    "INT8": "08",
    "TH": "TH"    # Thésard
}

# Commande /add
# Exemple : /add medecine L2
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Utilisation : /add <faculté> <année>\n"
            "Exemple : /add medecine L2"
        )
        return

    fac = context.args[0].lower()
    an = context.args[1].upper()

    if fac not in CODES or an not in ANNEES:
        await update.message.reply_text("❌ Faculté ou année invalide")
        return

    data = load_data()
    key = f"{fac}_{an}"

    data[key] = data.get(key, 0) + 1
    save_data(data)

    numero = f"{CODES[fac]}_{ANNEES[an]}_{data[key]:03d}"

    await update.message.reply_text(f"✅ Numéro attribué : {numero}")

# Lancement du bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("add", add))

print("🤖 Bot démarré...")
app.run_polling()
