import os, json, re

class FileTool:
    @staticmethod
    def sanitize_filename(filename):
        disallowed_chars = r'[<>:"/\\|?*.]'
        sanitized_filename = re.sub(disallowed_chars, ' ', filename)
        return sanitized_filename

    # 获取桌面路径
    @staticmethod
    def get_desktop_path(filename, file_format):
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        desk_path = os.path.join(desktop_path, f"{filename}.{file_format}")
        print(f'file_path = {desk_path}')
        return desk_path

    @classmethod
    def save_file(cls, content, filename, file_format, folder_path="desktop"):
        # 写入文件
        def saving(path, content):
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"文件已保存到: {path}")

        if folder_path == 'desktop':
            desk_path = cls.get_desktop_path(filename, file_format)
            saving(desk_path, content)
        else:
            os.makedirs(folder_path, exist_ok=True)
            folder_path = folder_path + '/' + filename + '.' + file_format
            try:
                saving(folder_path, content)
            except:
                print('🔴failed')

    @classmethod
    def save_as_json(cls, content, filename, file_format, folder_path="desktop"):
        try:
            json_content = json.dumps(content)
            cls.save_file(json_content, filename, file_format, folder_path)
        except:
            print('🔴json saving is failed')

    @ staticmethod
    def file_reader(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content


class FileForWords(FileTool):

    @classmethod
    def save_html(cls,times:int, words:list):
        body = []
        # print(f"🌱words={words}")
        a = 1
        for word in words:
            note = f"<p>{a} words</p>"
            if a % 25 == 0 and a // 25 > 0:
                body.append(note)
            word_html = f"<p>{word}</p>"
            for i in range(times):
                body.append(word_html)
            a += 1
        body_html = ''.join(body)
        html_content = f'''
<html>
<head></head>
<body>
{body_html}
</body>
</html>
'''
        filename = f"{words[0]}_{words[-1:][0]}"
        cls.save_file(
            content=html_content,
            filename=filename,
            file_format='html'
        )
        return filename


if __name__ == '__main__':
    content = "<html><body><h1>Hello, world!</h1></body></html>"
    filename = "example"
    file_format = "html"
    FileTool.save_file(content, filename, file_format)
