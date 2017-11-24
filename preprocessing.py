#!/usr/bin/python3

import csv
import datetime
import glob
import re
import sys


LOOK_BACK = [1, 3, 6]
VALUE_COLS = ["Temperature", "Noise", "Count", "Direction", "Speed"]
VALUE_COLS_RE = re.compile("(" + "|".join(VALUE_COLS) + ")$")
STUDENTS_COUNT_RE = re.compile("Students.*Count$")
BIRDS_COUNT_RE = re.compile("Birds.*Count$")


def loadData(fName, dataCols):
    fh = open(fName, newline='')
    reader = csv.DictReader(fh)

    result = []

    for row in reader:
        proc = {
            'TS': row['TS'],
            'INDEX': len(result)
        }
        for colName in dataCols:
            if colName in row:
                k = row['Name'] + "-" + colName
                proc[k] = float(row[colName])

        result.append(proc)
    return result


def saveData(fName, data):
    with open(fName, 'w') as csvFile:
        values = list(data.values())
        fieldNames = (
            ['TS'] +
            sorted(list(values[len(values) - 1].keys()))
        )
        writer = csv.DictWriter(
            csvFile,
            fieldnames=fieldNames
        )

        writer.writeheader()
        for vals in values:
            writer.writerow(vals)


combinedData = {}

for fName in glob.glob("data/data*.csv"):
    singleData = loadData(
        fName,
        VALUE_COLS
    )

    # Toto funguje jen proto, ze jsou ty data kompletni
    # V realnem pripade je potreba spojovat data na zaklade
    # casobeho razitka + nejake tolerance okolo
    if len(combinedData) == 0:
        for v in singleData:
            combinedData[v['INDEX']] = {}

    for vals in singleData:
        i = vals['INDEX']
        for k, v in vals.items():
            combinedData[i][k] = v

saveData("preprocessed/just-merged.csv", combinedData)

keys = list(combinedData[0].keys()) + \
    ["D_StudentsTotal-Count", "D_BirdsTotal-Count"]

for i in range(len(combinedData)):
    rec = combinedData[i]
    sTotalC = 0
    bTotalC = 0

    for k in keys:
        if k in ["D_StudentsTotal-Count", "D_BirdsTotal-Count"]:
            continue
        if STUDENTS_COUNT_RE.search(k) is not None:
            sTotalC += rec[k]
        if BIRDS_COUNT_RE.search(k) is not None:
            bTotalC += rec[k]

    rec['D_StudentsTotal-Count'] = sTotalC
    rec['D_BirdsTotal-Count'] = bTotalC
    dt = datetime.datetime.strptime(rec['TS'], "%Y-%m-%d %H:%M:%S")

    d = ((int(dt.strftime("%w")) + 6) % 7)
    h = int(dt.strftime("%H"))

    rec['D_DayOfWeek'] = ["Po", "Ut", "St", "Ct", "Pa", "So", "Ne"][d]
    rec['D_HourOfDay'] = str(h) + "h"
    rec['D_DayHour'] = rec['D_DayOfWeek'] + "-" + rec['D_HourOfDay']

    for b in LOOK_BACK:
        if i >= b:
            for k in keys:
                if VALUE_COLS_RE.search(k) is not None:
                    rec["D-" + k + "-" + str(b)] = (
                        rec[k] - combinedData[i - b][k]
                    )

saveData("preprocessed/with-derived.csv", combinedData)
