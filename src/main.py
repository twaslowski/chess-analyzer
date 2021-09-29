#!/usr/bin/env python3

from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters
import os
import emoji
import pgn_helper
from move_evaluation import MoveEvaluation
from typing import List
from analysis import Analysis
import time

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


def stringify_evals(move_evals: List[MoveEvaluation]):
    result_string = "Here's the most interesting moves I could find: \n\n"
    black_evals = [move_eval for move_eval in move_evals if move_eval.turn % 1 != 0]
    white_evals = [move_eval for move_eval in move_evals if move_eval.turn % 1 == 0]

    result_string += emoji.emojize("Moves for Black: :white_circle:\n\n")
    for move_eval in white_evals:
        result_string += move_eval.stringify() + '\n'

    result_string += emoji.emojize("Moves for Black: :black_circle:\n\n")
    for move_eval in black_evals:
        result_string += move_eval.stringify() + '\n'

    return result_string


def message_handler(update, context):
    user_input = update.message.text
    pgn = pgn_helper.read_pgn_from_string(user_input)
    if pgn is not None:
        analysis = Analysis(pgn)
        analysis.run()
        current_progress = analysis.progress
        msg = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Analyzing your game now! Progress: {current_progress}%")
        while analysis.is_done is not True:
            if current_progress != analysis.progress:
                current_progress = analysis.progress
                context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                              message_id=msg.message_id,
                                              text=f'Analyzing your game now! Progress: {current_progress}%')
            time.sleep(1)
        context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                      message_id=msg.message_id,
                                      text=f'Analyzing your game now! Progress: 100%')
        evals = analysis.move_evals
        context.bot.send_message(chat_id=update.effective_chat.id, text=stringify_evals(evals))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="That doesn't look like a PGN to me.")


def error_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="An error occurred while analyzing your game. Ping @violin_tobi for details.")


dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(CommandHandler('help', help_handler))
dispatcher.add_error_handler(error_handler)
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))

updater.start_polling()
