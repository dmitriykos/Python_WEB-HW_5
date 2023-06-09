import aiohttp
import asyncio
import platform

from datetime import datetime, timedelta


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as responce:
                if responce.status == 200:
                    result = await responce.json()
                    return result
                else:
                    print(f"Error status: {responce.status} for {url}")
        except aiohttp.ClientConnectorError as err:
            print(f'Connection error: {url}', str(err))


async def main(days):
    res = []
    date_now = datetime.now().date()
    for i in range(0, days):
        date_to_show = date_now - timedelta(days=i)
        year = date_to_show.year
        month = date_to_show.month if date_to_show.month >= 10 else str(
            date_to_show.month).rjust(2, "0")
        day = date_to_show.day if date_to_show.day >= 10 else str(
            date_to_show.day).rjust(2, "0")
        my_date = f"{day}.{month}.{year}"
        result = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={my_date}')
        if result:
            currency_USD = [[rate["saleRate"], rate["purchaseRate"]]
                            for rate in result["exchangeRate"] if rate["currency"] == "USD"]
            currency_EUR = [[rate["saleRate"], rate["purchaseRate"]]
                            for rate in result["exchangeRate"] if rate["currency"] == "EUR"]
            # sale, buy = currency[0][0], currency[0][1]
            my_dict = {my_date: {"USD": {"sale": currency_USD[0][0], "purchase": currency_USD[0][1]}, "EUR": {
                "sale": currency_EUR[0][0], "purchase": currency_EUR[0][1]}}}
            res.append(my_dict)
    if res:
        return res
    else:
        return 'Not found'


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    while True:
        try:
            days = input("How many days to show the exchange rate? (Max 10 days): ")
            if days in ["exit", "cancel"]:
                break
            days = 10 if int(days) > 10 else 1 if int(days) <= 0 else int(days)
            break
        except:
            print("Please enter a number.")
            continue
    r = asyncio.run(main(days))
    print(r)
    