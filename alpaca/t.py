from alpaca_trade_api.rest import REST
import json

from rich.console import Console
from rich.table import Table


class API:
    def __init__(self) -> None:
        self.api = REST(raw_data=True)


class Account(API):
    def __init__(self) -> None:
        super().__init__()

    def get_account(self) -> dict:
        return self.api.get_account()

    def get_activities(self) -> dict:
        return self.api.get_activities()

    def get_account_config(self) -> dict:
        return self.api.get_account_configurations()


class Clock(API):
    def __init__(self) -> None:
        super().__init__()

    def get_clock(self) -> dict:
        return self.api.get_clock()


class Positions(API):
    def __init__(self) -> None:
        super().__init__()

    def get_position(self, symbol: str) -> dict:
        return self.api.get_position(symbol=symbol)

    def list_positions(self) -> dict:
        return self.api.list_positions()


class News(API):
    def __init__(self) -> None:
        super().__init__()

    def get_news(self, symbol: str) -> dict:
        return self.api.get_news(symbol)


def output(data: dict) -> None:
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Attributes", justify="left")
    table.add_column("Values", justify="right")

    for key, value in data.items():
        table.add_row(str(key), str(value))

    console.print(table)


acc = Account()
account = acc.get_account()
activity = acc.get_activities()
config = acc.get_account_config()

clock = Clock()
clock_data = clock.get_clock()

position = Positions()
all_positions = position.list_positions()
get_positions = position.get_position("MARA")

news = News()
news_data = news.get_news("MARA")
print(news_data)

# =============================================================================
# Output
# =============================================================================

# account always returns a dict
# output(account)

# activities returns a list of dict list[dict]
# output(activity[0])

# config always returns a dict
# output(config)

# get_clock always returns a dict
# output(clock_data)

# list of dicts, we can have multiple positions
# for position in all_positions:
#     output(position)

# get_position returns dict
# output(get_positions)
