@echo off
REM 激活虚拟环境
call C:\FYB\python_relate\python_env\streamlit_env\Scripts\activate.bat

REM 确保虚拟环境激活后使用 streamlit 运行 main.py 文件
call streamlit run C:\FYB\dictate_words\main.py

REM 保持窗口打开，方便查看输出或错误信息
pause
