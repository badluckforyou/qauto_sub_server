

from common.record import Record
from common.excel import Excel
from platforms.android.methods import Methods
from platforms.identifier import ExecutablePath


@Record.finish
def run(excel):
    if excel:
        steps = Excel.parse(excel)
    m = Methods()
    m.example_of_open_baidu()