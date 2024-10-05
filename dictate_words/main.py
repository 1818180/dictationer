import streamlit as st
import hydralit_components as hc
import playsound as ps

from sort_tool.input import InputWords
from sort_tool.output import OutputData
from sort_tool.table_templates import TableTemplates,DataEditorTemplates
from sort_tool.file_handle import FileForWords
from sort_tool.data_process import DataProcessor

st.set_page_config(
    page_title="Dictationer",
    page_icon="✍",
    layout="wide",
)

def state_initialize(key, value):
    if key not in st.session_state:
        st.session_state[key] = value
    else:
        pass

def state_update(key, value):
    st.session_state[key] = value

state_initialize('all_words', len(OutputData.get_all_words()))
state_initialize('dictate_1_number', len(OutputData.get_timed_words_detail(dictate_time='>= 1')))
state_initialize('dictate_2_number', len(OutputData.get_timed_words_detail(dictate_time='>= 2')))
state_initialize('group_names', OutputData.get_groups_names())
state_initialize('timed_words', [])
state_initialize('grouped_words', [])
state_initialize('diy_words', [])
state_initialize('select_words', [])
state_initialize('dictate_words', [])
state_initialize('unchecked_words', [])
state_initialize('checked_df', [])
ps.playsound(r"assets\sound\button_click_bright.mp3")
def upload_words():
    numbers = InputWords.save_new_words(words=st.session_state.new_words,group_name=st.session_state.group_name)
    st.toast(f"已经存入{numbers}个单词",icon="✔")
    ps.playsound(r"assets\sound\ui_notification_classic_bell.mp3")
    st.session_state.new_words = ''
    st.session_state.group_name = ''

def save_material(times):
    file_name = FileForWords.save_html(times=times,words=[word[1] for word in st.session_state.dictate_words])
    st.toast(f"文件{file_name}已经下载至桌面")
    ps.playsound(r"assets\sound\ui_notification_classic_bell.mp3")

def download_dictate_audio(repeat_times):
    ps.playsound(r"assets\sound\button_click_bright.mp3")
    start_num = st.session_state.dictate_numbers[0] - 1
    end_num = st.session_state.dictate_numbers[1]
    st.session_state.dictate_words = st.session_state.select_words[start_num:end_num]
    if repeat_times == '':
        repeat_times = 3
    save_material(int(repeat_times))

def dictate_with_translation():
    pass

# override_theme = {'progress_color': '#D0F5DE'}
with st.sidebar:
    st.header("听写进度")
    complete_percent = st.session_state.dictate_1_number / st.session_state.all_words * 100
    complete_percent_2 = st.session_state.dictate_2_number / st.session_state.all_words * 100
    complete_number = f"听写一次完成度：{st.session_state.dictate_1_number} / {st.session_state.all_words}"
    complete_number_2 = f"听写两次完成度：{st.session_state.dictate_2_number} / {st.session_state.all_words}"
    hc.progress_bar(complete_percent,complete_number)
    hc.progress_bar(complete_percent_2,complete_number_2)
    # complete_percent
    # complete_number
    st.divider()
    add_words_pop = st.popover(
        "导入听写单词",
        use_container_width=True
    )

with add_words_pop:
    st.subheader('导入单词 📍')
    st.text_area(
        label="拷贝单词至这里，格式为一个单词一行",
        placeholder='''word1\nword2\n...''',
        height=200,
        key='new_words',
    )
    st.text_input(
        label="单词组名称",
        key="group_name",
        placeholder="可有可无"
    )
    st.button(
        label="上传单词",
        on_click=lambda :upload_words(),
        type='primary')

# 主页 HOME PAGE
st.header("筛选听写单词")
setting1, buff, dictate2 = st.columns([1.5,0.1,0.6])

with setting1:
    # st.session_state.group_names
    tab1, tab2, tab3 = st.tabs(["单词本查看","听写次数查看","自定义导入"])
    with tab1:
        if st.session_state.group_names:
            st.selectbox(
                label="选择单词分组",
                options=tuple(st.session_state.group_names),
                key='select_group',
                index=0,
            )
            st.session_state.grouped_words=OutputData.get_grouped_words(tag=st.session_state.select_group,detail=True)
            group_data = DataEditorTemplates.show_detailed_info(st.session_state.grouped_words,group=st.session_state.select_group)
            DataEditorTemplates.group_dataeditor(group_data,key="group_dataeditor1")
            # st.session_state.group_dataeditor1
            # st.button(
            #     "删除单词本",
            #     on_click=lambda :InputWords.deletwords(OutputData.get_grouped_words(tag=st.session_state.select_group))
            # )

    with tab2:
        if st.session_state.all_words > 0:
            st.selectbox(
                "选择听写次数及错误情况",
                OutputData.words_times_options(),
                index=0,
                key="select_time"
            )
            st.session_state.timed_words=OutputData.get_timed_words(st.session_state.select_time,detail=True)
            time_data = DataEditorTemplates.show_detailed_info(
                st.session_state.timed_words,
                times=DataProcessor.times_2number(
                    times=st.session_state.select_time,
                    list_time=True)
                )
            DataEditorTemplates.time_dataeditor(data=time_data,key="time_dataeditor1")

    with tab3:
        st.text_area(
            "自定义听写单词，格式为一个单词一行",
            key="diy_words_str",
            height=500,
            placeholder='''word1\nword2\n...''',
        )

with dictate2:
    with st.container(border=True):
        st.radio(
            "选择听写单词来源",
            ["单词本", "错误次数", "自己导入"],
            captions=["听写单词本里的单词","按照听写次数和错误次数选择单词","听写自己导入的单词"],
            key='dictate_mood'
        )
        st.divider()
        # 选择听写单词的来源，是在OutputData.get_grouped_words里，与表格里的改动无关
        if st.session_state.dictate_mood == '单词本':
            st.session_state.select_words = st.session_state.grouped_words
        if st.session_state.dictate_mood == '错误次数':
            st.session_state.select_words = st.session_state.timed_words
        if st.session_state.dictate_mood == '自己导入':
            if st.session_state.diy_words_str:
                st.session_state.diy_words = InputWords.listed_words(st.session_state.diy_words_str)
                st.session_state.select_words = st.session_state.diy_words
        if len(st.session_state.select_words) > 1:
            st.select_slider(
                "选择听写范围",
                options=list(range(1, len(st.session_state.select_words) + 1)),
                value=[1,2],
                key="dictate_numbers"
            )
        repeat_times = st.text_input(
            "听写重复次数",
            placeholder="默认重复3次"
        )
        st.button(
            "音频听写",
            on_click = lambda :download_dictate_audio(repeat_times),
            type='primary'
        )
        st.button(
            "中文默写",
            on_click = lambda :dictate_with_translation(),
            type='primary'
        )
st.divider()

def check_words():
    unchecked_words = st.session_state.unchecked_words, # 自己听写单词的列表
    dictate_words = [word[1] for word in st.session_state.dictate_words] # 正确单词的详细列表转换为单词列表
    checked_df = TableTemplates.checked_table(
        unchecked_words,
        dictate_words
    )
    ps.playsound(r"assets\sound\ui_chime_tone.mp3")
    st.session_state.checked_df = checked_df
    state_update('all_words', len(OutputData.get_all_words()))
    state_update('dictate_1_number', len(OutputData.get_timed_words_detail(dictate_time='>= 1')))
    state_update('group_names', OutputData.get_groups_names())

def upload_checked(checked_df):
    InputWords.checked_in(checked_df)
    st.toast("已提交成功！")
    ps.playsound(r"assets\sound\ui_notification_classic_bell.mp3")
    st.session_state.dictate_words = None
    st.session_state.checked_df = None

if st.session_state.dictate_words:
    st.header("听写单词")
    DataEditorTemplates.dictate_dataeditor(TableTemplates.dictate_table(st.session_state.dictate_words))
    uncheckeds = [ word['Word'] for word in list(st.session_state.dictate_table['edited_rows'].values())]
    st.session_state.unchecked_words = uncheckeds
    st.button(
        "检查 ✔",
        type='primary',
        on_click=lambda : check_words()
    )
    if st.session_state.checked_df:
        upload_df = DataEditorTemplates.check_dataeditor(st.session_state.checked_df)
        st.button(
            "提交至单词库",
            type='primary',
            on_click=lambda :upload_checked(upload_df)
        )
