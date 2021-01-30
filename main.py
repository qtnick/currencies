from requests_html import HTMLSession
import time
from datetime import datetime
from pytz import timezone


now_poland = datetime.now(timezone('Europe/Warsaw'))

print('Ctrl+c to exit.\n')


def usd_to_pln():
    session = HTMLSession()
    response = session.get('https://internetowykantor.pl/kurs-dolara/')

    ex_rate = response.html.find('span.kurs_sredni', first=True)
    print(f'Current USD-PLN exchange rate: {ex_rate.text} ({now_poland.strftime("%H:%M:%S %d-%m-%y")})')


while True:
    try:
        usd_to_pln()
        time.sleep(10)
    except KeyboardInterrupt:
        print('\nInterrupted.')
        break
