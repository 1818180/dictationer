import pandas as pd

from sort_tool.output import OutputData
from db.db_add import DatabaseSave
from db.db_fetch import DatabaseFetch
from sort_tool.data_process import DataProcessor

# 导入单词和数据
class InputWords:

    # 格式化清理str输入
    @staticmethod
    def listed_words(words:str):
        words = words.split('\n')
        clean_words = DataProcessor.list_process(words)
        return clean_words

    @staticmethod
    def remove_old_words(words:list):
        # 获取已有的生单词,去除已有单词
        words_db = OutputData.get_all_words()
        if words_db:
            clean_words = DataProcessor.remove_common_elements(words,words_db)
            return clean_words
        else:
            return words

    @classmethod
    def clean_inputs(cls,words:str):
        clean_words = cls.listed_words(words)
        # print(f"💙clean_words={clean_words}")
        clean_words = cls.remove_old_words(clean_words)
        # print(f"💙clean_words={clean_words}")
        return clean_words

    @staticmethod
    def add_tag(words:list, tag:str):
        tag = '(' + tag + ')'
        for w in words:
            w_tag = OutputData.get_word_tags(word=w,quote=True) # 带（）的标签列表
            # print(f"💛已有单词的标签{w} = {w_tag}")
            if w_tag:
                if tag not in w_tag:
                    w_tag.append(tag)
                w_tag = ','.join(w_tag)
            else:
                w_tag = tag
            # w_tag需要是str
            # print(f"💛存入的标签{w} = {w_tag}")
            DatabaseSave.update_table(query='''UPDATE words SET groups=? WHERE word=?;''',params=(w_tag,w))

    @classmethod
    def add_log(cls,words:list, correct: bool = True):
        for word in words:
            word_log = OutputData.get_word_log(word)
            if word_log is None:
                word_log = ''
            if correct is True:
                word_log_update = word_log + '1'
            else:
                word_log_update = word_log + '0'
            DatabaseSave.update_colum(
                colum='log',
                new=word_log_update,
                condition="WHERE word = ?",
                condition_value=[word]
            )            

    # def add_notes(cls, words:list, notes:list):
        # for word, note in zip(words, notes):


    @classmethod
    def change_groups(cls,words:list, delete_group:str = None, new_group:str = None):
        if new_group:
            cls.add_tag(words=words,tag=new_group)
        elif delete_group:
            DatabaseSave.delete_group_tag(words=words,tag=delete_group)

    @classmethod
    def save_new_words(cls, group_name:str = None, words:str = None, words_list:list = []):
        if words:
            #先把不重复的新单词导入到数据库，再给每个单词加上tag
            # print(f"🔴words={words}")
            clean_words = cls.clean_inputs(words) #所有不重复单词列表
            all_clean_words = cls.listed_words(words) #包括重复单词的列表
            if clean_words:
                numbers = len(clean_words)
            else:
                numbers = 0
            if clean_words:
                DatabaseSave.add_new_words(clean_words)
            if group_name:
                words = words.split('\n')
                cls.add_tag(all_clean_words,group_name)
            return numbers
                
        elif words_list:
            clean_words = DataProcessor.list_process(words_list)
            only_words = cls.remove_old_words(clean_words)
            DatabaseSave.add_new_words(only_words)
            if group_name:
                cls.add_tag(clean_words,group_name)


    def mark_time(words:list, type:str):
        for w in words:
            old = DatabaseFetch.colum_condition(
                colum=[type],
                condition=f"WHERE word = ?",
                condition_value=[w]
            )
            old = old[0]
            if old:
                new = old + 1
            else:
                new = 1
            DatabaseSave.update_colum(
                colum=type,
                new=new,
                condition=f"WHERE word = ?",
                condition_value=[w]
            )

    # 保存听写结果及笔记
    @classmethod
    def checked_in(cls,checked_df):
        # 找出正确错误单词
        df = pd.DataFrame(checked_df)
        all_words = df["正确单词"].tolist()
        cls.save_new_words(words_list=all_words)
        cls.mark_time(all_words, 'dictate_times')

        incorrect_words = df[df["✔"] == "❌"]["正确单词"].tolist()
        cls.mark_time(incorrect_words, 'wrong_times')
        cls.add_log(incorrect_words, False)

        correct_words = df[df["✔"] == "✔"]["正确单词"].tolist()
        cls.add_log(correct_words)


        # 找出错误原因及对应笔记
        unknown_words = df[df["错误原因"] == "生词"]["正确单词"].tolist()
        cls.add_tag(words=unknown_words,tag="生词")

        pronunciation_words = df[df["错误原因"] == "发音"]["正确单词"].tolist()
        cls.add_tag(words=pronunciation_words,tag="发音")

        form_words = df[df["错误原因"] == "词形"]["正确单词"].tolist()
        cls.add_tag(words=form_words,tag="词形")


    @staticmethod
    def deletwords(words:list):
        for word in words:
            DatabaseSave.update_table(f'''DELETE FROM {DatabaseSave.table} WHERE word=? ''',params=(word,))
