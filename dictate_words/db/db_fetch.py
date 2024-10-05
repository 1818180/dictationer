import sqlite3

# 通用型
class DatabaseFetch:

    # database_path = "D:/resource/Python_relate/database_all/english_learning/dictation.db"
    database_path = "db/dictation.db"
    table="words"

    @classmethod
    def fetch_db(cls, query, params=()):
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        r = cursor.fetchall()
        conn.close()
        return r

    @classmethod
    def all_colums(cls):
        results = cls.fetch_db(f'''SELECT * FROM {cls.table};''')
        return results

    @classmethod
    def some_colums(cls, colums:list):
        columns_str = ', '.join(colums)
        results = cls.fetch_db(f"SELECT {columns_str} FROM {cls.table}")
        return results
# '''
# [
#     (1, 'Alice', 30),
#     (2, 'Bob', 25),
#     (3, 'Charlie', 35)
# ]
# '''

    @classmethod
    def colum_condition(cls, colum:list, condition_value:list = [], condition:str = None):
        if len(colum) == 1:
            columns_str = colum[0]
        else:
            columns_str = ', '.join(colum)
        if condition:
            if condition_value:
                con_params = ()
                if len(condition_value) == 1:
                    con_params = (condition_value[0],)
                else:
                    con_params = tuple(condition_value)
                # print(f'🔹con_params={con_params}')
                results = cls.fetch_db(query=f"SELECT {columns_str} FROM {cls.table} {condition}; ", params=con_params)
            else:
                results = cls.fetch_db(query=f"SELECT {columns_str} FROM {cls.table} {condition}; ")
        else:
            results = cls.fetch_db(query=f"SELECT {columns_str} FROM {cls.table};")

        if columns_str == '*' or len(colum) > 1:
            return results
        else:
            return [r[0] for r in results]



    # 选择column里的唯一元素
    @classmethod
    def distinct_values(cls, colum:str, condition_value:list = [], condition:str = None):
        if condition:
            if condition_value:
                con_params = ()
                if len(condition_value) == 1:
                    con_params = (condition_value[0],)
                else:
                    con_params = tuple(condition_value)
                results = cls.fetch_db(f"SELECT DISTINCT {colum} FROM {cls.table} {condition};", params=con_params)
            else:
                results = cls.fetch_db(f"SELECT DISTINCT {colum} FROM {cls.table} {condition};")
        else:
            results = cls.fetch_db(f"SELECT DISTINCT {colum} FROM {cls.table};")
        return results
    

if __name__ == "__main__":
    all_words = DatabaseFetch.all_colums("words")
    print(all_words)