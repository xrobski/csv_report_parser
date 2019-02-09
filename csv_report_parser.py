import csv
from pprint import pprint
from datetime import datetime
from pycountry import subdivisions


def csv_report_parser(file):
    # file open, read csv file
    with open(file, "r", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file)

        # listed data
        #TODO: czy nie ma pustych wierszy?
        rows = list(csv_reader)
        sorted_rows = sorted(rows, key=lambda x: datetime.strptime(x[0], '%m/%d/%Y'))

        output_data = []
        aggregated_data = {}
        previous_date = sorted_rows[0][0]

        for row in sorted_rows:
            current_date, city, ads, ctr = row[0], row[1], int(row[2]), row[3]
            new_day = previous_date != current_date

            if new_day:
                # Finalize previous day
                for code in sorted(aggregated_data):
                    d = datetime.strptime(previous_date, '%m/%d/%Y')
                    formatted_date = d.strftime('%Y-%m-%d')
                    aggreated_ads = aggregated_data[code][0]
                    rounded_clicks = round(aggregated_data[code][1])

                    # Push to output
                    output_data.append('{},{},{},{}'.format(formatted_date,
                                                            code,
                                                            aggreated_ads,
                                                            rounded_clicks))
                # Clean up
                aggregated_data = {}
                previous_date = current_date

            # process data
            country_code = subdivisions.lookup(city).country_code
            clicks = float(ctr[:-1]) / 100 * ads

            # aggregate data
            if country_code in aggregated_data:
                aggregated_data[country_code][0] += ads
                aggregated_data[country_code][1] += clicks
            else:
                aggregated_data[country_code] = [ads,clicks]

        pprint(output_data)

if __name__ == '__main__':
    csv_report_parser('test1.csv')
