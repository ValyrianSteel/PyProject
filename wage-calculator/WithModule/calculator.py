#!/usr/bin/env python3

import sys
import configparser
from datetime import datetime
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
    def city(self):
        return self._value_after_option('-C')

    @property
    def config_path(self):
        return self._value_after_option('-c')

    @property
    def userdata_path(self):
        return self._value_after_option('-d')

    @property
    def export_path(self):
        return self._value_after_option('-o')

args = Args()

class Config(object):

    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config = configparser.ConfigParser()
        config.read(args.config_path)
        if args.city and args.city.upper() in config.sections():
            return config[args.city.upper()]
        else:
            return config['DEFAULT']

    def _get_config(self, name):
        try:
            return float(self.config[name])
        except (ValueError, KeyError):
            print('Parameter Error')
            exit()

    @property
    def social_insurance_baseline_low(self):
        return self._get_config('JiShuL')

    @property
    def social_insurance_baseline_high(self):
        return self._get_config('JiShuH')

    @property
    def social_insurance_total_rate(self):
        return sum([
            self._get_config('YangLao'),
            self._get_config('YiLiao'),
            self._get_config('ShiYe'),
            self._get_config('GongShang'),
            self._get_config('ShengYu'),
            self._get_config('GongJiJin')
        ])

config = Config()

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
        tax_get = wageBefore - insurance - INCOME_TAX_START_POINT
        if tax_get <= 0:
            return 0
        for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
            if tax_get > item.start_point:
                tax = tax_get * item.tax_rate - item.quick_subtractor
                return tax
    def calculator(self, wageBefore, insurance, tax):
        return wageBefore - insurance - tax
    def dumptonewdata(self, userdataData, config):
        newdata = []
        for key, value in userdataData.items():
            no = key
            wageBefore = value
            JiShuL = config.social_insurance_baseline_low
            JiShuH = config.social_insurance_baseline_high
            rate = config.social_insurance_total_rate
            insurance = self.calc_insurance(wageBefore, JiShuL, JiShuH, rate)
            tax = self.calc_tax(wageBefore, insurance)
            wageAfter = self.calculator(wageBefore, insurance, tax)

            l = []
            l.append(no)
            l.append(str(wageBefore))
            l.append(str(format(insurance, ".2f")))
            l.append(str(format(tax, ".2f")))
            l.append(str(format(wageAfter, ".2f")))
            l.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            newdata.append(l)
        return newdata

queue1 = Queue()
queue2 = Queue()

def f1(userdata, userdatafile):
    userdata.set_userdata(userdatafile)
    queue1.put(userdata.get_userdata())

def f2(userdata, userdatafile, config):
    userdataData = queue1.get()
    #newdata
    newdata = userdata.dumptonewdata(userdataData, config)
    queue2.put(newdata)
    

def f3(outputfile):
    newdata = queue2.get()
    with open(outputfile, 'w') as file:
        for line in newdata:
            sep = ','
            file.write(str(sep.join(line)))
            file.write('\n')

if __name__ == '__main__':



    userdata_path = args.userdata_path
    userdata = UserData()
    userdata.set_userdata(userdata_path)

    export_path = args.export_path

    Process(target=f1, args=(userdata, userdata_path)).start()
    Process(target=f2, args=(userdata, userdata_path, config)).start()
    Process(target=f3, args=(export_path, )).start()
