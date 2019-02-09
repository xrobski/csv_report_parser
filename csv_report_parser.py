import csv
from pprint import pprint
from datetime import datetime
from pycountry import subdivisions


def csv_report_parser(file):
    # output variables
    csv_output = []
    work_output = {}

    # file open, read csv file
    with open(file, "r", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file)

        # listed data
        #TODO: czy nie ma pustych wierszy?
        rows = list(csv_reader)

        # sort file
        sorted_rows = sorted(rows, key=lambda x: datetime.strptime(x[0], '%m/%d/%Y'))

        current_day = sorted_rows[0][0]
        for row in sorted_rows:
            date, city, ads, ctr = row[0], row[1], row[2], row[3]
            #if current_day = date:
            print(date, city, ads, ctr)


if __name__ == '__main__':
    csv_report_parser('test1.csv')
