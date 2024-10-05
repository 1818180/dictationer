import re
# from pypinyin import pinyin, lazy_pinyin
import locale

class DataProcessor:

    def list_process(str_list:list[str]):
        # 去空‘’，去空格，去重复
        str_list = [item for item in str_list if item != '']
        for s in str_list:
            s = s.strip()
        unique_set = set(str_list)
        str_list = list(unique_set)
        return str_list

    def remove_common_elements(del_list:list, aim_list:list):
        result = [item for item in del_list if item not in aim_list]
        return result
    
    def times_2number(times:str, list_time:bool = False):
        match = re.search(r'听写次数(\d+)，错误次数(\d+)', times)
        dictate_time = int(match.group(1))
        error_time = int(match.group(2))
        if list_time is True:
            return [dictate_time,error_time]
        else:
            return dictate_time,error_time
    
    # 将字符串数字，分解为整数列表 '1234' -> [1,2,3,4]
    # 将log转换为趋势图
    def str_number_2list(number_str:str):
        number = [int(char) for char in number_str]
        trend = []
        socre = 0
        for num in number:
            if num == 0:
                socre -= 1
            elif num == 1:
                socre += 1
            trend.append(socre)
        return trend

    @classmethod
    def list_str_order(cls,mixed_list:list[str]):
        sorted_mixed_list = sorted(mixed_list)
        return sorted_mixed_list
    

if __name__ == "__main__":
    numbers = '001110111'
    mixed_list = ["3.3-1", "4.1-9", "3.2-3", "apple", "香蕉", "30", "cherry", "4", "苹果"]
    # trends = DataProcessor.str_number_2list(numbers)
    # print(trends)
    sorted_mixed_list = DataProcessor.list_str_order(mixed_list)
    print(sorted_mixed_list)  # 输出按自定义规则排序的结果