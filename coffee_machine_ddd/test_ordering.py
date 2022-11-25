import pytest
from domain.model import OutOfStock, to_order, Drink, DrinkOrder


def test_drink_availability_logic():
    coffee = Drink(drink_name="coffee", quantity=4)
    tea = Drink(drink_name="tea", quantity=2)
    chocolate = Drink(drink_name="chocolate", quantity=1)

    order_1 = DrinkOrder(order_id="512", drink_name="tea", sugar=1)
    to_order(order_1, tea)
    assert tea.available_quantity == 1

    order_2 = DrinkOrder(order_id="587", drink_name="coffee", sugar=1)
    to_order(order_2, coffee)
    assert coffee.available_quantity == 3

    order_3 = DrinkOrder(order_id="56", drink_name="chocolate", sugar=2)
    to_order(order_3, chocolate)
    assert chocolate.available_quantity == 0

    order_4 = DrinkOrder(order_id="43", drink_name="chocolate", sugar=1)
    with pytest.raises(OutOfStock):
        to_order(order_4, chocolate)


def test_adding_sugar_and_stick():
    coffee = Drink(drink_name="coffee", quantity=3)
    tea = Drink(drink_name="tea", quantity=3)
    chocolate = Drink(drink_name="chocolate", quantity=3)

    order_1 = DrinkOrder(order_id="512", drink_name="tea", sugar=1)
    assert to_order(order_1, tea) == "Drink maker makes 1 tea with 1 sugar and a stick"

    order_2 = DrinkOrder(order_id="587", drink_name="coffee", sugar=2)
    assert (
        to_order(order_2, coffee)
        == "Drink maker makes 1 coffee with 2 sugar and a stick"
    )

    order_3 = DrinkOrder(order_id="56", drink_name="chocolate", sugar=0)
    assert (
        to_order(order_3, chocolate)
        == "Drink maker makes 1 chocolate with no sugar - and therefore no stick"
    )
