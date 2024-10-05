import sqlite3
from datetime import datetime


class DatabaseSave:
    # database_path = "D:/resource/Python_relate/database_all/english_learning/dictation.db"
    database_path = "db/dictation.db"
    table="words"

    @staticmethod
    def get_current_date():
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d')
        return formatted_date

    @classmethod
    def update_table(cls, query, params=()):
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()

    @classmethod
    def update_colum(cls, colum:str, new, condition:str, condition_value:list):
        values_set = []
        values_set.append(new)
        values_set = tuple(values_set + condition_value)
        query = f'''UPDATE {cls.table} SET {colum} = ? {condition};'''
        cls.update_table(query, values_set)

    @classmethod
    def add_new_words(cls, words: list):
        time = cls.get_current_date()
        query = f'''INSERT INTO "{cls.table}" (word, time) VALUES (?, ?);''' 
        for w in words:
            cls.update_table(query, (w, time))

    @classmethod
    def delete_group_tag(cls, words:list, tag:str):
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        for w in words:
            cursor.execute(f'''SELECT groups FROM words WHERE word=?;''',({w},))
            w_tag = cursor.fetchone()[0]
            # print(f"📍w_tag={w_tag}")
            if w_tag:
                tag = f"({tag})"
                if tag == w_tag:
                    w_tag = ''
                elif tag in w_tag:
                    new_tags = [t for t in w_tag.split(',') if t != tag]
                    w_tag = ','.join(new_tags)
            # print(f"📍📍w_tag={w_tag}")
            cursor.execute(f'''UPDATE words SET groups=? WHERE word=?;''',(w_tag,w))
            conn.commit()
        conn.close()


    @classmethod
    def deletwords(cls,words:list):
        for word in words:
            cls.update_table(f'''DELETE FROM {cls.table} WHERE word=? ''', query=(word,))


if __name__ == "__main__":
    pass