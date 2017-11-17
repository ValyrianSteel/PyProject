#!/usr/bin/env python3

import sys

def calcSocial(wage):
    return wage*0.165

def calcTax(wage, social):
    tax_get = wage - social - 3500
    
    if tax_get <= 0:
        return 0
    elif 0 < tax_get <= 1500:
        return tax_get*0.03 - 0
    elif 1500 < tax_get <= 4500:
        return tax_get*0.1 - 105
    elif 4500 < tax_get <= 9000:
        return tax_get*0.2 - 555
    elif 9000 < tax_get <= 35000:
        return tax_get*0.25 - 1005
    elif 35000 < tax_get <= 55000:
        return tax_get*0.3 - 2755
    elif 55000 < tax_get <= 80000:
        return tax_get*0.35 - 5505
    elif 80000 < tax_get:
        return tax_get*0.45 - 13505


if __name__ == "__main__":
    wage = 0
    try:
        for arg in sys.argv[1:]:
            no, wage = arg.split(':')

            try:
                wage = int(wage)
            except:
                print("Parameter Error")


            social = calcSocial(wage)
            tax = calcTax(wage, social)

            pay = wage - social - tax
            print(no, format(pay, ".2f"), sep=':')
    except:
        print("Calculate Error")
