from abc import ABC, abstractmethod


class DiscountStrategy(ABC):

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return round(total, 2)


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage: float):
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return round(total * (1 - self.percentage / 100), 2)


class BulkDiscount(DiscountStrategy):

    def __init__(self, threshold: float, amount: float):
        if threshold < 0:
            raise ValueError("Bulk discount threshold cannot be negative.")
        if amount < 0:
            raise ValueError("Bulk discount amount cannot be negative.")
        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float:
        discounted = total - self.amount if total >= self.threshold else total
        return round(max(discounted, 0), 2)


class StudentDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return round(total * 0.9, 2)
