import sqlite3

class DB_info:
    
    word = "word"
    time = "time"
    dictate_times = "dictate_times"
    groups = "groups"
    notes = "notes"
    translation = "translation"


db_path="D:/resource/Python_relate/database_all/english_learning/dictation.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(f'''CREATE TABLE IF NOT EXISTS words (
                            id INTEGER PRIMARY KEY,
                            word TEXT,
                            time TEXT,
                            dictate_times INTEGER,
                            wrong_times INTEGER,
                            groups TEXT,
                            notes TEXT,
                            translation TEXT,
                            log TEXT 
        )''')
conn.commit()
conn.close()

if __name__ == "__main__":
    def clear_table(table_name: str):
        cursor.execute(f'''DELETE FROM {table_name}
        ''')
        conn.commit()

    def add_column(table_name: str, column_name: str, date_type: str):
        cursor.execute(f'''ALTER TABLE {table_name} ADD COLUMN {column_name} {date_type}
        ''')
        conn.commit()
    db_path="D:/resource/Python_relate/database_all/english_learning/dictation.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    table_names = ['words']

    # 删除表格内容
    # for name in table_names:
        # clear_table(name)
    # add_column('words', 'wrong_reason', 'TEXT')

    conn.close()
