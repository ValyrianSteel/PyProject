#!/usr/bin/env python3

import sys
from collections import namedtuple
from multiprocessing import Process, Queue

IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
)

INCOME_TAX_START_POINT = 3500

INCOME_TAX_QUICK_LOOKUP_TABLE = [
    IncomeTaxQuickLookupItem(80000, 0.45, 13505),
    IncomeTaxQuickLookupItem(55000, 0.35, 5505),
    IncomeTaxQuickLookupItem(35000, 0.30, 2755),
    IncomeTaxQuickLookupItem(9000,  0.25, 1005),
    IncomeTaxQuickLookupItem(4500,  0.20, 555),
    IncomeTaxQuickLookupItem(1500,  0.10, 105),
    IncomeTaxQuickLookupItem(0,     0.03, 0)
]

class Args(object):

    def __init__(self):
        self.args = sys.argv[1:]

    def _value_after_option(self, option):
        try:
            index = self.args.index(option)
            return self.args[index + 1]
        except(ValueError, IndexError):
            print('Parameter Error')
            exit()

    @property
    def config_path(self):
        return self._value_after_option('-c')

    @property
    def userdata_path(self):
        return self._value_after_option('-d')

    @property
    def export_path(self):
        return self._value_after_option('-o')


class Config(object):
    def __init__(self):
        self._config = {}
    def set_config(self, configfile):
        with open(configfile, 'r') as file:
        	for line in file:
        		l = line.strip().replace(' ', '').split('=')
        		self._config[l[0]] = float(l[1])
    def get_configdata(self):
        return self._config
    def get_config(self, item):
        if 'JiShuH' == item:
            return self._config['JiShuH']
        elif 'JiShuL' == item:
            return self._config['JiShuL']
        else:
            return 0
    def get_rate(self):
        return self._config['YangLao'] + \
                self._config['YiLiao'] + \
                self._config['ShiYe'] + \
                self._config['GongShang'] + \
                self._config['ShengYu'] + \
                self._config['GongJiJin']

class UserData(object):
    def __init__(self):
        self._userdata = {}
    def set_userdata(self, userdatafile):
        with open(userdatafile, 'r') as file:
        	for line in file:
        		l = line.strip().split(',')
        		self._userdata[l[0]] = int(l[1])
    def get_userdata(self):
        return self._userdata
    def calc_insurance(self, wageBefore, JiShuL, JiShuH, rate):
        if wageBefore < JiShuL:
            return JiShuL * rate
        elif wageBefore > JiShuH:
            return JiShuH * rate
        else:
            return wageBefore * rate
    def calc_tax(self, wageBefore, insurance):
        tax_get = wageBefore - insurance - 3500
        if tax_get <= 0:
            return 0
        elif 0 < tax_get <= 1500:
            return tax_get * 0.03 - 0
        elif 1500 < tax_get <= 4500:
            return tax_get * 0.1 - 105
        elif 4500 < tax_get <= 9000:
            return tax_get * 0.2 - 555
        elif 9000 < tax_get <= 35000:
            return tax_get * 0.25 - 1005
        elif 35000 < tax_get <= 55000:
            return tax_get * 0.3 - 2755
        elif 55000 < tax_get <= 80000:
            return tax_get * 0.35 - 5505
        elif 80000 < tax_get:
            return tax_get * 0.45 - 13505
    def calculator(self, wageBefore, insurance, tax):
        return wageBefore - insurance - tax
    def dumptonewdata(self, userdataData, config):
        newdata = []
        for key, value in userdataData.items():
            no = key
            wageBefore = value
            JiShuL = config.get_config('JiShuL')
            JiShuH = config.get_config('JiShuH')
            rate = config.get_rate()
            insurance = self.calc_insurance(wageBefore, JiShuL, JiShuH, rate)
            tax = self.calc_tax(wageBefore, insurance)
            wageAfter = self.calculator(wageBefore, insurance, tax)

            l = []
            l.append(no)
            l.append(str(wageBefore))
            l.append(str(format(insurance, ".2f")))
            l.append(str(format(tax, ".2f")))
            l.append(str(format(wageAfter, ".2f")))

            newdata.append(l)
        return newdata

queue1 = Queue()
queue2 = Queue()

def f1(userdata, userdatafile):
    userdata.set_userdata(userdatafile)
    queue1.put(userdata.get_userdata())

def f2(userdata, userdatafile, config):
    userdataData = queue1.get(timeout=1)
    #newdata
    newdata = userdata.dumptonewdata(userdataData, config)
    queue2.put(newdata)
    

def f3(outputfile):
    newdata = queue2.get(timeout=1)
    with open(outputfile, 'w') as file:
        for line in newdata:
            sep = ','
            file.write(str(sep.join(line)))
            file.write('\n')

if __name__ == '__main__':
    args = Args()
    
    config_path = args.config_path
    config = Config()
    config.set_config(config_path)

    userdata_path = args.userdata_path
    userdata = UserData()
    userdata.set_userdata(userdata_path)

    export_path = args.export_path

    Process(target=f1, args=(userdata, userdata_path)).start()
    Process(target=f2, args=(userdata, userdata_path, config)).start()
    Process(target=f3, args=(export_path, )).start()
