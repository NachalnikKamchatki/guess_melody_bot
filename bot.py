from random import randint, seed, choice

from config import token, db_name
from telebot import TeleBot, types

from SQLighter import SQLighter
import utils

bot = TeleBot(token)


@bot.message_handler(commands=['game'])
def game(message: types.Message):
    # Получаем случайную строку из БД
    msg = bot.send_message(
        message.chat.id,
        'Выберите жанр музыки, в котором вы хотите отгадывать.',
        reply_markup=utils.genre_markup(["Rock", "Pop", "Classic"])
    )
    bot.register_next_step_handler(msg, genre_choice)
    # random_melody = randint(1, utils.get_rows_count())
    # row = db_worker.select_single(random_melody)
    # # Формируем разметку
    # markup = utils.generate_markup(row[2], row[3])
    # # Отправляем аудиофайл с вариантами ответа
    # bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    # # Включаем "игровой режим"
    # utils.set_user_game(message.chat.id, row[2])


def genre_choice(message: types.Message):
    # Подключаемся к базе данных
    db_worker = SQLighter(db_name)

    if message.text == 'Rock':

        # Получаем из базы данных все композиции с жанром "Rock"
        rock_music = db_worker.select_genre('Rock')

        # Получаем file_id случайной мелодии
        random_melody = choice(rock_music)

        # Формируем разметку
        markup = utils.generate_markup(random_melody[2], random_melody[3])

        # Отправляем аудиофайл с вариантами ответа
        bot.send_voice(message.chat.id, random_melody[1], reply_markup=markup)

        # Включаем "игровой режим"
        utils.set_user_game(message.chat.id, random_melody[2])

    if message.text == 'Classic':
        # Получаем из базы данных все композиции с жанром "Classic"
        classsic_music = db_worker.select_genre('Classic')

        # Получаем file_id случайной мелодии
        random_melody = choice(classsic_music)

        # Формируем разметку
        markup = utils.generate_markup(random_melody[2], random_melody[3])

        # Отправляем аудиофайл с вариантами ответа
        bot.send_voice(message.chat.id, random_melody[1], reply_markup=markup)

        # Включаем "игровой режим"
        utils.set_user_game(message.chat.id, random_melody[2])

    if message.text == 'Pop':
        # Получаем из базы данных все композиции с жанром "Rock"
        pop_music = db_worker.select_genre('Pop')

        # Получаем file_id случайной мелодии
        random_melody = choice(pop_music)

        # Формируем разметку
        markup = utils.generate_markup(random_melody[2], random_melody[3])

        # Отправляем аудиофайл с вариантами ответа
        bot.send_voice(message.chat.id, random_melody[1], reply_markup=markup)

        # Включаем "игровой режим"
        utils.set_user_game(message.chat.id, random_melody[2])

    # Отключаемся от БД
    db_worker.close()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message: types.Message):
    answer = utils.get_answer_from_user(message.chat.id)
    # Если вернет None, то человек не в игре
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
    else:
        kb_hider = types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=kb_hider)
        else:
            bot.send_message(message.chat.id, 'Увы, Вы не угадали. Попробуйте ещё раз!', reply_markup=kb_hider)
        utils.finish_user_game(message.chat.id)


if __name__ == '__main__':
    utils.set_count_rows()
    utils.set_rows_count_by_genre('Rock')
    utils.set_rows_count_by_genre('Pop')
    utils.set_rows_count_by_genre('Classic')
    seed()
    bot.polling(none_stop=True)
