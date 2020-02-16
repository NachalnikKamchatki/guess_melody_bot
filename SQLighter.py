import _sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = _sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """Получаем все строки таблицы"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM music').fetchall()

    def select_single(self, rownum):
        """Получаем одну строку с номером rownum"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE id = ?', (rownum,)).fetchall()[0]

    def select_genre(self, genre):
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE genre = ?', (genre, )).fetchall()

    def count_rows(self):
        """Счиатем количество строк"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM music').fetchall()
            return len(result)

    def count_rows_by_genre(self, genre):
        with self.connection:
            return len(self.cursor.execute('SELECT * FROM music WHERE genre = ?', (genre, )).fetchall())

    def close(self):
        """закрываем текущее соединение с базой"""
        self.connection.close()
