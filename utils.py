import shelve
from random import shuffle

from SQLighter import SQLighter
from config import shelve_name, db_name

from telebot import types


def set_count_rows():
    """
    Данный метод считает общее коичество строк в базе данных и сохраняет в хранилище
    Потом из этого количества будем выбирать музыку
    """
    db = SQLighter(database=db_name)
    rows_num = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rows_num


def set_rows_count_by_genre(genre):
    """
        Данный метод считает количество записей в базе данных с определенным жанром и сохраняет в хранилище
        Потом из этого количества будем выбирать музыку определенного жанра
    """
    db = SQLighter(database=db_name)
    rows_num_by_genre = db.count_rows_by_genre(genre)
    with shelve.open(shelve_name) as storage:
        storage[genre] = rows_num_by_genre


def get_rows_count():
    """
    Получает из хранилища количество строк в БД
    :return: (int) Число строк
    """
    with shelve.open(shelve_name) as storage:
        rows_num = storage['rows_count']
    return rows_num


def get_rows_count_by_genre(genre):
    """"
    Получает из хранилища количество строк в БД с определенным жанром
    :param genre: Жанр музыки
    :return: (int) Число строк
    """
    with shelve.open(shelve_name) as storage:
        try:
            rows_num_by_genre = storage[genre]
            return rows_num_by_genre
        except KeyError:
            return 0


def set_user_game(chat_id, estimated_answer):
    """
    Записываем юзера в игроки и запоминаем, что он должен ответить
    :param chat_id: id юзера
    :param estimated_answer: правильный ответ (из БД)
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer


def finish_user_game(chat_id):
    """
    Заканчиваем игру текущего пользователя и удлаяем правильный ответ из хранилища
    :param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


def get_answer_from_user(chat_id):
    """
    Получаем правильный ответ для текущего юзера.
    В случае если человек просто ввел какие-то символы, не начав игру, возвращаем None
    :param chat_id: id юзера
    :return: (str) Правильный ответ / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            return None


def genre_markup(genres: list):

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for genre in genres:
        markup.add(types.KeyboardButton(text=genre))

    return markup


def generate_markup(right_answer, wrong_answers):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    all_answers = f'{right_answer}, {wrong_answers}'

    #  Создаем список и записываем в него все элементы
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    # Перемешиваем
    shuffle(list_items)
    # Заполняем разметку перемешанными элементами
    for item in list_items:
        markup.add(item)
    return markup
