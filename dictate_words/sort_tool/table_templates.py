# import streamlit as st
import pandas as pd
import streamlit as st
from sort_tool.output import OutputData
from sort_tool.data_process import DataProcessor

class TableTemplates:

    # 用于听写的表格
    def dictate_table(words:list):
        table = []
        i = 1
        for word in words:
            table.append(
                {"Index": i, "Word": ''}
            )
            i += 1
        return pd.DataFrame(table)

    # 用于检查后的笔记表格
    def checked_table(unchecked_words:list[str], correct_words:list[str]):
        
        table = []
        for unchecked, correct in zip(unchecked_words[0], correct_words):
            if unchecked.lower() == correct.lower():
                table.append(
                    {"我的单词": unchecked, "正确单词": correct, "✔": '✔', "错误原因": '', "单词笔记": ''}
                )
            else:
                table.append(
                    {"我的单词": unchecked, "正确单词": correct, "✔": '❌', "错误原因": '', "单词笔记": ''}
                )
        return table
    

    # '''
    # [
    #     (1, 'Alice', 30),
    #     (2, 'Bob', 25),
    #     (3, 'Charlie', 35)
    # ]
    # '''


    @classmethod
    def show_detailed_info(cls,words:list, group:str = None, times:list = []):
        table = []
        i=1
        for word in words:
            # print(f"⭐word ={word}")
            w_word = word[1]
            w_dictate = word[3]
            w_wrong = word[4]
            w_tag = word[5]
            w_note = word[6]
            w_translation = word[7]
            w_log = word[8]

            if w_translation is None:
                w_translation = ''

            if w_note is None:
                w_note = ''

            if w_wrong is None:
                w_wrong = 0

            if w_dictate is None:
                w_dictate = 0

            tags = OutputData.tag_format(w_tag, quote=False)
            if group:
                tags = [t for t in tags if t != group]

            if w_log is None:
                w_log = [0]
            elif w_log:
                #  w_log = DataProcessor.str_number_2list(w_log)
                 w_log = [int(char) for char in w_log]

            # 正确率
            if w_dictate > 0:
                correct_time = w_dictate - w_wrong
                rate = (correct_time / w_dictate)
            else:
                rate = 0

            if times:
                if w_wrong == times[1] and w_dictate == times[0]:
                    table.append(
                        {
                            "单词数量": i,
                            "单词词组": w_word,
                            # "中文翻译": w_translation,
                            # "正确率": rate, # 20%
                            "单词分组": tags, # list
                            "单词笔记": w_note,
                            "听写趋势": w_log,
                        }
                    )
            else:
                table.append(
                        {
                            "单词数量": i,
                            "单词词组": w_word,
                            # "中文翻译": w_translation,
                            "正确率": rate, # 20%
                            "听写次数": w_dictate,
                            # "错误次数": w_wrong,
                            "单词分组": tags, # list
                            "单词笔记": w_note,
                            "听写趋势": w_log,
                        }
                    ) 
            i += 1
        return table

class DataEditorTemplates(TableTemplates):
    def column_config():
        column_config={
                    "听写趋势":st.column_config.AreaChartColumn(
                        "听写趋势",
                        width='medium',
                        y_min=0,
                        y_max=1,
                    ),
                    "单词数量":st.column_config.NumberColumn(
                        "单词标号",
                        # width='small',
                        disabled=True,
                    ),
                    "听写次数":st.column_config.NumberColumn(
                        "听写次数",
                        width='small',
                        disabled=True,
                    ),
                    "单词词组":st.column_config.TextColumn(
                        "单词词组",
                        width='medium',
                        disabled=True,
                    ),
                    "单词分组":st.column_config.ListColumn(
                        "其他分组",
                        width='small',
                    ),
                    "正确率":st.column_config.ProgressColumn(
                        "正确率",
                        min_value=0,
                        max_value=1
                    )
                }
        return column_config

    @classmethod
    def group_dataeditor(cls,data, key:str):
        data_editor = st.data_editor(
                data = data,
                use_container_width=True,
                height=480,
                key=key,
                column_config=cls.column_config()
                )
        return data_editor
    
    @classmethod
    def time_dataeditor(cls,data, key:str):
        time_config = cls.column_config()
        del time_config["听写次数"]
        del time_config["正确率"]
        data_editor = st.data_editor(
                data = data,
                use_container_width=True,
                height=480,
                key=key,
                column_config=time_config
                )
        return data_editor

    def check_dataeditor(data):
        data_editor = st.data_editor(
            data = data,
            use_container_width=True,
            # key='upload_df',
            column_config={
                "错误原因": st.column_config.SelectboxColumn(
                    "错误原因",
                    options=[
                        "发音", # 听错为另一个单词
                        "词形", # 拼写老是不准确
                        "生词", # 不认识，不熟悉单词
                        "英美式",
                    ]
                ),
            },
        )

        return data_editor
    
    def dictate_dataeditor(data):
        data_editor = st.data_editor(
        data=data,
        hide_index=True,
        use_container_width=True,
        key="dictate_table",
        column_config={
            "Index": st.column_config.Column(
                "Index",
                width='small',
                disabled=True,
                required=True,
            ),
            "Word": st.column_config.Column(
                "Word",
                width='large',
                required=True,
            )
        }
        )
        return data_editor
