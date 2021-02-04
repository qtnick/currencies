from requests_html import HTMLSession
import time
from datetime import datetime
from pytz import timezone


class ExchangeRateScraper:
    def __init__(self):
        self.session = HTMLSession()
        self.interval_in_sec = 10

    def run_forever(self):
        print('Ctrl+c to exit.\n')
        while True:
            try:
                self.print_usd_exchange_rate()
                time.sleep(self.interval_in_sec)
            except KeyboardInterrupt:
                print('\nInterrupted.')
                exit(0)

    def print_usd_exchange_rate(self):
        response = self.session.get('https://internetowykantor.pl/kurs-dolara/')
        ex_rate = response.html.find('span.kurs_sredni', first=True)
        print(f'Current USD-PLN exchange rate: {ex_rate.text} ({self.current_time()})')

    @staticmethod
    def current_time():
        current_time = datetime.now(timezone('Europe/Warsaw'))
        return current_time.strftime("%H:%M:%S %d-%m-%y")


if __name__ == "__main__":
    ExchangeRateScraper().run_forever()
