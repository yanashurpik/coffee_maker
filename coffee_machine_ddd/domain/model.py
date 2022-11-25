from __future__ import annotations
from dataclasses import dataclass, field


class OutOfStock(Exception):
    pass


class TooMuchSugar(Exception):
    pass


def to_order(order: DrinkOrder, drink: Drink) -> str:
    if drink.can_be_ordered(order):
        drink.to_order(order)
        return drink.send_message(order)
    raise OutOfStock(f"Out of stock for drink {order.drink_name}")


@dataclass(unsafe_hash=True)
class DrinkOrder:
    order_id: str
    drink_name: str
    sugar: int
    quantity: int = field(default=0, init=False, repr=False)
    stick: bool = False

    _sugar: int = field(init=False, repr=False)

    @property
    def sugar(self) -> int:
        return self._sugar

    @sugar.setter
    def sugar(self, value: int) -> None:
        if value > 2:
            raise TooMuchSugar("Sorry, but you can order maximum 2 sugar")
        self._sugar = value

    def has_sugar(self) -> bool:
        return self.sugar > 0


class Drink:
    def __init__(self, quantity: int, drink_name: str):
        self.drink_name = drink_name
        self._purchased_quantity = quantity
        self._order_line = set()

    def __repr__(self):
        return f"<Drink {self.drink_name}>"

    def __eq__(self, other):
        if not isinstance(other, Drink):
            return False
        return other.drink_name == self.drink_name

    def __hash__(self):
        return hash(self.drink_name)

    def to_order(self, order: DrinkOrder):
        if order.has_sugar():
            order.stick = True
        order.quantity += 1
        self._order_line.add(order)

    def cancel_order(self, order: DrinkOrder):
        if order in self._order_line:
            self._order_line.remove(order)

    def send_message(self, order: DrinkOrder):
        if order.has_sugar():
            return f"Drink maker makes 1 {self.drink_name} with {order.sugar} sugar and a stick"
        return f"Drink maker makes 1 {self.drink_name} with no sugar - and therefore no stick"

    @property
    def ordered_quantity(self) -> int:
        return sum(order.quantity for order in self._order_line)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.ordered_quantity

    def can_be_ordered(self, order: DrinkOrder) -> bool:
        return self.available_quantity >= 1 and self.drink_name == order.drink_name
