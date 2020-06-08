import os
import xlrd
import xlwt


__author__ = "Jackey"



def check_file(file):
    """检查excel的文件名及是否存在这个文件"""
    if not isinstance(file, str):
        return
    if not os.path.exists(file):
        if file.endswith("xls"):
            file += "x"
        elif file.endswith("xlsx"):
            file = file[:-1]
        else:
            pass
    return file if os.path.exists(file) else None


class Excel:

    """
    自动化将通过excel表来控制, 
    目前暂未支持, 将在后续版本增加
    也存在转用csv的可能
    """

    @staticmethod
    def parse(file):
        """
        excel表的解析
        return格式:
            [
                (),
                (),
                ...
            ]
        """
        file = check_file(file)
        # 如果是不存在的文件, 就无需再执行下去了
        if file is None:
            return

        workbook = xlrd.open_workbook(file)
        # 只读取第一个sheet
        sheetname = workbook.sheet_names()[0]
        sheet = workbook.sheet_by_name(sheetname)
        result = list()
        # 处据数据成期望的格式
        for row in range(sheet.nrows):
            if not row:
                continue
            data = list()
            for value in sheet.row_values(row):
                if value == 0.0:
                    # 如果是0.0的float, 直接计成0
                    data.append(0)
                elif value:
                    data.append(value)
                else:
                    pass
            result.append(tuple(data))
        return result

    @staticmethod
    def generate(file, data):
        """根据data生成excel"""
        workbook = xlwt.Workbook(encoding="utf-8")
        sheet = workbook.add_sheet("sheet")
        for row, value in enumerate(data):
            for i, v in enumerate(value):
                sheet.write(row, i, v)
        workbook.save(file)
