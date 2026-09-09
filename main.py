import os
import telebot
import yfinance as yf
import requests
import math
import logging
import time
import threading
import json
from datetime import datetime
import pytz
from flask import Flask
from telebot import types

BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is not set. "
        "Set it before starting the bot, e.g.: export BOT_TOKEN='your-token-here'"
    )

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("calc_bot")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='Markdown')

app = Flask(__name__)

@app.route('/')
def index():
    status = {
        "status": "online",
        "server_time": str(datetime.now()),
        "service": "Telegram Bot API",
        "load": "Normal"
    }
    return json.dumps(status, indent=4)

def run_server():
    app.run(host='0.0.0.0', port=8080)

def start_keep_alive():
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()

CURRENCY_DB = {
    "AED": {
        "name": "United Arab Emirates Dirham",
        "code": "AED",
        "symbol": "د.إ",
        "country": "United Arab Emirates",
        "flag": "🇦🇪",
        "type": "Fiat"
    },
    "AFN": {
        "name": "Afghan Afghani",
        "code": "AFN",
        "symbol": "؋",
        "country": "Afghanistan",
        "flag": "🇦🇫",
        "type": "Fiat"
    },
    "ALL": {
        "name": "Albanian Lek",
        "code": "ALL",
        "symbol": "L",
        "country": "Albania",
        "flag": "🇦🇱",
        "type": "Fiat"
    },
    "AMD": {
        "name": "Armenian Dram",
        "code": "AMD",
        "symbol": "֏",
        "country": "Armenia",
        "flag": "🇦🇲",
        "type": "Fiat"
    },
    "ANG": {
        "name": "Netherlands Antillean Guilder",
        "code": "ANG",
        "symbol": "ƒ",
        "country": "Curaçao",
        "flag": "🇨🇼",
        "type": "Fiat"
    },
    "AOA": {
        "name": "Angolan Kwanza",
        "code": "AOA",
        "symbol": "Kz",
        "country": "Angola",
        "flag": "🇦🇴",
        "type": "Fiat"
    },
    "ARS": {
        "name": "Argentine Peso",
        "code": "ARS",
        "symbol": "$",
        "country": "Argentina",
        "flag": "🇦🇷",
        "type": "Fiat"
    },
    "AUD": {
        "name": "Australian Dollar",
        "code": "AUD",
        "symbol": "$",
        "country": "Australia",
        "flag": "🇦🇺",
        "type": "Fiat"
    },
    "AWG": {
        "name": "Aruban Florin",
        "code": "AWG",
        "symbol": "ƒ",
        "country": "Aruba",
        "flag": "🇦🇼",
        "type": "Fiat"
    },
    "AZN": {
        "name": "Azerbaijani Manat",
        "code": "AZN",
        "symbol": "₼",
        "country": "Azerbaijan",
        "flag": "🇦🇿",
        "type": "Fiat"
    },
    "BAM": {
        "name": "Bosnia-Herzegovina Mark",
        "code": "BAM",
        "symbol": "KM",
        "country": "Bosnia and Herzegovina",
        "flag": "🇧🇦",
        "type": "Fiat"
    },
    "BBD": {
        "name": "Barbadian Dollar",
        "code": "BBD",
        "symbol": "$",
        "country": "Barbados",
        "flag": "🇧🇧",
        "type": "Fiat"
    },
    "BDT": {
        "name": "Bangladeshi Taka",
        "code": "BDT",
        "symbol": "৳",
        "country": "Bangladesh",
        "flag": "🇧🇩",
        "type": "Fiat"
    },
    "BGN": {
        "name": "Bulgarian Lev",
        "code": "BGN",
        "symbol": "лв",
        "country": "Bulgaria",
        "flag": "🇧🇬",
        "type": "Fiat"
    },
    "BHD": {
        "name": "Bahraini Dinar",
        "code": "BHD",
        "symbol": ".د.ب",
        "country": "Bahrain",
        "flag": "🇧🇭",
        "type": "Fiat"
    },
    "BIF": {
        "name": "Burundian Franc",
        "code": "BIF",
        "symbol": "FBu",
        "country": "Burundi",
        "flag": "🇧🇮",
        "type": "Fiat"
    },
    "BMD": {
        "name": "Bermudan Dollar",
        "code": "BMD",
        "symbol": "$",
        "country": "Bermuda",
        "flag": "🇧🇲",
        "type": "Fiat"
    },
    "BND": {
        "name": "Brunei Dollar",
        "code": "BND",
        "symbol": "$",
        "country": "Brunei",
        "flag": "🇧🇳",
        "type": "Fiat"
    },
    "BOB": {
        "name": "Bolivian Boliviano",
        "code": "BOB",
        "symbol": "Bs.",
        "country": "Bolivia",
        "flag": "🇧🇴",
        "type": "Fiat"
    },
    "BRL": {
        "name": "Brazilian Real",
        "code": "BRL",
        "symbol": "R$",
        "country": "Brazil",
        "flag": "🇧🇷",
        "type": "Fiat"
    },
    "BSD": {
        "name": "Bahamian Dollar",
        "code": "BSD",
        "symbol": "$",
        "country": "Bahamas",
        "flag": "🇧🇸",
        "type": "Fiat"
    },
    "BTC": {
        "name": "Bitcoin",
        "code": "BTC",
        "symbol": "₿",
        "country": "Global",
        "flag": "🌐",
        "type": "Crypto"
    },
    "BTN": {
        "name": "Bhutanese Ngultrum",
        "code": "BTN",
        "symbol": "Nu.",
        "country": "Bhutan",
        "flag": "🇧🇹",
        "type": "Fiat"
    },
    "BWP": {
        "name": "Botswanan Pula",
        "code": "BWP",
        "symbol": "P",
        "country": "Botswana",
        "flag": "🇧🇼",
        "type": "Fiat"
    },
    "BYN": {
        "name": "Belarusian Ruble",
        "code": "BYN",
        "symbol": "Br",
        "country": "Belarus",
        "flag": "🇧🇾",
        "type": "Fiat"
    },
    "BZD": {
        "name": "Belize Dollar",
        "code": "BZD",
        "symbol": "BZ$",
        "country": "Belize",
        "flag": "🇧🇿",
        "type": "Fiat"
    },
    "CAD": {
        "name": "Canadian Dollar",
        "code": "CAD",
        "symbol": "$",
        "country": "Canada",
        "flag": "🇨🇦",
        "type": "Fiat"
    },
    "CDF": {
        "name": "Congolese Franc",
        "code": "CDF",
        "symbol": "FC",
        "country": "DR Congo",
        "flag": "🇨🇩",
        "type": "Fiat"
    },
    "CHF": {
        "name": "Swiss Franc",
        "code": "CHF",
        "symbol": "Fr",
        "country": "Switzerland",
        "flag": "🇨🇭",
        "type": "Fiat"
    },
    "CLP": {
        "name": "Chilean Peso",
        "code": "CLP",
        "symbol": "$",
        "country": "Chile",
        "flag": "🇨🇱",
        "type": "Fiat"
    },
    "CNY": {
        "name": "Chinese Yuan",
        "code": "CNY",
        "symbol": "¥",
        "country": "China",
        "flag": "🇨🇳",
        "type": "Fiat"
    },
    "COP": {
        "name": "Colombian Peso",
        "code": "COP",
        "symbol": "$",
        "country": "Colombia",
        "flag": "🇨🇴",
        "type": "Fiat"
    },
    "CRC": {
        "name": "Costa Rican Colón",
        "code": "CRC",
        "symbol": "₡",
        "country": "Costa Rica",
        "flag": "🇨🇷",
        "type": "Fiat"
    },
    "CUP": {
        "name": "Cuban Peso",
        "code": "CUP",
        "symbol": "₱",
        "country": "Cuba",
        "flag": "🇨🇺",
        "type": "Fiat"
    },
    "CVE": {
        "name": "Cape Verdean Escudo",
        "code": "CVE",
        "symbol": "$",
        "country": "Cape Verde",
        "flag": "🇨🇻",
        "type": "Fiat"
    },
    "CZK": {
        "name": "Czech Republic Koruna",
        "code": "CZK",
        "symbol": "Kč",
        "country": "Czech Republic",
        "flag": "🇨🇿",
        "type": "Fiat"
    },
    "DJF": {
        "name": "Djiboutian Franc",
        "code": "DJF",
        "symbol": "Fdj",
        "country": "Djibouti",
        "flag": "🇩🇯",
        "type": "Fiat"
    },
    "DKK": {
        "name": "Danish Krone",
        "code": "DKK",
        "symbol": "kr",
        "country": "Denmark",
        "flag": "🇩🇰",
        "type": "Fiat"
    },
    "DOP": {
        "name": "Dominican Peso",
        "code": "DOP",
        "symbol": "RD$",
        "country": "Dominican Republic",
        "flag": "🇩🇴",
        "type": "Fiat"
    },
    "DZD": {
        "name": "Algerian Dinar",
        "code": "DZD",
        "symbol": "د.ج",
        "country": "Algeria",
        "flag": "🇩🇿",
        "type": "Fiat"
    },
    "EGP": {
        "name": "Egyptian Pound",
        "code": "EGP",
        "symbol": "£",
        "country": "Egypt",
        "flag": "🇪🇬",
        "type": "Fiat"
    },
    "ERN": {
        "name": "Eritrean Nakfa",
        "code": "ERN",
        "symbol": "Nfk",
        "country": "Eritrea",
        "flag": "🇪🇷",
        "type": "Fiat"
    },
    "ETB": {
        "name": "Ethiopian Birr",
        "code": "ETB",
        "symbol": "Br",
        "country": "Ethiopia",
        "flag": "🇪🇹",
        "type": "Fiat"
    },
    "EUR": {
        "name": "Euro",
        "code": "EUR",
        "symbol": "€",
        "country": "European Union",
        "flag": "🇪🇺",
        "type": "Fiat"
    },
    "ETH": {
        "name": "Ethereum",
        "code": "ETH",
        "symbol": "Ξ",
        "country": "Global",
        "flag": "💎",
        "type": "Crypto"
    },
    "FJD": {
        "name": "Fijian Dollar",
        "code": "FJD",
        "symbol": "$",
        "country": "Fiji",
        "flag": "🇫🇯",
        "type": "Fiat"
    },
    "FKP": {
        "name": "Falkland Islands Pound",
        "code": "FKP",
        "symbol": "£",
        "country": "Falkland Islands",
        "flag": "🇫🇰",
        "type": "Fiat"
    },
    "GBP": {
        "name": "British Pound Sterling",
        "code": "GBP",
        "symbol": "£",
        "country": "United Kingdom",
        "flag": "🇬🇧",
        "type": "Fiat"
    },
    "GEL": {
        "name": "Georgian Lari",
        "code": "GEL",
        "symbol": "₾",
        "country": "Georgia",
        "flag": "🇬🇪",
        "type": "Fiat"
    },
    "GHS": {
        "name": "Ghanaian Cedi",
        "code": "GHS",
        "symbol": "GH₵",
        "country": "Ghana",
        "flag": "🇬🇭",
        "type": "Fiat"
    },
    "GIP": {
        "name": "Gibraltar Pound",
        "code": "GIP",
        "symbol": "£",
        "country": "Gibraltar",
        "flag": "🇬🇮",
        "type": "Fiat"
    },
    "GMD": {
        "name": "Gambian Dalasi",
        "code": "GMD",
        "symbol": "D",
        "country": "Gambia",
        "flag": "🇬🇲",
        "type": "Fiat"
    },
    "GNF": {
        "name": "Guinean Franc",
        "code": "GNF",
        "symbol": "FG",
        "country": "Guinea",
        "flag": "🇬🇳",
        "type": "Fiat"
    },
    "GTQ": {
        "name": "Guatemalan Quetzal",
        "code": "GTQ",
        "symbol": "Q",
        "country": "Guatemala",
        "flag": "🇬🇹",
        "type": "Fiat"
    },
    "GYD": {
        "name": "Guyanaese Dollar",
        "code": "GYD",
        "symbol": "$",
        "country": "Guyana",
        "flag": "🇬🇾",
        "type": "Fiat"
    },
    "HKD": {
        "name": "Hong Kong Dollar",
        "code": "HKD",
        "symbol": "$",
        "country": "Hong Kong",
        "flag": "🇭🇰",
        "type": "Fiat"
    },
    "HNL": {
        "name": "Honduran Lempira",
        "code": "HNL",
        "symbol": "L",
        "country": "Honduras",
        "flag": "🇭🇳",
        "type": "Fiat"
    },
    "HRK": {
        "name": "Croatian Kuna",
        "code": "HRK",
        "symbol": "kn",
        "country": "Croatia",
        "flag": "🇭🇷",
        "type": "Fiat"
    },
    "HTG": {
        "name": "Haitian Gourde",
        "code": "HTG",
        "symbol": "G",
        "country": "Haiti",
        "flag": "🇭🇹",
        "type": "Fiat"
    },
    "HUF": {
        "name": "Hungarian Forint",
        "code": "HUF",
        "symbol": "Ft",
        "country": "Hungary",
        "flag": "🇭🇺",
        "type": "Fiat"
    },
    "IDR": {
        "name": "Indonesian Rupiah",
        "code": "IDR",
        "symbol": "Rp",
        "country": "Indonesia",
        "flag": "🇮🇩",
        "type": "Fiat"
    },
    "ILS": {
        "name": "Israeli New Sheqel",
        "code": "ILS",
        "symbol": "₪",
        "country": "Israel",
        "flag": "🇮🇱",
        "type": "Fiat"
    },
    "INR": {
        "name": "Indian Rupee",
        "code": "INR",
        "symbol": "₹",
        "country": "India",
        "flag": "🇮🇳",
        "type": "Fiat"
    },
    "IQD": {
        "name": "Iraqi Dinar",
        "code": "IQD",
        "symbol": "ع.د",
        "country": "Iraq",
        "flag": "🇮🇶",
        "type": "Fiat"
    },
    "IRR": {
        "name": "Iranian Rial",
        "code": "IRR",
        "symbol": "﷼",
        "country": "Iran",
        "flag": "🇮🇷",
        "type": "Fiat"
    },
    "ISK": {
        "name": "Icelandic Króna",
        "code": "ISK",
        "symbol": "kr",
        "country": "Iceland",
        "flag": "🇮🇸",
        "type": "Fiat"
    },
    "JMD": {
        "name": "Jamaican Dollar",
        "code": "JMD",
        "symbol": "J$",
        "country": "Jamaica",
        "flag": "🇯🇲",
        "type": "Fiat"
    },
    "JOD": {
        "name": "Jordanian Dinar",
        "code": "JOD",
        "symbol": "د.ا",
        "country": "Jordan",
        "flag": "🇯🇴",
        "type": "Fiat"
    },
    "JPY": {
        "name": "Japanese Yen",
        "code": "JPY",
        "symbol": "¥",
        "country": "Japan",
        "flag": "🇯🇵",
        "type": "Fiat"
    },
    "KES": {
        "name": "Kenyan Shilling",
        "code": "KES",
        "symbol": "KSh",
        "country": "Kenya",
        "flag": "🇰🇪",
        "type": "Fiat"
    },
    "KGS": {
        "name": "Kyrgystani Som",
        "code": "KGS",
        "symbol": "с",
        "country": "Kyrgyzstan",
        "flag": "🇰🇬",
        "type": "Fiat"
    },
    "KHR": {
        "name": "Cambodian Riel",
        "code": "KHR",
        "symbol": "៛",
        "country": "Cambodia",
        "flag": "🇰🇭",
        "type": "Fiat"
    },
    "KMF": {
        "name": "Comorian Franc",
        "code": "KMF",
        "symbol": "CF",
        "country": "Comoros",
        "flag": "🇰🇲",
        "type": "Fiat"
    },
    "KPW": {
        "name": "North Korean Won",
        "code": "KPW",
        "symbol": "₩",
        "country": "North Korea",
        "flag": "🇰🇵",
        "type": "Fiat"
    },
    "KRW": {
        "name": "South Korean Won",
        "code": "KRW",
        "symbol": "₩",
        "country": "South Korea",
        "flag": "🇰🇷",
        "type": "Fiat"
    },
    "KWD": {
        "name": "Kuwaiti Dinar",
        "code": "KWD",
        "symbol": "د.ك",
        "country": "Kuwait",
        "flag": "🇰🇼",
        "type": "Fiat"
    },
    "KYD": {
        "name": "Cayman Islands Dollar",
        "code": "KYD",
        "symbol": "$",
        "country": "Cayman Islands",
        "flag": "🇰🇾",
        "type": "Fiat"
    },
    "KZT": {
        "name": "Kazakhstani Tenge",
        "code": "KZT",
        "symbol": "₸",
        "country": "Kazakhstan",
        "flag": "🇰🇿",
        "type": "Fiat"
    },
    "LAK": {
        "name": "Laotian Kip",
        "code": "LAK",
        "symbol": "₭",
        "country": "Laos",
        "flag": "🇱🇦",
        "type": "Fiat"
    },
    "LBP": {
        "name": "Lebanese Pound",
        "code": "LBP",
        "symbol": "ل.ل",
        "country": "Lebanon",
        "flag": "🇱🇧",
        "type": "Fiat"
    },
    "LKR": {
        "name": "Sri Lankan Rupee",
        "code": "LKR",
        "symbol": "₨",
        "country": "Sri Lanka",
        "flag": "🇱🇰",
        "type": "Fiat"
    },
    "LRD": {
        "name": "Liberian Dollar",
        "code": "LRD",
        "symbol": "$",
        "country": "Liberia",
        "flag": "🇱🇷",
        "type": "Fiat"
    },
    "LSL": {
        "name": "Lesotho Loti",
        "code": "LSL",
        "symbol": "L",
        "country": "Lesotho",
        "flag": "🇱🇸",
        "type": "Fiat"
    },
    "LYD": {
        "name": "Libyan Dinar",
        "code": "LYD",
        "symbol": "ل.د",
        "country": "Libya",
        "flag": "🇱🇾",
        "type": "Fiat"
    },
    "MAD": {
        "name": "Moroccan Dirham",
        "code": "MAD",
        "symbol": "د.م.",
        "country": "Morocco",
        "flag": "🇲🇦",
        "type": "Fiat"
    },
    "MDL": {
        "name": "Moldovan Leu",
        "code": "MDL",
        "symbol": "L",
        "country": "Moldova",
        "flag": "🇲🇩",
        "type": "Fiat"
    },
    "MGA": {
        "name": "Malagasy Ariary",
        "code": "MGA",
        "symbol": "Ar",
        "country": "Madagascar",
        "flag": "🇲🇬",
        "type": "Fiat"
    },
    "MKD": {
        "name": "Macedonian Denar",
        "code": "MKD",
        "symbol": "ден",
        "country": "North Macedonia",
        "flag": "🇲🇰",
        "type": "Fiat"
    },
    "MMK": {
        "name": "Myanma Kyat",
        "code": "MMK",
        "symbol": "K",
        "country": "Myanmar",
        "flag": "🇲🇲",
        "type": "Fiat"
    },
    "MNT": {
        "name": "Mongolian Tugrik",
        "code": "MNT",
        "symbol": "₮",
        "country": "Mongolia",
        "flag": "🇲🇳",
        "type": "Fiat"
    },
    "MOP": {
        "name": "Macanese Pataca",
        "code": "MOP",
        "symbol": "MOP$",
        "country": "Macau",
        "flag": "🇲🇴",
        "type": "Fiat"
    },
    "MRU": {
        "name": "Mauritanian Ouguiya",
        "code": "MRU",
        "symbol": "UM",
        "country": "Mauritania",
        "flag": "🇲🇷",
        "type": "Fiat"
    },
    "MUR": {
        "name": "Mauritian Rupee",
        "code": "MUR",
        "symbol": "₨",
        "country": "Mauritius",
        "flag": "🇲🇺",
        "type": "Fiat"
    },
    "MVR": {
        "name": "Maldivian Rufiyaa",
        "code": "MVR",
        "symbol": "Rf",
        "country": "Maldives",
        "flag": "🇲🇻",
        "type": "Fiat"
    },
    "MWK": {
        "name": "Malawian Kwacha",
        "code": "MWK",
        "symbol": "MK",
        "country": "Malawi",
        "flag": "🇲🇼",
        "type": "Fiat"
    },
    "MXN": {
        "name": "Mexican Peso",
        "code": "MXN",
        "symbol": "$",
        "country": "Mexico",
        "flag": "🇲🇽",
        "type": "Fiat"
    },
    "MYR": {
        "name": "Malaysian Ringgit",
        "code": "MYR",
        "symbol": "RM",
        "country": "Malaysia",
        "flag": "🇲🇾",
        "type": "Fiat"
    },
    "MZN": {
        "name": "Mozambican Metical",
        "code": "MZN",
        "symbol": "MT",
        "country": "Mozambique",
        "flag": "🇲🇿",
        "type": "Fiat"
    },
    "NAD": {
        "name": "Namibian Dollar",
        "code": "NAD",
        "symbol": "$",
        "country": "Namibia",
        "flag": "🇳🇦",
        "type": "Fiat"
    },
    "NGN": {
        "name": "Nigerian Naira",
        "code": "NGN",
        "symbol": "₦",
        "country": "Nigeria",
        "flag": "🇳🇬",
        "type": "Fiat"
    },
    "NIO": {
        "name": "Nicaraguan Córdoba",
        "code": "NIO",
        "symbol": "C$",
        "country": "Nicaragua",
        "flag": "🇳🇮",
        "type": "Fiat"
    },
    "NOK": {
        "name": "Norwegian Krone",
        "code": "NOK",
        "symbol": "kr",
        "country": "Norway",
        "flag": "🇳🇴",
        "type": "Fiat"
    },
    "NPR": {
        "name": "Nepalese Rupee",
        "code": "NPR",
        "symbol": "₨",
        "country": "Nepal",
        "flag": "🇳🇵",
        "type": "Fiat"
    },
    "NZD": {
        "name": "New Zealand Dollar",
        "code": "NZD",
        "symbol": "$",
        "country": "New Zealand",
        "flag": "🇳🇿",
        "type": "Fiat"
    },
    "OMR": {
        "name": "Omani Rial",
        "code": "OMR",
        "symbol": "ر.ع.",
        "country": "Oman",
        "flag": "🇴🇲",
        "type": "Fiat"
    },
    "PAB": {
        "name": "Panamanian Balboa",
        "code": "PAB",
        "symbol": "B/.",
        "country": "Panama",
        "flag": "🇵🇦",
        "type": "Fiat"
    },
    "PEN": {
        "name": "Peruvian Nuevo Sol",
        "code": "PEN",
        "symbol": "S/.",
        "country": "Peru",
        "flag": "🇵🇪",
        "type": "Fiat"
    },
    "PGK": {
        "name": "Papua New Guinean Kina",
        "code": "PGK",
        "symbol": "K",
        "country": "Papua New Guinea",
        "flag": "🇵🇬",
        "type": "Fiat"
    },
    "PHP": {
        "name": "Philippine Peso",
        "code": "PHP",
        "symbol": "₱",
        "country": "Philippines",
        "flag": "🇵🇭",
        "type": "Fiat"
    },
    "PKR": {
        "name": "Pakistani Rupee",
        "code": "PKR",
        "symbol": "₨",
        "country": "Pakistan",
        "flag": "🇵🇰",
        "type": "Fiat"
    },
    "PLN": {
        "name": "Polish Zloty",
        "code": "PLN",
        "symbol": "zł",
        "country": "Poland",
        "flag": "🇵🇱",
        "type": "Fiat"
    },
    "PYG": {
        "name": "Paraguayan Guarani",
        "code": "PYG",
        "symbol": "₲",
        "country": "Paraguay",
        "flag": "🇵🇾",
        "type": "Fiat"
    },
    "QAR": {
        "name": "Qatari Rial",
        "code": "QAR",
        "symbol": "ر.ق",
        "country": "Qatar",
        "flag": "🇶🇦",
        "type": "Fiat"
    },
    "RON": {
        "name": "Romanian Leu",
        "code": "RON",
        "symbol": "lei",
        "country": "Romania",
        "flag": "🇷🇴",
        "type": "Fiat"
    },
    "RSD": {
        "name": "Serbian Dinar",
        "code": "RSD",
        "symbol": "дин.",
        "country": "Serbia",
        "flag": "🇷🇸",
        "type": "Fiat"
    },
    "RUB": {
        "name": "Russian Ruble",
        "code": "RUB",
        "symbol": "₽",
        "country": "Russia",
        "flag": "🇷🇺",
        "type": "Fiat"
    },
    "RWF": {
        "name": "Rwandan Franc",
        "code": "RWF",
        "symbol": "FRw",
        "country": "Rwanda",
        "flag": "🇷🇼",
        "type": "Fiat"
    },
    "SAR": {
        "name": "Saudi Riyal",
        "code": "SAR",
        "symbol": "ر.س",
        "country": "Saudi Arabia",
        "flag": "🇸🇦",
        "type": "Fiat"
    },
    "SBD": {
        "name": "Solomon Islands Dollar",
        "code": "SBD",
        "symbol": "$",
        "country": "Solomon Islands",
        "flag": "🇸🇧",
        "type": "Fiat"
    },
    "SCR": {
        "name": "Seychellois Rupee",
        "code": "SCR",
        "symbol": "₨",
        "country": "Seychelles",
        "flag": "🇸🇨",
        "type": "Fiat"
    },
    "SDG": {
        "name": "Sudanese Pound",
        "code": "SDG",
        "symbol": "£",
        "country": "Sudan",
        "flag": "🇸🇩",
        "type": "Fiat"
    },
    "SEK": {
        "name": "Swedish Krona",
        "code": "SEK",
        "symbol": "kr",
        "country": "Sweden",
        "flag": "🇸🇪",
        "type": "Fiat"
    },
    "SGD": {
        "name": "Singapore Dollar",
        "code": "SGD",
        "symbol": "$",
        "country": "Singapore",
        "flag": "🇸🇬",
        "type": "Fiat"
    },
    "SHP": {
        "name": "Saint Helena Pound",
        "code": "SHP",
        "symbol": "£",
        "country": "Saint Helena",
        "flag": "🇸🇭",
        "type": "Fiat"
    },
    "SLL": {
        "name": "Sierra Leonean Leone",
        "code": "SLL",
        "symbol": "Le",
        "country": "Sierra Leone",
        "flag": "🇸🇱",
        "type": "Fiat"
    },
    "SOS": {
        "name": "Somali Shilling",
        "code": "SOS",
        "symbol": "Sh",
        "country": "Somalia",
        "flag": "🇸🇴",
        "type": "Fiat"
    },
    "SRD": {
        "name": "Surinamese Dollar",
        "code": "SRD",
        "symbol": "$",
        "country": "Suriname",
        "flag": "🇸🇷",
        "type": "Fiat"
    },
    "SSP": {
        "name": "South Sudanese Pound",
        "code": "SSP",
        "symbol": "£",
        "country": "South Sudan",
        "flag": "🇸🇸",
        "type": "Fiat"
    },
    "STN": {
        "name": "São Tomé and Príncipe Dobra",
        "code": "STN",
        "symbol": "Db",
        "country": "São Tomé and Príncipe",
        "flag": "🇸🇹",
        "type": "Fiat"
    },
    "SYP": {
        "name": "Syrian Pound",
        "code": "SYP",
        "symbol": "£",
        "country": "Syria",
        "flag": "🇸🇾",
        "type": "Fiat"
    },
    "SZL": {
        "name": "Swazi Lilangeni",
        "code": "SZL",
        "symbol": "L",
        "country": "Eswatini",
        "flag": "🇸🇿",
        "type": "Fiat"
    },
    "THB": {
        "name": "Thai Baht",
        "code": "THB",
        "symbol": "฿",
        "country": "Thailand",
        "flag": "🇹🇭",
        "type": "Fiat"
    },
    "TJS": {
        "name": "Tajikistani Somoni",
        "code": "TJS",
        "symbol": "SM",
        "country": "Tajikistan",
        "flag": "🇹🇯",
        "type": "Fiat"
    },
    "TMT": {
        "name": "Turkmenistani Manat",
        "code": "TMT",
        "symbol": "m",
        "country": "Turkmenistan",
        "flag": "🇹🇲",
        "type": "Fiat"
    },
    "TND": {
        "name": "Tunisian Dinar",
        "code": "TND",
        "symbol": "د.ت",
        "country": "Tunisia",
        "flag": "🇹🇳",
        "type": "Fiat"
    },
    "TOP": {
        "name": "Tongan Pa'anga",
        "code": "TOP",
        "symbol": "T$",
        "country": "Tonga",
        "flag": "🇹🇴",
        "type": "Fiat"
    },
    "TRY": {
        "name": "Turkish Lira",
        "code": "TRY",
        "symbol": "₺",
        "country": "Turkey",
        "flag": "🇹🇷",
        "type": "Fiat"
    },
    "TTD": {
        "name": "Trinidad and Tobago Dollar",
        "code": "TTD",
        "symbol": "TT$",
        "country": "Trinidad and Tobago",
        "flag": "🇹🇹",
        "type": "Fiat"
    },
    "TWD": {
        "name": "New Taiwan Dollar",
        "code": "TWD",
        "symbol": "NT$",
        "country": "Taiwan",
        "flag": "🇹🇼",
        "type": "Fiat"
    },
    "TZS": {
        "name": "Tanzanian Shilling",
        "code": "TZS",
        "symbol": "Sh",
        "country": "Tanzania",
        "flag": "🇹🇿",
        "type": "Fiat"
    },
    "UAH": {
        "name": "Ukrainian Hryvnia",
        "code": "UAH",
        "symbol": "₴",
        "country": "Ukraine",
        "flag": "🇺🇦",
        "type": "Fiat"
    },
    "UGX": {
        "name": "Ugandan Shilling",
        "code": "UGX",
        "symbol": "USh",
        "country": "Uganda",
        "flag": "🇺🇬",
        "type": "Fiat"
    },
    "USD": {
        "name": "United States Dollar",
        "code": "USD",
        "symbol": "$",
        "country": "United States",
        "flag": "🇺🇸",
        "type": "Fiat"
    },
    "UYU": {
        "name": "Uruguayan Peso",
        "code": "UYU",
        "symbol": "$U",
        "country": "Uruguay",
        "flag": "🇺🇾",
        "type": "Fiat"
    },
    "UZS": {
        "name": "Uzbekistan Som",
        "code": "UZS",
        "symbol": "лв",
        "country": "Uzbekistan",
        "flag": "🇺🇿",
        "type": "Fiat"
    },
    "VES": {
        "name": "Venezuelan Bolívar",
        "code": "VES",
        "symbol": "Bs.S",
        "country": "Venezuela",
        "flag": "🇻🇪",
        "type": "Fiat"
    },
    "VND": {
        "name": "Vietnamese Dong",
        "code": "VND",
        "symbol": "₫",
        "country": "Vietnam",
        "flag": "🇻🇳",
        "type": "Fiat"
    },
    "VUV": {
        "name": "Vanuatu Vatu",
        "code": "VUV",
        "symbol": "VT",
        "country": "Vanuatu",
        "flag": "🇻🇺",
        "type": "Fiat"
    },
    "WST": {
        "name": "Samoan Tala",
        "code": "WST",
        "symbol": "WS$",
        "country": "Samoa",
        "flag": "🇼🇸",
        "type": "Fiat"
    },
    "XAF": {
        "name": "CFA Franc BEAC",
        "code": "XAF",
        "symbol": "FCFA",
        "country": "Cameroon",
        "flag": "🇨🇲",
        "type": "Fiat"
    },
    "XCD": {
        "name": "East Caribbean Dollar",
        "code": "XCD",
        "symbol": "$",
        "country": "Antigua and Barbuda",
        "flag": "🇦🇬",
        "type": "Fiat"
    },
    "XOF": {
        "name": "CFA Franc BCEAO",
        "code": "XOF",
        "symbol": "CFA",
        "country": "Benin",
        "flag": "🇧🇯",
        "type": "Fiat"
    },
    "XPF": {
        "name": "CFP Franc",
        "code": "XPF",
        "symbol": "₣",
        "country": "French Polynesia",
        "flag": "🇵🇫",
        "type": "Fiat"
    },
    "YER": {
        "name": "Yemeni Rial",
        "code": "YER",
        "symbol": "﷼",
        "country": "Yemen",
        "flag": "🇾🇪",
        "type": "Fiat"
    },
    "ZAR": {
        "name": "South African Rand",
        "code": "ZAR",
        "symbol": "R",
        "country": "South Africa",
        "flag": "🇿🇦",
        "type": "Fiat"
    },
    "ZMW": {
        "name": "Zambian Kwacha",
        "code": "ZMW",
        "symbol": "ZK",
        "country": "Zambia",
        "flag": "🇿🇲",
        "type": "Fiat"
    },
    "ZWL": {
        "name": "Zimbabwean Dollar",
        "code": "ZWL",
        "symbol": "$",
        "country": "Zimbabwe",
        "flag": "🇿🇼",
        "type": "Fiat"
    }
}

class YahooFinanceEngine:
    """
    Handles connection with Yahoo Finance API.
    Provides Real-Time Data for Currencies, Stocks, and Crypto.
    """
    
    def get_currency_rate(self, base, target):
        """Fetch live currency exchange rate (Smart Ticker Search)"""
        try:
            # 1. সাধারণ কারেন্সি চেষ্টা করা (যেমন: USDBDT=X)
            ticker1 = f"{base}{target}=X"
            data = yf.Ticker(ticker1).history(period="1d")
            
            if not data.empty:
                return data['Close'].iloc[-1]

            # 2. যদি ফেইল করে, তাহলে ক্রিপ্টো ফরম্যাট চেষ্টা করা (যেমন: BTC-USD)
            ticker2 = f"{base}-{target}"
            data2 = yf.Ticker(ticker2).history(period="1d")
            
            if not data2.empty:
                return data2['Close'].iloc[-1]
                
            return None

        except Exception as e:
            logger.error(f"Currency API Error: {e}")
            return None

    def get_stock_price(self, symbol):
        """Fetch live stock/crypto price"""
        try:
            data = yf.Ticker(symbol).history(period="1d")
            if not data.empty:
                return data['Close'].iloc[-1]
            return None
        except:
            return None

class MathEngine:
    """
    Safe and Powerful Math Evaluator.
    Supports: Basic Math, Trig, Log, Powers.
    """
    @staticmethod
    def solve(expression):
        allowed_chars = "0123456789.+-*/()%^ sincoqrtalgpe"
        
        # Security Check: Remove dangerous characters
        clean_expr = expression.lower().replace(' ', '')
        for char in clean_expr:
            if char not in allowed_chars:
                return "❌ Error: Invalid Character"

        # Mapping to Python Math functions
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
        
        for key, value in replacements.items():
            clean_expr = clean_expr.replace(key, value)

        try:
            # Safe Evaluation
            result = eval(clean_expr, {"__builtins__": None}, {"math": math})
            
            # Formatting Result
            if isinstance(result, float):
                if result.is_integer():
                    return str(int(result))
                return f"{result:.4f}"
            return str(result)
            
        except ZeroDivisionError:
            return "♾️ Infinity"
        except Exception:
            return "❌ Syntax Error"

# Initialize Engines
finance_engine = YahooFinanceEngine()
math_engine = MathEngine()

@bot.message_handler(commands=['start'])
def welcome_message(message):
    user = message.from_user.first_name
    text = (
        f"👋 **Hello {user}!**\n\n"
        "Welcome!\n"
        "I am powered by Google/Yahoo Finance Real-Time Data.\n\n"
        "🛠 **MY FEATURES:**\n"
        "💱 **Currency Converter**\n"
        "`/convert 100 USD BDT`\n\n"
        "🧮 **Scientific Calculator**\n"
        "`/calc 50 + sqrt(144)`\n\n"
        "📈 **Stock/Crypto Price**\n"
        "`/price BTC-USD` (Bitcoin)\n"
        "`/price AAPL` (Apple)\n\n"
        "🌍 **World Time**\n"
        "`/time London`\n"
        "🔍 **Inline Mode:** Type `@mybot 100 USD BDT` in any chat."
    )
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/YOUR_USER_NAME")
    btn2 = types.InlineKeyboardButton("📜 Currency List", callback_data="show_list")
    markup.add(btn1, btn2)
    
    bot.reply_to(message, text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_message(message):
    text = (
        "🆘 **HELP & DOCUMENTATION**\n\n"
        "1️⃣ **Currency Conversion**\n"
        "Format: `/convert [Amount] [From] [To]`\n"
        "Example: `/convert 500 SAR BDT`\n"
        "Note: We use Yahoo Finance for 100% accurate market rates.\n\n"
        "2️⃣ **Calculator Usage**\n"
        "Format: `/calc [Expression]`\n"
        "Supported: +, -, *, /, ^, sin, cos, sqrt\n"
        "Example: `/calc sin(90) + 10^2`\n\n"
        "3️⃣ **Check Prices (Stocks/Crypto)**\n"
        "Format: `/price [Symbol]`\n"
        "Example: `/price BTC-USD` for Bitcoin\n"
        "Example: `/price GOOGL` for Google Stock"
    )
    bot.reply_to(message, text)

# --- Currency Converter ---
@bot.message_handler(commands=['convert'])
def convert_currency(message):
    try:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "⚠️ **Format Error:**\nUse: `/convert 100 USD BDT`")
            return
            
        amount = float(parts[1])
        base = parts[2].upper()
        target = parts[3].upper()
        
        # Send 'Typing' action
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Fetch Rate
        rate = finance_engine.get_currency_rate(base, target)
        
        if rate:
            result = amount * rate
            
            # Get Currency Details from DB
            base_data = CURRENCY_DB.get(base, {"flag": "🏳️", "name": base})
            target_data = CURRENCY_DB.get(target, {"flag": "🏁", "name": target})
            
            response = (
                f"💱 **Exchange Rate (Live)**\n"
                f"{base_data['flag']} **{amount} {base}**\n"
                f"Checking Market Data... 📡\n"
                f"⬇️\n"
                f"{target_data['flag']} **{result:,.2f} {target}**\n"
                f"📈 **Rate:** 1 {base} = {rate:.4f} {target}\n"
                f"🕒 **Time:** {datetime.now().strftime('%I:%M %p')}"
            )
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "❌ **Error:** Invalid Currency Code or API Down.")
            
    except ValueError:
        bot.reply_to(message, "❌ **Error:** Amount must be a number.")
    except Exception as e:
        logger.error(f"Convert Error: {e}")
        bot.reply_to(message, "❌ System Error. Try again later.")

# --- Calculator ---
@bot.message_handler(commands=['calc'])
def calculate(message):
    try:
        expression = message.text.replace('/calc', '').strip()
        if not expression:
            bot.reply_to(message, "⚠️ Write some math! Example: `/calc 10+20`")
            return
            
        result = math_engine.solve(expression)
        
        bot.reply_to(message, f"🔢 **Result:** `{result}`")
        
    except Exception as e:
        bot.reply_to(message, "❌ Calculation Failed.")

# --- Stock/Crypto Price ---
@bot.message_handler(commands=['price'])
def check_price(message):
    try:
        symbol = message.text.replace('/price', '').strip().upper()
        if not symbol:
            bot.reply_to(message, "⚠️ Example: `/price BTC-USD`")
            return
            
        bot.send_chat_action(message.chat.id, 'typing')
        price = finance_engine.get_stock_price(symbol)
        
        if price:
            bot.reply_to(message, f"📈 **{symbol} Price:** ${price:,.2f}")
        else:
            bot.reply_to(message, f"❌ Symbol `{symbol}` not found.")
    except:
        bot.reply_to(message, "❌ Error fetching price.")

# --- World Time ---
@bot.message_handler(commands=['time'])
def world_time(message):
    try:
        location = message.text.replace('/time', '').strip()
        if not location:
            bot.reply_to(message, "⚠️ Example: `/time London`")
            return

        query = location.lower().replace(' ', '_')
        match = None
        for tz_name in pytz.all_timezones:
            city = tz_name.split('/')[-1].lower()
            if city == query or query in city:
                match = tz_name
                break

        if not match:
            bot.reply_to(message, f"❌ Couldn't find a timezone for `{location}`.")
            return

        now = datetime.now(pytz.timezone(match))
        bot.reply_to(
            message,
            f"🕒 **{location.title()}** ({match})\n{now.strftime('%Y-%m-%d %I:%M:%S %p')}"
        )
    except Exception as e:
        logger.error(f"Time Error: {e}")
        bot.reply_to(message, "❌ Error fetching world time.")

@bot.inline_handler(lambda query: len(query.query) > 0)
def inline_manager(query):
    text = query.query.strip()
    results = []
    
    try:
        parts = text.split()
        
        # --- SCENARIO 1: Currency (e.g., 100 USD BDT) ---
        if len(parts) == 3 and parts[0].replace('.', '', 1).isdigit():
            amount = float(parts[0])
            base = parts[1].upper()
            target = parts[2].upper()
            
            rate = finance_engine.get_currency_rate(base, target)
            
            if rate:
                final_amount = amount * rate
                
                # Metadata
                base_flag = CURRENCY_DB.get(base, {}).get("flag", "")
                target_flag = CURRENCY_DB.get(target, {}).get("flag", "")
                
                title = f"{base_flag} {amount} {base} ➡️ {target_flag} {final_amount:.2f} {target}"
                desc = f"Market Rate: 1 {base} = {rate:.4f} {target}"
                
                r1 = types.InlineQueryResultArticle(
                    id='1',
                    title=title,
                    description=desc,
                    input_message_content=types.InputTextMessageContent(
                        f"{title}\nRate: {rate:.4f}"
                    )
                )
                results.append(r1)

        # --- SCENARIO 2: Calculator (e.g., 50+50) ---
        else:
            calc_res = math_engine.solve(text)
            if "Error" not in calc_res:
                r2 = types.InlineQueryResultArticle(
                    id='2',
                    title=f"🔢 Calculate: {text}",
                    description=f"Result: {calc_res}",
                    input_message_content=types.InputTextMessageContent(
                        f"🔢 **{text}** = `{calc_res}`"
                    )
                )
                results.append(r2)
        
        bot.answer_inline_query(query.id, results, cache_time=1)
        
    except Exception as e:
        logger.error(f"Inline Error: {e}")

def start_bot():
    """Runs the bot with auto-restart capability"""
    while True:
        try:
            logger.info("Bot is connecting to Telegram Servers...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"Connection Lost: {e}")
            time.sleep(5)
            logger.info("Reconnecting...")

if __name__ == "__main__":
    start_keep_alive()
    start_bot()
