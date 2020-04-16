
import os
from common.handle_excel import Excel_Hande
from ddt import ddt,data
import unittest
from common.heandle_path import DATA_DIR

@ddt
class Withdraw(unittest.TestCase):
    exce = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'withdraw')
    case = exce.read_excel()

    @data(*case)
    def test_withdraw(self, cas):
        print(cas)


# @ddt
# class kk(unittest.TestCase):
#     exce = Excel_Hande(os.path.join(DATA_DIR,'apicases.xlsx'),'withdraw')
#     case = exce.read_excel()
#
#     @data(*case)
#     def test_gg(self,cas):
#         print(cas)