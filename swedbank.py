import pandas as pd
pd.set_option('display.max_colwidth', -1)


class Transfers:
    """Swedbank money transfer operations."""

    def __init__(self, frame: pd.DataFrame) -> None:
        self._frame = frame

    def payed(self) -> 'Transfers':
        """Filter transfers where I payed."""
        return Transfers(self._frame[self._frame.amount < 0])

    def for_(self, reason: str) -> 'Transfers':
        """Filter transfers by reason column pattern."""
        return Transfers(self._frame[self._frame.reason.str.contains(reason)])

    def exclude(self, reason: str) -> 'Transfers':
        """Exclude transfers that match reason column pattern."""
        return Transfers(
            self._frame[self._frame.reason.str.contains(reason) == False])

    def print(self) -> None:
        """Pretty print transfers."""
        for _, row in self._frame.iterrows():
            print('{} {:7.2f} {}'.format(row.date.strftime('%Y-%m-%d'),
                row.amount, row.reason))

    def within(self, start_date: str, end_date: str) -> 'Transfers':
        """Filter transfers by date."""
        date_filter = pd.date_range(start_date, end_date)
        return Transfers(self._frame[self._frame.date.isin(date_filter)])

    def __getattr__(self, attr: str):
        return getattr(self._frame, attr)


def read_transfers(csv_file: str) -> Transfers:
    """Read transfers from CSV file exported from Swedbank page."""
    data = pd.read_csv(csv_file)
    data = data[['Data', 'Paaiškinimai', 'Suma', 'D/K',]]
    data.columns = ['date', 'reason', 'amount', 'type']
    data.type = data.type.map({'K': '+', 'D': '-'})
    data.date = data.date.apply(lambda day: pd.Timestamp(day))
    data.amount = data[['amount', 'type']].apply(
        lambda at: _number_with_sign(*at), axis=1)
    return Transfers(data)


def _number_with_sign(n: float, sign: str) -> float:
    if sign == '-':
        return n * -1
    return n
