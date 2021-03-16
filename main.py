from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
from pytz import timezone
import sqlite3


conn = sqlite3.connect('exchange_rates.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS exchange_rates (
            rate real,
            date real
            )""")


def insert_rate(rate, date):
    with conn:
        c.execute("INSERT INTO exchange_rates VALUES (:rate, :date)", {'rate': rate, 'date': date})


class ExchangeRateScraper:
    def __init__(self):
        self.interval_in_sec = 10

    def run_forever(self):
        print('\nCtrl+c to exit.\n')
        while True:
            try:
                self.print_usd_exchange_rate()
                time.sleep(self.interval_in_sec)
            except KeyboardInterrupt:
                print('\nInterrupted.')
                exit(0)

    def print_usd_exchange_rate(self):
        source = requests.get('https://internetowykantor.pl/kurs-dolara/').text
        html = BeautifulSoup(source, 'lxml')
        ex_rate = html.find('span', class_='kurs_sredni').text
        print(f'Current USD-PLN exchange rate: {ex_rate} ({self.current_time()})')
        insert_rate(ex_rate, self.current_time())

    @staticmethod
    def current_time():
        current_time = datetime.now(timezone('Europe/Warsaw'))
        return current_time.strftime("%H:%M:%S %d-%m-%y")


if __name__ == "__main__":
    ExchangeRateScraper().run_forever()

conn.commit()
conn.close()
