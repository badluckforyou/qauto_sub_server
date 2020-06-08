

from common.record import Record
from common.excel import Excel
from platforms.android.methods import Methods
from platforms.identifier import AndroidSession


@Record.finish
def run(excel):
    if excel:
        steps = Excel.parse(excel)
    # 执行行为方法前先连接手机
    AndroidSession.connect()
    m = Methods()