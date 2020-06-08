import os
import csv


from common.helper import get_automatedtesting



class Csv:

    """csv文件的简易处理"""

    def __init__(self, filename):
        self.filename = self.get_true_filename(filename)

    @staticmethod
    def check_file(file):
        if not file.endswith(".csv") or not os.path.exists(file):
            file = None
        return file

    @classmethod
    def parse(cls, file, key_line=None):
        """解析csv文件"""
        # 如果为None就直接返回
        if cls.check_file(file) is None:
            return
        result = list()
        with open(file, "r+") as f:
            reader = csv.reader(f)
            for line in reader:
                if not line:
                    continue
                # key_line解析后的结果为dict
                if key_line is not None:
                    if line == reader[key_line]:
                        continue
                    data = dict()
                    for l in range(len(line)):
                        data.setdefault(reader[key_line][l], line[l])
                else:
                    data = tuple(line)
                result.append(data)
        return result

    @staticmethod
    def get_true_filename(filename):
        return os.path.join(get_automatedtesting(), filename)

    def generate(self, data):
        """生成csv文件"""
        with open(self.filename, "w+") as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def write(self, data):
        with open(self.filename, "a+") as f:
            writer = csv.writer(f)
            writer.writerow(data)

