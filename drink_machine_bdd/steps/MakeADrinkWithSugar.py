from behave import step, then, use_step_matcher
from drink_maker import Invoker, TurnOff, Order, SaveOrderHistory


use_step_matcher("re")


@step("(?P<drink>.+) with (?P<sugar_amount>.+) is ordered")
def step_impl(context, drink, sugar_amount):
    order_command = Order(
        context.drink_maker, drink_name=drink, sugar_quantity=int(sugar_amount)
    )
    context.save_order = SaveOrderHistory(order_command, context.drink_maker)
    context.invoker.set_commands([order_command])
    context.invoker.set_on_finish([context.save_order, context.turn_off_command])


@then(
    "selected (?P<drink>.+) is created with (?P<sugar_amount>.+) of sugar and stick = (?P<is_stick>.+)"
)
def step_impl(context, drink, sugar_amount, is_stick):
    if int(sugar_amount) > 0:
        assert (
            context.ready_order
            == f"Drink maker makes 1 {drink} with {sugar_amount} sugar and a stick"
        )
    else:
        assert (
            context.ready_order
            == f"Drink maker makes 1 {drink} with no sugar - and therefore no stick"
        )
    assert context.drink_maker.stick == bool(is_stick)
