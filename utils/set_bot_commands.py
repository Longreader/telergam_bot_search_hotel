from config_data.config import DEFAULT_COMMANDS
from telebot.types import BotCommand


def set_default_commands(bot):
    """
    Display bot command
    :param bot: Bot
    :return: None
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
