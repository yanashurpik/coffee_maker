from __future__ import annotations

import pathlib
from abc import ABC, abstractmethod
from typing import Optional


class Command(ABC):
    """
    The Command interface declares a method for executing a command.
    """

    @abstractmethod
    def execute(self) -> str:
        pass


class TurnOn(Command):
    """
    Command that can implement simple operation (turn on the drink maker) on their own before main actions.
    """

    def __init__(self, drink_maker: DrinkMaker):
        self._drink_maker = drink_maker

    def execute(self) -> str:
        return f"Drink maker '{self._drink_maker.name}' is starting..."


class TurnOff(Command):
    """
    Command that can implement simple operation (turn off the drink maker) after main actions.
    """

    def __init__(self, drink_maker: DrinkMaker):
        self._drink_maker = drink_maker

    def execute(self) -> str:
        return f"Drink maker '{self._drink_maker.name}' is off. Goodbye!"


class Order(Command):
    """
    However, Order command can delegate more complex operations to other
    objects, called "receivers" = drink_maker.
    """

    def __init__(
        self, drink_maker: DrinkMaker, drink_name: str, sugar_quantity: int = 0
    ):
        self._drink_maker = drink_maker
        self.drink_name = drink_name
        self.sugar_quantity = sugar_quantity

    def execute(self) -> str:
        self._drink_maker.to_order_drink(drink_name=self.drink_name)
        self._drink_maker.add_sugar(sugar_quantity=self.sugar_quantity)
        return self._drink_maker.send_message()


class SaveOrderHistory(Command):
    """
    Command that can implement simple operation (save the history of drink_maker orders) after main actions.
    """

    def __init__(self, order: Order, drink_maker: DrinkMaker):
        self._order = order
        self._drink_maker = drink_maker

    def execute(self) -> None:
        self._drink_maker.save_in_order_history(self._order)
        print("Order is saved")


class DrinkMaker:
    """
    The Receiver class (DrinkMaker) contain some important business logic. It knows how to
    perform all kinds of operations, associated with carrying out a request.
    """

    def __init__(self):
        self.name = "Drink Maker Pro Max"
        self.drink_name: Optional[str] = None
        self.sugar_quantity: Optional[int] = None
        self.stick: bool = False
        self.history = set()

    def to_order_drink(self, drink_name: str) -> None:
        self.drink_name = drink_name

    def add_sugar(self, sugar_quantity: int) -> None:
        self.sugar_quantity = sugar_quantity
        self.stick = True

    def save_in_order_history(self, order: Order):
        self.history.add(order)

    def send_message(self) -> str:
        if self.sugar_quantity > 0:
            return f"Drink maker makes 1 {self.drink_name} with {self.sugar_quantity} sugar and a stick"
        return f"Drink maker makes 1 {self.drink_name} with no sugar - and therefore no stick"


class Invoker:
    """
    The Invoker is associated with one or several commands. It sends a request
    to the command.
    """

    def __init__(self):
        self.commands: list[Command] = []
        self._on_start = None
        self._on_finish: list[Command] = []

    def set_commands(self, commands: list[Command]) -> None:
        self.commands = commands

    def set_on_start(self, command: Command) -> None:
        self._on_start = command

    def set_on_finish(self, commands: list[Command]) -> None:
        self._on_finish = commands

    def invoke(self) -> str:
        ready_order: str = ""

        if isinstance(self._on_start, Command):
            print(self._on_start.execute())

        for command in self.commands:
            ready_order = command.execute()
            print(ready_order)

        for command in self._on_finish:
            print(command.execute())

        return ready_order

