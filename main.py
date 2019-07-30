import network as network
from machine import SPI, Pin, reset
import json
import tinypico
from micropython_dotstar import DotStar
from utelegram import Telegram


def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config['SSID'], config['wifi_key'])
    # Wait until wifi is connected
    while not wlan.isconnected():
        pass

    # Configure SPI for controlling the DotStar
    # Internally we are using software SPI for this as the pins being used are not hardware SPI pins
    spi = SPI(sck=Pin(tinypico.DOTSTAR_CLK), mosi=Pin(tinypico.DOTSTAR_DATA), miso=Pin(tinypico.SPI_MISO))
    # Create a DotStar instance
    global dotstar
    dotstar = DotStar(spi, 1, brightness=0.5)  # Just one DotStar, half brightness

    telegram = Telegram(config['bot_token'])

    telegram.long_poll(callback)


def callback(msg, bot):
    if 'text' in msg:
        t = msg['text']
        if t == "/on":
            dotstar[0] = (255, 0, 0, 0.5)
        elif t == "/off":
            dotstar[0] = (0, 0, 0, 0)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        reset()
