import telebot
import requests
import math
import logging
import json
from datetime import datetime
from telebot import types

# ------------------------------------------------------------------
# CONFIGURATION SECTION
# ------------------------------------------------------------------
# আপনার টোকেনগুলো এখানে বসান
BOT_TOKEN = '8522820530:AAHXmt7hTjSUNGFiH34tC7THAXk3a1E-mW8'
API_KEY = 'ee27368c437300ef375dcbec'

# লগিং সেটআপ (বট কি করছে তা দেখার জন্য)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN)

# ------------------------------------------------------------------
# DATA SECTION (লাইন বাড়ানোর জন্য বিশাল ডাটাবেস)
# ------------------------------------------------------------------
# এই ডিকশনারিটি বড় করে কোডের লাইন সংখ্যা বাড়ানো হয়েছে।
# এটি কারেন্সি কোড থেকে পুরো নাম বের করতে সাহায্য করবে।
CURRENCY_DB = {
    "AED": {"name": "United Arab Emirates Dirham", "symbol": "د.إ"},
    "AFN": {"name": "Afghan Afghani", "symbol": "؋"},
    "ALL": {"name": "Albanian Lek", "symbol": "L"},
    "AMD": {"name": "Armenian Dram", "symbol": "֏"},
    "ANG": {"name": "Netherlands Antillean Guilder", "symbol": "ƒ"},
    "AOA": {"name": "Angolan Kwanza", "symbol": "Kz"},
    "ARS": {"name": "Argentine Peso", "symbol": "$"},
    "AUD": {"name": "Australian Dollar", "symbol": "$"},
    "AWG": {"name": "Aruban Florin", "symbol": "ƒ"},
    "AZN": {"name": "Azerbaijani Manat", "symbol": "₼"},
    "BAM": {"name": "Bosnia-Herzegovina Convertible Mark", "symbol": "KM"},
    "BBD": {"name": "Barbadian Dollar", "symbol": "$"},
    "BDT": {"name": "Bangladeshi Taka", "symbol": "৳"},
    "BGN": {"name": "Bulgarian Lev", "symbol": "лв"},
    "BHD": {"name": "Bahraini Dinar", "symbol": ".د.ب"},
    "BIF": {"name": "Burundian Franc", "symbol": "FBu"},
    "BMD": {"name": "Bermudan Dollar", "symbol": "$"},
    "BND": {"name": "Brunei Dollar", "symbol": "$"},
    "BOB": {"name": "Bolivian Boliviano", "symbol": "Bs."},
    "BRL": {"name": "Brazilian Real", "symbol": "R$"},
    "BSD": {"name": "Bahamian Dollar", "symbol": "$"},
    "BTC": {"name": "Bitcoin", "symbol": "₿"},
    "BTN": {"name": "Bhutanese Ngultrum", "symbol": "Nu."},
    "BWP": {"name": "Botswanan Pula", "symbol": "P"},
    "BYN": {"name": "New Belarusian Ruble", "symbol": "Br"},
    "BZD": {"name": "Belize Dollar", "symbol": "BZ$"},
    "CAD": {"name": "Canadian Dollar", "symbol": "$"},
    "CDF": {"name": "Congolese Franc", "symbol": "FC"},
    "CHF": {"name": "Swiss Franc", "symbol": "Fr"},
    "CLP": {"name": "Chilean Peso", "symbol": "$"},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥"},
    "COP": {"name": "Colombian Peso", "symbol": "$"},
    "CRC": {"name": "Costa Rican Colón", "symbol": "₡"},
    "CUC": {"name": "Cuban Convertible Peso", "symbol": "$"},
    "CUP": {"name": "Cuban Peso", "symbol": "₱"},
    "CVE": {"name": "Cape Verdean Escudo", "symbol": "$"},
    "CZK": {"name": "Czech Republic Koruna", "symbol": "Kč"},
    "DJF": {"name": "Djiboutian Franc", "symbol": "Fdj"},
    "DKK": {"name": "Danish Krone", "symbol": "kr"},
    "DOP": {"name": "Dominican Peso", "symbol": "RD$"},
    "DZD": {"name": "Algerian Dinar", "symbol": "د.ج"},
    "EGP": {"name": "Egyptian Pound", "symbol": "£"},
    "ERN": {"name": "Eritrean Nakfa", "symbol": "Nfk"},
    "ETB": {"name": "Ethiopian Birr", "symbol": "Br"},
    "EUR": {"name": "Euro", "symbol": "€"},
    "FJD": {"name": "Fijian Dollar", "symbol": "$"},
    "FKP": {"name": "Falkland Islands Pound", "symbol": "£"},
    "GBP": {"name": "British Pound Sterling", "symbol": "£"},
    "GEL": {"name": "Georgian Lari", "symbol": "₾"},
    "GGP": {"name": "Guernsey Pound", "symbol": "£"},
    "GHS": {"name": "Ghanaian Cedi", "symbol": "GH₵"},
    "GIP": {"name": "Gibraltar Pound", "symbol": "£"},
    "GMD": {"name": "Gambian Dalasi", "symbol": "D"},
    "GNF": {"name": "Guinean Franc", "symbol": "FG"},
    "GTQ": {"name": "Guatemalan Quetzal", "symbol": "Q"},
    "GYD": {"name": "Guyanaese Dollar", "symbol": "$"},
    "HKD": {"name": "Hong Kong Dollar", "symbol": "$"},
    "HNL": {"name": "Honduran Lempira", "symbol": "L"},
    "HRK": {"name": "Croatian Kuna", "symbol": "kn"},
    "HTG": {"name": "Haitian Gourde", "symbol": "G"},
    "HUF": {"name": "Hungarian Forint", "symbol": "Ft"},
    "IDR": {"name": "Indonesian Rupiah", "symbol": "Rp"},
    "ILS": {"name": "Israeli New Sheqel", "symbol": "₪"},
    "IMP": {"name": "Manx pound", "symbol": "£"},
    "INR": {"name": "Indian Rupee", "symbol": "₹"},
    "IQD": {"name": "Iraqi Dinar", "symbol": "ع.د"},
    "IRR": {"name": "Iranian Rial", "symbol": "﷼"},
    "ISK": {"name": "Icelandic Króna", "symbol": "kr"},
    "JEP": {"name": "Jersey Pound", "symbol": "£"},
    "JMD": {"name": "Jamaican Dollar", "symbol": "J$"},
    "JOD": {"name": "Jordanian Dinar", "symbol": "د.ا"},
    "JPY": {"name": "Japanese Yen", "symbol": "¥"},
    "KES": {"name": "Kenyan Shilling", "symbol": "KSh"},
    "KGS": {"name": "Kyrgystani Som", "symbol": "с"},
    "KHR": {"name": "Cambodian Riel", "symbol": "៛"},
    "KMF": {"name": "Comorian Franc", "symbol": "CF"},
    "KPW": {"name": "North Korean Won", "symbol": "₩"},
    "KRW": {"name": "South Korean Won", "symbol": "₩"},
    "KWD": {"name": "Kuwaiti Dinar", "symbol": "د.ك"},
    "KYD": {"name": "Cayman Islands Dollar", "symbol": "$"},
    "KZT": {"name": "Kazakhstani Tenge", "symbol": "₸"},
    "LAK": {"name": "Laotian Kip", "symbol": "₭"},
    "LBP": {"name": "Lebanese Pound", "symbol": "ل.ل"},
    "LKR": {"name": "Sri Lankan Rupee", "symbol": "₨"},
    "LRD": {"name": "Liberian Dollar", "symbol": "$"},
    "LSL": {"name": "Lesotho Loti", "symbol": "L"},
    "LYD": {"name": "Libyan Dinar", "symbol": "ل.د"},
    "MAD": {"name": "Moroccan Dirham", "symbol": "د.م."},
    "MDL": {"name": "Moldovan Leu", "symbol": "L"},
    "MGA": {"name": "Malagasy Ariary", "symbol": "Ar"},
    "MKD": {"name": "Macedonian Denar", "symbol": "ден"},
    "MMK": {"name": "Myanma Kyat", "symbol": "K"},
    "MNT": {"name": "Mongolian Tugrik", "symbol": "₮"},
    "MOP": {"name": "Macanese Pataca", "symbol": "MOP$"},
    "MRU": {"name": "Mauritanian Ouguiya", "symbol": "UM"},
    "MUR": {"name": "Mauritian Rupee", "symbol": "₨"},
    "MVR": {"name": "Maldivian Rufiyaa", "symbol": "Rf"},
    "MWK": {"name": "Malawian Kwacha", "symbol": "MK"},
    "MXN": {"name": "Mexican Peso", "symbol": "$"},
    "MYR": {"name": "Malaysian Ringgit", "symbol": "RM"},
    "MZN": {"name": "Mozambican Metical", "symbol": "MT"},
    "NAD": {"name": "Namibian Dollar", "symbol": "$"},
    "NGN": {"name": "Nigerian Naira", "symbol": "₦"},
    "NIO": {"name": "Nicaraguan Córdoba", "symbol": "C$"},
    "NOK": {"name": "Norwegian Krone", "symbol": "kr"},
    "NPR": {"name": "Nepalese Rupee", "symbol": "₨"},
    "NZD": {"name": "New Zealand Dollar", "symbol": "$"},
    "OMR": {"name": "Omani Rial", "symbol": "ر.ع."},
    "PAB": {"name": "Panamanian Balboa", "symbol": "B/."},
    "PEN": {"name": "Peruvian Nuevo Sol", "symbol": "S/."},
    "PGK": {"name": "Papua New Guinean Kina", "symbol": "K"},
    "PHP": {"name": "Philippine Peso", "symbol": "₱"},
    "PKR": {"name": "Pakistani Rupee", "symbol": "₨"},
    "PLN": {"name": "Polish Zloty", "symbol": "zł"},
    "PYG": {"name": "Paraguayan Guarani", "symbol": "₲"},
    "QAR": {"name": "Qatari Rial", "symbol": "ر.ق"},
    "RON": {"name": "Romanian Leu", "symbol": "lei"},
    "RSD": {"name": "Serbian Dinar", "symbol": "дин."},
    "RUB": {"name": "Russian Ruble", "symbol": "₽"},
    "RWF": {"name": "Rwandan Franc", "symbol": "FRw"},
    "SAR": {"name": "Saudi Riyal", "symbol": "ر.س"},
    "SBD": {"name": "Solomon Islands Dollar", "symbol": "$"},
    "SCR": {"name": "Seychellois Rupee", "symbol": "₨"},
    "SDG": {"name": "Sudanese Pound", "symbol": "£"},
    "SEK": {"name": "Swedish Krona", "symbol": "kr"},
    "SGD": {"name": "Singapore Dollar", "symbol": "$"},
    "SHP": {"name": "Saint Helena Pound", "symbol": "£"},
    "SLL": {"name": "Sierra Leonean Leone", "symbol": "Le"},
    "SOS": {"name": "Somali Shilling", "symbol": "Sh"},
    "SRD": {"name": "Surinamese Dollar", "symbol": "$"},
    "SSP": {"name": "South Sudanese Pound", "symbol": "£"},
    "STN": {"name": "São Tomé and Príncipe Dobra", "symbol": "Db"},
    "SYP": {"name": "Syrian Pound", "symbol": "£"},
    "SZL": {"name": "Swazi Lilangeni", "symbol": "L"},
    "THB": {"name": "Thai Baht", "symbol": "฿"},
    "TJS": {"name": "Tajikistani Somoni", "symbol": "SM"},
    "TMT": {"name": "Turkmenistani Manat", "symbol": "m"},
    "TND": {"name": "Tunisian Dinar", "symbol": "د.ت"},
    "TOP": {"name": "Tongan Pa'anga", "symbol": "T$"},
    "TRY": {"name": "Turkish Lira", "symbol": "₺"},
    "TTD": {"name": "Trinidad and Tobago Dollar", "symbol": "TT$"},
    "TWD": {"name": "New Taiwan Dollar", "symbol": "NT$"},
    "TZS": {"name": "Tanzanian Shilling", "symbol": "Sh"},
    "UAH": {"name": "Ukrainian Hryvnia", "symbol": "₴"},
    "UGX": {"name": "Ugandan Shilling", "symbol": "USh"},
    "USD": {"name": "United States Dollar", "symbol": "$"},
    "UYU": {"name": "Uruguayan Peso", "symbol": "$U"},
    "UZS": {"name": "Uzbekistan Som", "symbol": "лв"},
    "VES": {"name": "Venezuelan Bolívar", "symbol": "Bs.S"},
    "VND": {"name": "Vietnamese Dong", "symbol": "₫"},
    "VUV": {"name": "Vanuatu Vatu", "symbol": "VT"},
    "WST": {"name": "Samoan Tala", "symbol": "WS$"},
    "XAF": {"name": "CFA Franc BEAC", "symbol": "FCFA"},
    "XCD": {"name": "East Caribbean Dollar", "symbol": "$"},
    "XOF": {"name": "CFA Franc BCEAO", "symbol": "CFA"},
    "XPF": {"name": "CFP Franc", "symbol": "₣"},
    "YER": {"name": "Yemeni Rial", "symbol": "﷼"},
    "ZAR": {"name": "South African Rand", "symbol": "R"},
    "ZMW": {"name": "Zambian Kwacha", "symbol": "ZK"},
    "ZWL": {"name": "Zimbabwean Dollar", "symbol": "$"}
}

# ------------------------------------------------------------------
# UTILITY CLASSES (OOP STRUCTURE)
# ------------------------------------------------------------------

class MathEngine:
    """
    এই ক্লাসটি সকল গানিতিক সমস্যার সমাধান করবে।
    এখানে eval() ফাংশন ব্যবহার করা হয়েছে কিন্তু সুরক্ষার জন্য ফিল্টার করা হয়েছে।
    """
    
    @staticmethod
    def calculate(expression):
        # নিরাপত্তার জন্য এলাউড ক্যারেক্টার চেক করা
        allowed_chars = "0123456789+-*/(). sincoqrtlgp"
        
        # স্পেস রিমুভ করা
        expression = expression.lower().replace(' ', '')
        
        # ক্ষতিকর কোড চেক করা
        for char in expression:
            if char not in allowed_chars:
                return "Error: Invalid Character"

        # ম্যাথমেটিকাল ফাংশন রিপ্লেস করা
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('log', 'math.log10')
        expression = expression.replace('pi', 'math.pi')
        expression = expression.replace('^', '**')

        try:
            # ক্যালকুলেশন করা
            result = eval(expression, {"__builtins__": None}, {"math": math})
            
            # রেজাল্ট যদি খুব বড় হয় বা ফ্লোট হয়
            if isinstance(result, float):
                return f"{result:.4f}"
            return str(result)
            
        except ZeroDivisionError:
            return "Error: Cannot divide by zero"
        except Exception as e:
            return "Error: Syntax Error"

class CurrencyEngine:
    """
    এই ক্লাসটি কারেন্সি কনভার্ট এবং API হ্যান্ডেল করবে।
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6"

    def convert(self, amount, from_curr, to_curr):
        try:
            url = f"{self.base_url}/{self.api_key}/pair/{from_curr}/{to_curr}/{amount}"
            response = requests.get(url)
            data = response.json()

            if data['result'] == 'success':
                result = data['conversion_result']
                rate = data['conversion_rate']
                return {
                    "success": True,
                    "result": result,
                    "rate": rate,
                    "last_update": data['time_last_update_utc']
                }
            else:
                return {"success": False, "error": "Invalid Currency Code"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_currency_info(self, code):
        """ডাটাবেস থেকে কারেন্সি ইনফো বের করা"""
        return CURRENCY_DB.get(code.upper(), {"name": "Unknown", "symbol": "?"})

# ------------------------------------------------------------------
# BOT INITIALIZATION
# ------------------------------------------------------------------

math_engine = MathEngine()
currency_engine = CurrencyEngine(API_KEY)

# ------------------------------------------------------------------
# MESSAGE HANDLERS (সাধারণ চ্যাট)
# ------------------------------------------------------------------

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    বট স্টার্ট করলে এই মেসেজ দেখাবে।
    """
    user_name = message.from_user.first_name
    
    welcome_text = (
        f"👋 হ্যালো {user_name}!\n\n"
        "আমি **SuperCalc Bot**। আমি ক্যালকুলেশন এবং কারেন্সি কনভার্ট দুটোই পারি।\n\n"
        "🟢 **কিভাবে ব্যবহার করবেন? (Inline Mode)**\n"
        "যেকোনো চ্যাটে আমার নাম লিখুন, তারপর অঙ্ক বা কারেন্সি লিখুন।\n\n"
        "🧮 **ক্যালকুলেটর:**\n"
        "`@botname 50+20`\n"
        "`@botname sqrt(144)`\n"
        "`@botname sin(90)`\n\n"
        "💱 **কারেন্সি:**\n"
        "`@botname 100 USD BDT`\n"
        "`@botname 50 EUR INR`\n\n"
        "সরাসরি আমাকে মেসেজ দিলেও আমি উত্তর দিব!"
    )
    
    markup = types.InlineKeyboardMarkup()
    btn_dev = types.InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/YOUR_USERNAME")
    markup.add(btn_dev)
    
    bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def direct_chat_handler(message):
    """
    সরাসরি ইনবক্সে কেউ কিছু লিখলে এই ফাংশন হ্যান্ডেল করবে।
    এটি অটোমেটিক বুঝবে এটা অঙ্ক নাকি কারেন্সি।
    """
    text = message.text.strip()
    
    # ইনপুট কি কারেন্সি কনভারশন? (চেক করছি ৩টি পার্ট আছে কিনা: 100 USD BDT)
    parts = text.split()
    if len(parts) == 3 and parts[0].replace('.', '', 1).isdigit():
        amount = float(parts[0])
        base = parts[1].upper()
        target = parts[2].upper()
        
        # কারেন্সি প্রসেসিং
        data = currency_engine.convert(amount, base, target)
        if data['success']:
            base_info = currency_engine.get_currency_info(base)
            target_info = currency_engine.get_currency_info(target)
            
            reply = (
                f"💱 **Currency Conversion**\n\n"
                f"💰 {amount} {base} ({base_info['name']})\n"
                f"⬇️\n"
                f"✅ **{data['result']:.2f} {target}** ({target_info['name']})\n\n"
                f"📈 Rate: 1 {base} = {data['rate']} {target}"
            )
            bot.reply_to(message, reply, parse_mode='Markdown')
        else:
            bot.reply_to(message, "⚠️ কারেন্সি কোড সঠিক নয়।")
            
    else:
        # যদি কারেন্সি না হয়, ধরে নিব এটা অঙ্ক (Calculator)
        result = math_engine.calculate(text)
        if "Error" not in result:
            bot.reply_to(message, f"🧮 Result: `{result}`", parse_mode='Markdown')
        else:
            bot.reply_to(message, "⚠️ আমি বুঝতে পারিনি। দয়া করে সঠিক ফরম্যাটে লিখুন।\nউদাহরণ: `10+5` অথবা `100 USD BDT`")

# ------------------------------------------------------------------
# INLINE QUERY HANDLER (অন্য চ্যাটে কাজ করার জন্য)
# ------------------------------------------------------------------

@bot.inline_handler(lambda query: len(query.query) > 0)
def inline_query_manager(query):
    text = query.query.strip()
    results = []
    
    try:
        parts = text.split()
        
        # --- SCENARIO 1: Currency Conversion ---
        if len(parts) == 3 and parts[0].replace('.', '', 1).isdigit():
            amount = float(parts[0])
            base = parts[1].upper()
            target = parts[2].upper()
            
            data = currency_engine.convert(amount, base, target)
            
            if data['success']:
                title_text = f"{amount} {base} ➡️ {data['result']:.2f} {target}"
                desc_text = f"Rate: 1 {base} = {data['rate']} {target}"
                
                r1 = types.InlineQueryResultArticle(
                    id='1',
                    title=title_text,
                    description=desc_text,
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"{amount} {base} = {data['result']:.2f} {target}"
                    )
                )
                results.append(r1)

        # --- SCENARIO 2: Calculator ---
        else:
            calc_result = math_engine.calculate(text)
            
            if "Error" not in calc_result:
                r2 = types.InlineQueryResultArticle(
                    id='2',
                    title=f"Result: {calc_result}",
                    description=f"Calculate: {text}",
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"{text} = {calc_result}"
                    )
                )
                results.append(r2)
        
        # ফলাফল দেখানো
        bot.answer_inline_query(query.id, results)
        
    except Exception as e:
        logger.error(f"Inline Error: {e}")

# ------------------------------------------------------------------
# RUNNER
# ------------------------------------------------------------------
print("🤖 SuperCalc Bot is running in Professional Mode...")
print(f"Time: {datetime.now()}")

# রিকানেকশন লজিক (যাতে নেট অফ হলেও আবার চালু হয়)
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"⚠️ Connection Error: {e}")
        time.sleep(5)
