import urequests


class Telegram:
    offset = 0

    def __init__(self, bot_token):
        self.base_url = "https://api.telegram.org/bot" + bot_token + "/"

    def get_updates(self, timeout=0):
        data = {'offset': self.offset, 'timeout': timeout}
        res = urequests.post(self.base_url + "getUpdates", json=data).json()
        if not res['ok']:
            raise Exception("Error while polling telegram updates")
        res = res['result']
        if len(res) > 0:
            self.offset = res[-1]['update_id'] + 1
        return res

    def long_poll(self, callback):
        while True:
            res = self.get_updates(timeout=300)
            for upd in res:
                if 'message' in upd:
                    callback(upd['message'], self)

    def send_message(self, chat_id, text, **kwargs):
        kwargs['chat_id'] = chat_id
        kwargs['text'] = text
        res = urequests.post(self.base_url + "sendMessage", json=kwargs).json()
        if not res['ok']:
            raise Exception("Error while sending telegram message")
        return res['result']