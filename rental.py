from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Rental:
    """
    the rental data for a book
    """
    rental_date: datetime
    return_date: datetime
    num_rental_days: int

    @property
    def cost(self):
        days_overdue = (self.to_date - self.from_date).days - self.included_days

        if days_overdue > 0:
            return round(4.5 + days_overdue*3.35,2)
        else:
            return round(4.5,2)
