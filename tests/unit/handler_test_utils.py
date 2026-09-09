"""Shared fakes for exercising handlers/*.py without a real Telegram bot."""

from types import SimpleNamespace


class FakeBot:
    def __init__(self):
        self.replies = []
        self.inline_answers = None
        self._commands = {}
        self._inline_handlers = []

    def message_handler(self, commands=None, **kwargs):
        def decorator(func):
            for name in commands or []:
                self._commands[name] = func
            return func

        return decorator

    def inline_handler(self, filter_func):
        def decorator(func):
            self._inline_handlers.append(func)
            return func

        return decorator

    def reply_to(self, message, text, **kwargs):
        self.replies.append(text)

    def send_chat_action(self, chat_id, action):
        pass

    def answer_inline_query(self, query_id, results, **kwargs):
        self.inline_answers = results

    def call(self, command, message):
        return self._commands[command](message)

    def call_inline(self, query):
        return self._inline_handlers[0](query)


def make_message(text, chat_id=1, first_name="Tester"):
    return SimpleNamespace(
        text=text,
        chat=SimpleNamespace(id=chat_id),
        from_user=SimpleNamespace(first_name=first_name),
    )


def make_inline_query(text, query_id="1"):
    return SimpleNamespace(query=text, id=query_id)


def make_deps(**overrides):
    import logging

    defaults = dict(
        finance_engine=None,
        math_engine=None,
        transaction_store=None,
        get_currency=lambda code: {"flag": "🏳️", "name": code, "code": code},
        logger=logging.getLogger("test"),
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)
