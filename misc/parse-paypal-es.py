#!/usr/bin/env python

import sys
import re
import csv
import datetime

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [cell for cell in row]

if len(sys.argv) != 3:
    print("Usage parse-paypal-es.py <paypal csv file> <qbo csv file>")
    sys.exit(-1)

try:
    fp = open(sys.argv[1], "r")
except IOError:
    print("Cannot open input file %s" % sys.argv[1])
    sys.exit(0)

try:
    _out = open(sys.argv[2], "w")
except IOError:
    print("Cannot open output file %s" % sys.argv[2])
    sys.exit(0)


out = csv.writer(_out, quoting=csv.QUOTE_MINIMAL)
out.writerow(["Date","Description","Amount"])

reader = unicode_csv_reader(fp)
index = 0
for fields in reader:
    if not index:
        index = 1
        continue

    desc = fields[3]
    dat = fields[0]
    dat = datetime.datetime.strptime(dat, '%d/%m/%Y').strftime('%m/%d/%Y')
    amount = fields[7]
    amount = amount.replace(",", ".")
    type = fields[4]
    status = fields[5]
    if status != 'Completed':
        continue

    if type.find("Account Hold") >= 0:
        continue

    out.writerow([dat, desc, amount])

    fee = fields[8]
    fee = fee.replace(",", ".")
    if fee and float(fee) != 0.0:
        out.writerow([dat, "PayPal fee", fee])

fp.close()
_out.close()
