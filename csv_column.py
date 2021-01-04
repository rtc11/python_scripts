#!/usr/bin/env python3
"""Get requested columns from CSV

Prequesite: pandas installed with python3,
e.g docker pull amancevice/pandas:alpine

usage: csv_column.py -c <column> -e -i <inputfile> -o <outputfile>
-c <column to keep> : collumn to keep e.g. -c CVSSv2_Severity -c CWE
-e : exclude header
-i <input-file> : input csv file. e.g /path/input.csv
-o <output-file>: output csv file. e.g /path/output.csv

"""

# python3 csv_column.py -e -i dependency-check-report.csv -o result.csv -c CVSSv2_Severity -c CWE

import sys, getopt
import pandas as pd

def writeColumnsToFile(inputFile, outputFile, culumnsToCopy, includeHeader):
    print("\nColumns:\t" + ", ".join(culumnsToCopy))
    print("Input:\t\t" + inputFile)
    print("Output:\t\t" + outputFile)
    print("Include Header:\t" + str(includeHeader))

    # data = pd.read_csv(inputFile, sep=',', usecols=['CWE', 'CVSSv2_Severity'])
    data = pd.read_csv(inputFile, sep=',', usecols=culumnsToCopy)
    data[culumnsToCopy]
    data.to_csv(outputFile, sep=',', header=includeHeader, index=False)
    print("")

def main(argv):
    inputFile = ''
    outputFile = ''
    culumnsToCopy = []
    includeHeader = True

    try:
        opts, args = getopt.getopt(argv,"hi:o:ec:")
    except getopt.GetoptError:
        print("usage: csv_column.py -c <column> -e -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("usage: csv_column.py -c <column> -e -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt == '-i':
            inputFile = arg
        elif opt == '-o':
            outputFile = arg
        elif opt == '-e':
            includeHeader = False
        elif opt == '-c':
            culumnsToCopy.append(arg)

    writeColumnsToFile(inputFile, outputFile, culumnsToCopy, includeHeader)

if __name__ == "__main__":
   main(sys.argv[1:])
