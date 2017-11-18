#!/usr/bin/env python3

import sys
from multiprocessing import Process, Queue

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
    def dumptonewdata(self, config):
        newdata = []
        for key, value in self._userdata.items():
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

def f1():
    queue1.put(data)

def f2(userdata, config):
    data = queue1.get()
    #newdata
    newdata = userdata.dumptonewdata(config)
    queue2.put(newdata)
    

def f3(outputfile):
    newdata = queue2.get()
    with open(outputfile, 'w') as file:
        for line in newdata:
            for item in line:
                file.write(item)
                file.write(',')
            file.write('\n')

if __name__ == '__main__':
    args = sys.argv[1:]

    index = args.index('-c')
    config = Config(args[index+1])

    index = args.index('-d')
    userdata = UserData(args[index+1])

    index = args.index('-o')
    output = args[index+1]

    # Process(target=f1, args=(, )).start()
    Process(target=f2, args=(userdata, config)).start()
    Process(target=f3, args=(output, )).start()
