from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters
import os
import analyzer

# Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
updater = Updater(token=os.getenv('telegram_token_chess'), use_context=True)
dispatcher = updater.dispatcher


def start_handler(update, context):
    message = "Hey, good to see you! I'll analyze your chess games. " \
              "To have a game analyzed, just share the PGN from lichess or chess.com with me!\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    logging.info("Started chat %d", update.effective_chat.id)


def help_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='blub')


def stringify_blunders(blunders):
    result_string = "Here's the most interesting moves I could find: \n"
    for blunder in blunders:
        result_string += f"{str(blunder.get('turn'))}. {blunder.get('move')} "
        result_string += f"(before: {str(blunder.get('prev_score'))}, after: {blunder.get('new_score')})\n"
        result_string += 'Continuation: ' + blunder.get('continuation')
        result_string += '\n'
    return result_string


def message_handler(update, context):
    user_input = update.message.text
    pgn = analyzer.read_pgn_from_string(user_input)
    if pgn is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm analyzing your game now! This may take a second.")
        blunders = analyzer.analyze_game(pgn)
        context.bot.send_message(chat_id=update.effective_chat.id, text=stringify_blunders(blunders))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="That doesn't look like a PGN to me.")


dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(CommandHandler('help', help_handler))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))

updater.start_polling()
