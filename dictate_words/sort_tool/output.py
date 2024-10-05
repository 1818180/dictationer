import re

from db.db_fetch import DatabaseFetch
from sort_tool.data_process import DataProcessor

class OutputData:
    # 返回已有单词列表[word1, word2...]

    @classmethod
    def get_all_words(cls, detail:bool = False):
        all_words = DatabaseFetch.some_colums(colums=['word'])
        if detail is False:
            return [r[0] for r in all_words]
        else:
            return all_words


    @classmethod
    def get_groups_names(cls):
        all_tags = DatabaseFetch.distinct_values(colum='groups')
        all_tags = [t[0] for t in all_tags if t[0] is not None]
        if all_tags:
            tags = []
            for tag in all_tags:
                if ',' in tag:
                    for t in tag.split(','):
                        t = t[1:-1]
                        tags.append(t)
                else:
                    tag = tag[1:-1]
                    tags.append(tag)
            tags = DataProcessor.list_process(tags)
            sort_tags = DataProcessor.list_str_order(tags)
            return sort_tags
        else:
            return None
    

    def tag_format(word_tags:str, quote:bool = True):
        if word_tags:
            tags = word_tags.split(',')
            if quote is True:
                return tags #返回带（）的标签
            else:
                tags = [tag[1:-1] for tag in tags]
                return tags
        else:
            return None

    @classmethod
    def get_word_tags(cls,word:str, quote:bool = True):
        word_tags = DatabaseFetch.colum_condition(colum=['groups'],condition=f"WHERE word =?",condition_value=[word])#[none]
        # print(f"💙word_tags = {word_tags}")
        word_tags = word_tags[0]
        tags = cls.tag_format(word_tags,quote)
        return tags


    def get_grouped_words(tag:str, detail:bool = False):
        if detail is False:
            select_column = 'word'
        else:
            select_column = '*'

        words = DatabaseFetch.colum_condition(
                colum=[select_column],
                condition=f"WHERE groups LIKE ?",
                condition_value=[f'%{tag}%'])    
        return words
    

    # 获得单词听写次数及听写错误次数情况
    @staticmethod
    def get_words_times():
        dictate_times = DatabaseFetch.distinct_values('dictate_times',condition=f"ORDER BY dictate_times ASC")
        dictate_times = [time[0] for time in dictate_times]
        if None in dictate_times:
            dictate_times.remove(None)
            dictate_times.insert(0,0)
        times_dict = {}
        for dic_time in dictate_times:
            if dic_time == 0:
                wrong_times = DatabaseFetch.distinct_values(
                    'wrong_times',
                    condition=f"WHERE dictate_times IS NULL ORDER BY wrong_times ASC"
                    )
            else:
                wrong_times = DatabaseFetch.distinct_values(
                    'wrong_times',
                    condition=f"WHERE dictate_times = {dic_time} ORDER BY wrong_times ASC"
                    )
            wrong_times = [time[0] for time in wrong_times]
            if None in wrong_times:
                wrong_times.remove(None)
                wrong_times.insert(0,0)
            times_dict[dic_time] = []
            for wrong in wrong_times:
                times_dict[dic_time].append(wrong)
        return times_dict
        # {0:[0],2:[0,1,2]}

    @classmethod
    def words_times_options(cls):
        times_condition = cls.get_words_times()
        options = []
        for dic_time, wrong_times in times_condition.items():
            for wrong in wrong_times:
                options.append(f"听写次数{dic_time}，错误次数{wrong}")
        return tuple(options)


    def get_timed_words_detail(dictate_time:str = None, error_time:str = None, detail:bool = False):
        select_column = 'word' if not detail else '*'
        conditions = []
        if dictate_time is not None:
            conditions.append(f"dictate_times {dictate_time}")
        if error_time is not None:
            conditions.append(f"wrong_times {error_time}")
        condition = "WHERE " + " AND ".join(conditions) if len(conditions) > 1 else "WHERE " + conditions[0]
        # print(f"📍condition = {condition}")
        timed_words = DatabaseFetch.colum_condition(
            colum=[select_column],
            condition= condition)
        return timed_words
    
    @classmethod
    def get_timed_words(cls,option:str, detail:bool = False):
        dictate_time, error_time=DataProcessor.times_2number(option)
        if dictate_time == 0:
            dictate_time = f"IS NULL"
        else:
            dictate_time = f"= {dictate_time}"
        if error_time == 0:
            error_time = f"IS NULL"
        else:
            error_time = f"= {error_time}"
        timed_words = cls.get_timed_words_detail(dictate_time,error_time,detail)
        return timed_words


    @classmethod
    def get_word_log(cls,word:str):
        log = DatabaseFetch.colum_condition(
            colum=['log'],
            condition="WHERE word = ?",
            condition_value=[word]
        )
        return log[0] # 返回str

class DictateMaterial:

    def save_words_html(cls, words:list, setting:int):
        pass