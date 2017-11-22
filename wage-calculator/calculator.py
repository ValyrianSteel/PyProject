#!/usr/bin/env python3

import sys
from collections import namedtuple

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
    def __init__(self, configfile):
        self._config = {}
        with open(configfile, 'r') as file:
        	for line in file:
        		l = line.strip().replace(' ', '').split('=')
        		self._config[l[0]] = float(l[1])
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
    def __init__(self, userdatafile):
        self._userdata = {}
        with open(userdatafile, 'r') as file:
        	for line in file:
        		l = line.strip().split(',')
        		self._userdata[l[0]] = float(l[1])
    def calc_insurance(self, wageBefore, JiShuL, JiShuH, rate):
        if wageBefore < JiShuL:
            return JiShuL * rate
        elif wageBefore > JiShuH:
            return JiShuH * rate
        else:
            return wageBefore * rate
    def calc_tax(self, wageBefore, insurance):
        tax_get = wageBefore - insurance - INCOME_TAX_START_POINT
        if tax_get <= 0:
            return 0
        for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
            if item.start_point < tax_get:
                tax = tax_get * item.tax_rate - item.quick_subtractor
                return tax
    def calculator(self, wageBefore, insurance, tax):
        return wageBefore - insurance - tax
    def dumptofile(self, outputfile, config):
    	with open(outputfile, 'w') as file:
            for key, value in self._userdata.items():
                no = key
                wageBefore = value
                JiShuL = config.get_config('JiShuL')
                JiShuH = config.get_config('JiShuH')
                rate = config.get_rate()
                insurance = self.calc_insurance(wageBefore, JiShuL, JiShuH, rate)
                tax = self.calc_tax(wageBefore, insurance)
                wageAfter = self.calculator(wageBefore, insurance, tax)
           
                file.write(no)
                file.write(',')
                file.write(str(wageBefore))
                file.write(',')
                file.write(str(format(insurance, ".2f")))
                file.write(',')
                file.write(str(format(tax, ".2f")))
                file.write(',')
                file.write(str(format(wageAfter, ".2f")))
                file.write('\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Parameter Error")
        exit(-1)

    args = Args()
    
    config_path = args.config_path
    config = Config(config_path)

    userdata_path = args.userdata_path
    userdata = UserData(userdata_path)

    export_path = args.export_path

    userdata.dumptofile(export_path, config)
