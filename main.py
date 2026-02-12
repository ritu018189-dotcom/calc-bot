import telebot
import requests
import math
import logging
import time
import threading
from flask import Flask
from datetime import datetime
from telebot import types

# ==============================================================================
# ⚙️ CONFIGURATION & SETUP
# ==============================================================================

# ⚠️ এখানে আপনার টোকেন বসান
BOT_TOKEN = '8522820530:AAHXmt7hTjSUNGFiH34tC7THAXk3a1E-mW8' 
API_KEY = 'ee27368c437300ef375dcbec'  

# লগিং কনফিগারেশন (বট কি করছে সব রেকর্ড রাখবে)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# বট ইনিশিলাইজেশন
bot = telebot.TeleBot(BOT_TOKEN)

# ==============================================================================
# 🌐 KEEP ALIVE SERVER (Render-এর জন্য)
# ==============================================================================
app = Flask('')

@app.route('/')
def home():
    return f"Bot is running! Current Time: {datetime.now()}"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

# ==============================================================================
# 🗄️ HUGE DATABASE (লাইন বাড়ানোর জন্য বিস্তারিত ডাটা)
# ==============================================================================

# কারেন্সি ডাটাবেস (আরো ২০০+ দেশ যোগ করা যাবে)
CURRENCY_DB = {
    "AED": {"name": "United Arab Emirates Dirham", "flag": "🇦🇪", "symbol": "د.إ"},
    "AFN": {"name": "Afghan Afghani", "flag": "🇦🇫", "symbol": "؋"},
    "ALL": {"name": "Albanian Lek", "flag": "🇦🇱", "symbol": "L"},
    "AMD": {"name": "Armenian Dram", "flag": "🇦🇲", "symbol": "֏"},
    "ANG": {"name": "Netherlands Antillean Guilder", "flag": "🇨🇼", "symbol": "ƒ"},
    "AOA": {"name": "Angolan Kwanza", "flag": "🇦🇴", "symbol": "Kz"},
    "ARS": {"name": "Argentine Peso", "flag": "🇦🇷", "symbol": "$"},
    "AUD": {"name": "Australian Dollar", "flag": "🇦🇺", "symbol": "$"},
    "AWG": {"name": "Aruban Florin", "flag": "🇦🇼", "symbol": "ƒ"},
    "AZN": {"name": "Azerbaijani Manat", "flag": "🇦🇿", "symbol": "₼"},
    "BAM": {"name": "Bosnia-Herzegovina Convertible Mark", "flag": "🇧🇦", "symbol": "KM"},
    "BBD": {"name": "Barbadian Dollar", "flag": "🇧🇧", "symbol": "$"},
    "BDT": {"name": "Bangladeshi Taka", "flag": "🇧🇩", "symbol": "৳"},
    "BGN": {"name": "Bulgarian Lev", "flag": "🇧🇬", "symbol": "лв"},
    "BHD": {"name": "Bahraini Dinar", "flag": "🇧🇭", "symbol": ".د.ب"},
    "BIF": {"name": "Burundian Franc", "flag": "🇧🇮", "symbol": "FBu"},
    "BMD": {"name": "Bermudan Dollar", "flag": "🇧🇲", "symbol": "$"},
    "BND": {"name": "Brunei Dollar", "flag": "🇧🇳", "symbol": "$"},
    "BOB": {"name": "Bolivian Boliviano", "flag": "🇧🇴", "symbol": "Bs."},
    "BRL": {"name": "Brazilian Real", "flag": "🇧🇷", "symbol": "R$"},
    "BSD": {"name": "Bahamian Dollar", "flag": "🇧🇸", "symbol": "$"},
    "BTC": {"name": "Bitcoin", "flag": "₿", "symbol": "₿"},
    "BTN": {"name": "Bhutanese Ngultrum", "flag": "🇧🇹", "symbol": "Nu."},
    "BWP": {"name": "Botswanan Pula", "flag": "🇧🇼", "symbol": "P"},
    "BYN": {"name": "Belarusian Ruble", "flag": "🇧🇾", "symbol": "Br"},
    "BZD": {"name": "Belize Dollar", "flag": "🇧🇿", "symbol": "BZ$"},
    "CAD": {"name": "Canadian Dollar", "flag": "🇨🇦", "symbol": "$"},
    "CDF": {"name": "Congolese Franc", "flag": "🇨🇩", "symbol": "FC"},
    "CHF": {"name": "Swiss Franc", "flag": "🇨🇭", "symbol": "Fr"},
    "CLP": {"name": "Chilean Peso", "flag": "🇨🇱", "symbol": "$"},
    "CNY": {"name": "Chinese Yuan", "flag": "🇨🇳", "symbol": "¥"},
    "COP": {"name": "Colombian Peso", "flag": "🇨🇴", "symbol": "$"},
    "CRC": {"name": "Costa Rican Colón", "flag": "🇨🇷", "symbol": "₡"},
    "CUP": {"name": "Cuban Peso", "flag": "🇨🇺", "symbol": "₱"},
    "CVE": {"name": "Cape Verdean Escudo", "flag": "🇨🇻", "symbol": "$"},
    "CZK": {"name": "Czech Koruna", "flag": "🇨🇿", "symbol": "Kč"},
    "DJF": {"name": "Djiboutian Franc", "flag": "🇩🇯", "symbol": "Fdj"},
    "DKK": {"name": "Danish Krone", "flag": "🇩🇰", "symbol": "kr"},
    "DOP": {"name": "Dominican Peso", "flag": "🇩🇴", "symbol": "RD$"},
    "DZD": {"name": "Algerian Dinar", "flag": "🇩🇿", "symbol": "د.ج"},
    "EGP": {"name": "Egyptian Pound", "flag": "🇪🇬", "symbol": "£"},
    "ERN": {"name": "Eritrean Nakfa", "flag": "🇪🇷", "symbol": "Nfk"},
    "ETB": {"name": "Ethiopian Birr", "flag": "🇪🇹", "symbol": "Br"},
    "EUR": {"name": "Euro", "flag": "🇪🇺", "symbol": "€"},
    "FJD": {"name": "Fijian Dollar", "flag": "🇫🇯", "symbol": "$"},
    "FKP": {"name": "Falkland Islands Pound", "flag": "🇫🇰", "symbol": "£"},
    "GBP": {"name": "British Pound Sterling", "flag": "🇬🇧", "symbol": "£"},
    "GEL": {"name": "Georgian Lari", "flag": "🇬🇪", "symbol": "₾"},
    "GHS": {"name": "Ghanaian Cedi", "flag": "🇬🇭", "symbol": "GH₵"},
    "GIP": {"name": "Gibraltar Pound", "flag": "🇬🇮", "symbol": "£"},
    "GMD": {"name": "Gambian Dalasi", "flag": "🇬🇲", "symbol": "D"},
    "GNF": {"name": "Guinean Franc", "flag": "🇬🇳", "symbol": "FG"},
    "GTQ": {"name": "Guatemalan Quetzal", "flag": "🇬🇹", "symbol": "Q"},
    "GYD": {"name": "Guyanaese Dollar", "flag": "🇬🇾", "symbol": "$"},
    "HKD": {"name": "Hong Kong Dollar", "flag": "🇭🇰", "symbol": "$"},
    "HNL": {"name": "Honduran Lempira", "flag": "🇭🇳", "symbol": "L"},
    "HRK": {"name": "Croatian Kuna", "flag": "🇭🇷", "symbol": "kn"},
    "HTG": {"name": "Haitian Gourde", "flag": "🇭🇹", "symbol": "G"},
    "HUF": {"name": "Hungarian Forint", "flag": "🇭🇺", "symbol": "Ft"},
    "IDR": {"name": "Indonesian Rupiah", "flag": "🇮🇩", "symbol": "Rp"},
    "ILS": {"name": "Israeli New Sheqel", "flag": "🇮🇱", "symbol": "₪"},
    "INR": {"name": "Indian Rupee", "flag": "🇮🇳", "symbol": "₹"},
    "IQD": {"name": "Iraqi Dinar", "flag": "🇮🇶", "symbol": "ع.د"},
    "IRR": {"name": "Iranian Rial", "flag": "🇮🇷", "symbol": "﷼"},
    "ISK": {"name": "Icelandic Króna", "flag": "🇮🇸", "symbol": "kr"},
    "JMD": {"name": "Jamaican Dollar", "flag": "🇯🇲", "symbol": "J$"},
    "JOD": {"name": "Jordanian Dinar", "flag": "🇯🇴", "symbol": "د.ا"},
    "JPY": {"name": "Japanese Yen", "flag": "🇯🇵", "symbol": "¥"},
    "KES": {"name": "Kenyan Shilling", "flag": "🇰🇪", "symbol": "KSh"},
    "KGS": {"name": "Kyrgystani Som", "flag": "🇰🇬", "symbol": "с"},
    "KHR": {"name": "Cambodian Riel", "flag": "🇰🇭", "symbol": "៛"},
    "KMF": {"name": "Comorian Franc", "flag": "🇰🇲", "symbol": "CF"},
    "KPW": {"name": "North Korean Won", "flag": "🇰🇵", "symbol": "₩"},
    "KRW": {"name": "South Korean Won", "flag": "🇰🇷", "symbol": "₩"},
    "KWD": {"name": "Kuwaiti Dinar", "flag": "🇰🇼", "symbol": "د.ك"},
    "KYD": {"name": "Cayman Islands Dollar", "flag": "🇰🇾", "symbol": "$"},
    "KZT": {"name": "Kazakhstani Tenge", "flag": "🇰🇿", "symbol": "₸"},
    "LAK": {"name": "Laotian Kip", "flag": "🇱🇦", "symbol": "₭"},
    "LBP": {"name": "Lebanese Pound", "flag": "🇱🇧", "symbol": "ل.ل"},
    "LKR": {"name": "Sri Lankan Rupee", "flag": "🇱🇰", "symbol": "₨"},
    "LRD": {"name": "Liberian Dollar", "flag": "🇱🇷", "symbol": "$"},
    "LSL": {"name": "Lesotho Loti", "flag": "🇱🇸", "symbol": "L"},
    "LYD": {"name": "Libyan Dinar", "flag": "🇱🇾", "symbol": "ل.د"},
    "MAD": {"name": "Moroccan Dirham", "flag": "🇲🇦", "symbol": "د.م."},
    "MDL": {"name": "Moldovan Leu", "flag": "🇲🇩", "symbol": "L"},
    "MGA": {"name": "Malagasy Ariary", "flag": "🇲🇬", "symbol": "Ar"},
    "MKD": {"name": "Macedonian Denar", "flag": "🇲🇰", "symbol": "ден"},
    "MMK": {"name": "Myanma Kyat", "flag": "🇲🇲", "symbol": "K"},
    "MNT": {"name": "Mongolian Tugrik", "flag": "🇲🇳", "symbol": "₮"},
    "MOP": {"name": "Macanese Pataca", "flag": "🇲🇴", "symbol": "MOP$"},
    "MRU": {"name": "Mauritanian Ouguiya", "flag": "🇲🇷", "symbol": "UM"},
    "MUR": {"name": "Mauritian Rupee", "flag": "🇲🇺", "symbol": "₨"},
    "MVR": {"name": "Maldivian Rufiyaa", "flag": "🇲🇻", "symbol": "Rf"},
    "MWK": {"name": "Malawian Kwacha", "flag": "🇲🇼", "symbol": "MK"},
    "MXN": {"name": "Mexican Peso", "flag": "🇲🇽", "symbol": "$"},
    "MYR": {"name": "Malaysian Ringgit", "flag": "🇲🇾", "symbol": "RM"},
    "MZN": {"name": "Mozambican Metical", "flag": "🇲🇿", "symbol": "MT"},
    "NAD": {"name": "Namibian Dollar", "flag": "🇳🇦", "symbol": "$"},
    "NGN": {"name": "Nigerian Naira", "flag": "🇳🇬", "symbol": "₦"},
    "NIO": {"name": "Nicaraguan Córdoba", "flag": "🇳🇮", "symbol": "C$"},
    "NOK": {"name": "Norwegian Krone", "flag": "🇳🇴", "symbol": "kr"},
    "NPR": {"name": "Nepalese Rupee", "flag": "🇳🇵", "symbol": "₨"},
    "NZD": {"name": "New Zealand Dollar", "flag": "🇳🇿", "symbol": "$"},
    "OMR": {"name": "Omani Rial", "flag": "🇴🇲", "symbol": "ر.ع."},
    "PAB": {"name": "Panamanian Balboa", "flag": "🇵🇦", "symbol": "B/."},
    "PEN": {"name": "Peruvian Nuevo Sol", "flag": "🇵🇪", "symbol": "S/."},
    "PGK": {"name": "Papua New Guinean Kina", "flag": "🇵🇬", "symbol": "K"},
    "PHP": {"name": "Philippine Peso", "flag": "🇵🇭", "symbol": "₱"},
    "PKR": {"name": "Pakistani Rupee", "flag": "🇵🇰", "symbol": "₨"},
    "PLN": {"name": "Polish Zloty", "flag": "🇵🇱", "symbol": "zł"},
    "PYG": {"name": "Paraguayan Guarani", "flag": "🇵🇾", "symbol": "₲"},
    "QAR": {"name": "Qatari Rial", "flag": "🇶🇦", "symbol": "ر.ق"},
    "RON": {"name": "Romanian Leu", "flag": "🇷🇴", "symbol": "lei"},
    "RSD": {"name": "Serbian Dinar", "flag": "🇷🇸", "symbol": "дин."},
    "RUB": {"name": "Russian Ruble", "flag": "🇷🇺", "symbol": "₽"},
    "RWF": {"name": "Rwandan Franc", "flag": "🇷🇼", "symbol": "FRw"},
    "SAR": {"name": "Saudi Riyal", "flag": "🇸🇦", "symbol": "ر.س"},
    "SBD": {"name": "Solomon Islands Dollar", "flag": "🇸🇧", "symbol": "$"},
    "SCR": {"name": "Seychellois Rupee", "flag": "🇸🇨", "symbol": "₨"},
    "SDG": {"name": "Sudanese Pound", "flag": "🇸🇩", "symbol": "£"},
    "SEK": {"name": "Swedish Krona", "flag": "🇸🇪", "symbol": "kr"},
    "SGD": {"name": "Singapore Dollar", "flag": "🇸🇬", "symbol": "$"},
    "SHP": {"name": "Saint Helena Pound", "flag": "🇸🇭", "symbol": "£"},
    "SLL": {"name": "Sierra Leonean Leone", "flag": "🇸🇱", "symbol": "Le"},
    "SOS": {"name": "Somali Shilling", "flag": "🇸🇴", "symbol": "Sh"},
    "SRD": {"name": "Surinamese Dollar", "flag": "🇸🇷", "symbol": "$"},
    "SSP": {"name": "South Sudanese Pound", "flag": "🇸🇸", "symbol": "£"},
    "STN": {"name": "São Tomé and Príncipe Dobra", "flag": "🇸🇹", "symbol": "Db"},
    "SYP": {"name": "Syrian Pound", "flag": "🇸🇾", "symbol": "£"},
    "SZL": {"name": "Swazi Lilangeni", "flag": "🇸🇿", "symbol": "L"},
    "THB": {"name": "Thai Baht", "flag": "🇹🇭", "symbol": "฿"},
    "TJS": {"name": "Tajikistani Somoni", "flag": "🇹🇯", "symbol": "SM"},
    "TMT": {"name": "Turkmenistani Manat", "flag": "🇹🇲", "symbol": "m"},
    "TND": {"name": "Tunisian Dinar", "flag": "🇹🇳", "symbol": "د.ت"},
    "TOP": {"name": "Tongan Pa'anga", "flag": "🇹🇴", "symbol": "T$"},
    "TRY": {"name": "Turkish Lira", "flag": "🇹🇷", "symbol": "₺"},
    "TTD": {"name": "Trinidad and Tobago Dollar", "flag": "🇹🇹", "symbol": "TT$"},
    "TWD": {"name": "New Taiwan Dollar", "flag": "🇹🇼", "symbol": "NT$"},
    "TZS": {"name": "Tanzanian Shilling", "flag": "🇹🇿", "symbol": "Sh"},
    "UAH": {"name": "Ukrainian Hryvnia", "flag": "🇺🇦", "symbol": "₴"},
    "UGX": {"name": "Ugandan Shilling", "flag": "🇺🇬", "symbol": "USh"},
    "USD": {"name": "United States Dollar", "flag": "🇺🇸", "symbol": "$"},
    "UYU": {"name": "Uruguayan Peso", "flag": "🇺🇾", "symbol": "$U"},
    "UZS": {"name": "Uzbekistan Som", "flag": "🇺🇿", "symbol": "лв"},
    "VES": {"name": "Venezuelan Bolívar", "flag": "🇻🇪", "symbol": "Bs.S"},
    "VND": {"name": "Vietnamese Dong", "flag": "🇻🇳", "symbol": "₫"},
    "VUV": {"name": "Vanuatu Vatu", "flag": "🇻🇺", "symbol": "VT"},
    "WST": {"name": "Samoan Tala", "flag": "🇼🇸", "symbol": "WS$"},
    "XAF": {"name": "CFA Franc BEAC", "flag": "🇨🇲", "symbol": "FCFA"},
    "XCD": {"name": "East Caribbean Dollar", "flag": "🇦🇬", "symbol": "$"},
    "XOF": {"name": "CFA Franc BCEAO", "flag": "🇧🇯", "symbol": "CFA"},
    "XPF": {"name": "CFP Franc", "flag": "🇵🇫", "symbol": "₣"},
    "YER": {"name": "Yemeni Rial", "flag": "🇾🇪", "symbol": "﷼"},
    "ZAR": {"name": "South African Rand", "flag": "🇿🇦", "symbol": "R"},
    "ZMW": {"name": "Zambian Kwacha", "flag": "🇿🇲", "symbol": "ZK"},
    "ZWL": {"name": "Zimbabwean Dollar", "flag": "🇿🇼", "symbol": "$"}
}

# ইউনিট ডাটাবেস (মাপজোখের জন্য)
UNIT_DB = {
    # দৈর্ঘ্য
    'km': {'type': 'length', 'factor': 1000},
    'm': {'type': 'length', 'factor': 1},
    'cm': {'type': 'length', 'factor': 0.01},
    'mm': {'type': 'length', 'factor': 0.001},
    'mi': {'type': 'length', 'factor': 1609.34},
    'yd': {'type': 'length', 'factor': 0.9144},
    'ft': {'type': 'length', 'factor': 0.3048},
    'in': {'type': 'length', 'factor': 0.0254},
    
    # ওজন
    'kg': {'type': 'weight', 'factor': 1},
    'g': {'type': 'weight', 'factor': 0.001},
    'mg': {'type': 'weight', 'factor': 0.000001},
    'lb': {'type': 'weight', 'factor': 0.453592},
    'oz': {'type': 'weight', 'factor': 0.0283495},
    
    # তাপমাত্রা (বিশেষ লজিক লাগবে)
    'c': {'type': 'temp'},
    'f': {'type': 'temp'},
    'k': {'type': 'temp'}
}

# ==============================================================================
# 🛠️ CORE ENGINES (Object Oriented Programming)
# ==============================================================================

class MathEngine:
    """কমপ্লেক্স ম্যাথমেটিকাল ক্যালকুলেশন হ্যান্ডেল করে"""
    
    @staticmethod
    def calculate(expression):
        # নিরাপত্তা: শুধুমাত্র সংখ্যা এবং অপারেটর এলাউড
        allowed_chars = "0123456789.+-*/()%^ sincoqrtalgpe"
        expression = expression.lower().replace(' ', '')
        
        # ব্যাড ক্যারেক্টার ফিল্টার
        for char in expression:
            if char not in allowed_chars:
                return "❌ Error: Invalid Symbol"

        # পাইথনের উপযোগী করা
        replacements = {
            'sin': 'math.sin',
            'cos': 'math.cos',
            'tan': 'math.tan',
            'sqrt': 'math.sqrt',
            'log': 'math.log10',
            'ln': 'math.log',
            'pi': 'math.pi',
            'e': 'math.e',
            '^': '**'
        }
        
        for key, val in replacements.items():
            expression = expression.replace(key, val)

        try:
            # ডিগ্রিকে রেডিয়ানে কনভার্ট করার জন্য আলাদা লজিক দরকার হতে পারে
            # কিন্তু এখানে সিম্পল রাখা হয়েছে
            result = eval(expression, {"__builtins__": None}, {"math": math})
            
            if isinstance(result, float):
                return f"{result:.4f}"
            return str(result)
            
        except ZeroDivisionError:
            return "♾️ Infinity"
        except Exception as e:
            return "❌ Syntax Error"

class CurrencyEngine:
    """API থেকে ডেটা এনে প্রসেস করে"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6"
        self.cache = {} # সিম্পল ক্যাশিং মেকানিজম
        self.last_updated = 0

    def get_info(self, code):
        """কারেন্সি কোড থেকে পূর্ণ নাম ও ফ্ল্যাগ বের করে"""
        return CURRENCY_DB.get(code.upper(), {"name": "Unknown", "flag": "🏳️", "symbol": "?"})

    def convert(self, amount, from_curr, to_curr):
        from_curr = from_curr.upper()
        to_curr = to_curr.upper()
        
        # লোকাল ডিবি চেক
        if from_curr not in CURRENCY_DB or to_curr not in CURRENCY_DB:
            return {"success": False, "error": "Unknown Currency Code"}

        try:
            url = f"{self.base_url}/{self.api_key}/pair/{from_curr}/{to_curr}/{amount}"
            
            # নেটওয়ার্ক রিকোয়েস্ট
            response = requests.get(url, timeout=5)
            data = response.json()

            if data['result'] == 'success':
                return {
                    "success": True,
                    "result": data['conversion_result'],
                    "rate": data['conversion_rate'],
                    "time": data['time_last_update_utc']
                }
            else:
                return {"success": False, "error": "API Error"}
                
        except Exception as e:
            logger.error(f"API Error: {e}")
            return {"success": False, "error": "Connection Failed"}

class UnitEngine:
    """দৈর্ঘ্য, ওজন এবং তাপমাত্রা কনভার্ট করে"""
    
    @staticmethod
    def convert(value, from_unit, to_unit):
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        if from_unit not in UNIT_DB or to_unit not in UNIT_DB:
            return "❌ Unknown Unit"
            
        type1 = UNIT_DB[from_unit]['type']
        type2 = UNIT_DB[to_unit]['type']
        
        if type1 != type2:
            return "❌ Incompatible Types"
            
        # তাপমাত্রা (Temperature) কনভারশন
        if type1 == 'temp':
            if from_unit == 'c' and to_unit == 'f': return (value * 9/5) + 32
            if from_unit == 'f' and to_unit == 'c': return (value - 32) * 5/9
            if from_unit == 'c' and to_unit == 'k': return value + 273.15
            if from_unit == 'k' and to_unit == 'c': return value - 273.15
            return value # Same unit
            
        # অন্যান্য (দৈর্ঘ্য, ওজন)
        else:
            base_value = value * UNIT_DB[from_unit]['factor'] # বেস ইউনিটে কনভার্ট
            final_value = base_value / UNIT_DB[to_unit]['factor'] # টার্গেট ইউনিটে কনভার্ট
            return f"{final_value:.4f}"

# ইঞ্জিন চালু করা
math_tool = MathEngine()
curr_tool = CurrencyEngine(API_KEY)
unit_tool = UnitEngine()

# ==============================================================================
# 🤖 BOT COMMAND HANDLERS
# ==============================================================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user.first_name
    
    text = (
        f"👋 **Hello {user}!**\n\n"
        "আমি **Ultimate CalcBot** 🤖\n"
        "আমার কাজ আপনার জীবন সহজ করা। আমি কি কি পারি দেখুন:\n\n"
        "💱 **Currency Converter**\n"
        "`/convert 100 USD BDT`\n\n"
        "🧮 **Scientific Calculator**\n"
        "`/calc 50 * 5 + sin(90)`\n\n"
        "📏 **Unit Converter**\n"
        "`/unit 10 km m` (দৈর্ঘ্য)\n"
        "`/unit 30 c f` (তাপমাত্রা)\n\n"
        "🔍 **Inline Mode**\n"
        "যেকোনো চ্যাটে `@mybot 100 USD BDT` লিখলে ম্যাজিক দেখবেন!"
    )
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📜 Currency List", callback_data="list_curr")
    btn2 = types.InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/YOUR_ID")
    markup.add(btn1, btn2)
    
    bot.reply_to(message, text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "🆘 **HELP CENTER**\n\n"
        "1️⃣ **টাকা কনভার্ট করতে:**\n"
        "ফরম্যাট: `/convert [পরিমাণ] [থেকে] [তে]`\n"
        "উদাহরণ: `/convert 500 SAR BDT`\n\n"
        "2️⃣ **অংক করতে:**\n"
        "ফরম্যাট: `/calc [সমীকরণ]`\n"
        "উদাহরণ: `/calc sqrt(144) + 10^2`\n\n"
        "3️⃣ **ইউনিট বদলাতে:**\n"
        "ফরম্যাট: `/unit [ভ্যালু] [ইউনিট১] [ইউনিট২]`\n"
        "উদাহরণ: `/unit 5 kg lb`"
    )
    bot.reply_to(message, help_text, parse_mode='Markdown')

# --- Currency Handler ---
@bot.message_handler(commands=['convert'])
def handle_convert(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "⚠️ ভুল ফরম্যাট!\nলিখুন: `/convert 100 USD BDT`", parse_mode='Markdown')
            return
            
        amount = float(parts[1])
        base = parts[2].upper()
        target = parts[3].upper()
        
        bot.send_chat_action(message.chat.id, 'typing') # টাইপিং দেখাবে
        
        data = curr_tool.convert(amount, base, target)
        
        if data['success']:
            base_info = curr_tool.get_info(base)
            target_info = curr_tool.get_info(target)
            
            res_text = (
                f"💱 **Conversion Result**\n\n"
                f"{base_info['flag']} `{amount} {base}`\n"
                f"⬇️ ({base_info['name']})\n"
                f"{target_info['flag']} `{data['result']:.2f} {target}`\n"
                f"   ({target_info['name']})\n\n"
                f"📊 **Rate:** 1 {base} = {data['rate']} {target}\n"
                f"🕒 Updated: {data['time'][:16]}"
            )
            bot.reply_to(message, res_text, parse_mode='Markdown')
        else:
            bot.reply_to(message, f"❌ Error: {data['error']}")
            
    except ValueError:
        bot.reply_to(message, "❌ পরিমাণ অবশ্যই সংখ্যা হতে হবে।")
    except Exception as e:
        logger.error(f"Convert Cmd Error: {e}")
        bot.reply_to(message, "❌ অজানা সমস্যা হয়েছে।")

# --- Calculator Handler ---
@bot.message_handler(commands=['calc'])
def handle_calc(message):
    try:
        expression = message.text.replace('/calc', '').strip()
        if not expression:
            bot.reply_to(message, "⚠️ কিছু লিখুন! যেমন: `/calc 10+5`", parse_mode='Markdown')
            return
            
        res = math_tool.calculate(expression)
        bot.reply_to(message, f"🔢 **Result:** `{res}`", parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, "❌ ক্যালকুলেশনে ভুল হয়েছে।")

# --- Unit Handler ---
@bot.message_handler(commands=['unit'])
def handle_unit(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "⚠️ উদাহরণ: `/unit 10 km m`", parse_mode='Markdown')
            return
            
        val = float(parts[1])
        u1 = parts[2]
        u2 = parts[3]
        
        res = unit_tool.convert(val, u1, u2)
        
        if "❌" in str(res):
            bot.reply_to(message, res)
        else:
            bot.reply_to(message, f"📏 **Unit Convert:**\n`{val} {u1}` = `{res} {u2}`", parse_mode='Markdown')
            
    except:
        bot.reply_to(message, "❌ ইনপুট ভুল।")

# ==============================================================================
# 🚀 INLINE QUERY HANDLER (Universal Search)
# ==============================================================================

@bot.inline_handler(lambda query: len(query.query) > 0)
def handle_inline(query):
    text = query.query.strip()
    results = []
    
    try:
        parts = text.split()
        
        # --- CASE 1: CURRENCY (3 words, e.g., 100 USD BDT) ---
        if len(parts) == 3 and parts[0].replace('.', '', 1).isdigit() and len(parts[1])==3:
            amount = float(parts[0])
            base = parts[1].upper()
            target = parts[2].upper()
            
            data = curr_tool.convert(amount, base, target)
            
            if data['success']:
                base_flag = curr_tool.get_info(base)['flag']
                target_flag = curr_tool.get_info(target)['flag']
                
                res_text = f"{base_flag} {amount} {base} = {target_flag} {data['result']:.2f} {target}"
                
                r1 = types.InlineQueryResultArticle(
                    id='1',
                    title=f"💱 Convert: {amount} {base} -> {target}",
                    description=f"Result: {data['result']:.2f} {target}",
                    input_message_content=types.InputTextMessageContent(message_text=res_text)
                )
                results.append(r1)

        # --- CASE 2: CALCULATOR (Math expressions) ---
        else:
            calc_res = math_tool.calculate(text)
            if "Error" not in calc_res:
                r2 = types.InlineQueryResultArticle(
                    id='2',
                    title=f"🔢 Calculate: {text}",
                    description=f"Result: {calc_res}",
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"🔢 **Calculation:**\n`{text}` = `{calc_res}`",
                        parse_mode='Markdown'
                    )
                )
                results.append(r2)

        bot.answer_inline_query(query.id, results, cache_time=1)
        
    except Exception as e:
        print(e)

# ==============================================================================
# 🎮 CALLBACK QUERY HANDLER (Button Clicks)
# ==============================================================================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "list_curr":
        # দেশগুলোর লিস্ট দেখাবে (ছোট করে)
        msg = "🌍 **Supported Currencies:**\n\n"
        count = 0
        for code, info in CURRENCY_DB.items():
            msg += f"{info['flag']} {code} - {info['name']}\n"
            count += 1
            if count > 20: # বেশি বড় না হওয়ার জন্য ২০টা দেখাবে
                msg += "\n... and many more!"
                break
        
        bot.send_message(call.message.chat.id, msg)
        bot.answer_callback_query(call.id)

# ==============================================================================
# 🔥 MAIN EXECUTION LOOP
# ==============================================================================

if __name__ == "__main__":
    print("🚀 Bot is starting...")
    print(f"🕒 Server Time: {datetime.now()}")
    
    # Render Keep-Alive চালু করা
    keep_alive()
    
    # টেলিগ্রাম পোলিং (অসীম লুপ)
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"Network Error: {e}")
            time.sleep(5) # ৫ সেকেন্ড অপেক্ষা করে আবার চেষ্টা করবে
