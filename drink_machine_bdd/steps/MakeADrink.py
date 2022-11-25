from behave import given, when, step, then, use_step_matcher
from drink_maker import (
    DrinkMaker,
    TurnOn,
    Invoker,
    TurnOff,
    Order,
    SaveOrderHistory,
)

use_step_matcher("re")


@given("drink_maker")
def step_impl(context):
    context.drink_maker = DrinkMaker()
    return context.drink_maker


@when("drink_maker is turn on")
def step_impl(context):
    context.turn_on_command = TurnOn(context.drink_maker)
    context.turn_off_command = TurnOff(context.drink_maker)

    context.invoker = Invoker()
    context.invoker.set_on_start(context.turn_on_command)


@step("(?P<drink>.+) is selected")
def step_impl(context, drink):
    order_command = Order(context.drink_maker, drink_name=drink)
    save_order = SaveOrderHistory(order_command, context.drink_maker)

    context.invoker.set_commands([order_command])
    context.invoker.set_on_finish([save_order, context.turn_off_command])


@step("order is running")
def step_impl(context):

    context.ready_order = context.invoker.invoke()
    return context.ready_order


@then("selected (?P<drink>.+) is created")
def step_impl(context, drink):
    assert (
        context.ready_order
        == f"Drink maker makes 1 {drink} with no sugar - and therefore no stick"
    )
