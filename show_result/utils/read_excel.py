import csv

def read_data(file_path):
    """读取csv文件"""
    with open(file_path, 'r', encoding="gbk") as f:
        reader = csv.reader(f)

        result = list(reader)

        return result