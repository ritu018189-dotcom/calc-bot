from . import calc, convert, help, inline, price, start, time_handler, verify

_MODULES = [start, help, convert, calc, price, time_handler, verify, inline]


def register_all(bot, deps):
    """Wire every command/inline handler onto the given TeleBot instance."""
    for module in _MODULES:
        module.register(bot, deps)
