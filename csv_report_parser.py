import csv
from datetime import datetime
from pycountry import subdivisions


def csv_report_parser(file):
    """ Return converted csv file to following format:
     date (YYYY-MM-DD),three letter country code (or XXX for unknown states),
     number of impressions, number ofclicks (rounded, assuming the CTR is exact)
     Rows are sorted lexicographically by date followed by the country code.
     """
    # File open, read csv file
    with open(file, "r", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = [line for line in csv_reader if line]
        sorted_rows = sorted(rows, key=lambda x: datetime.strptime(x[0], '%m/%d/%Y'))

    output_data = []
    aggregated_data = {}
    # Set default date
    previous_date = sorted_rows[0][0]

    for row in sorted_rows:
        # Read data from row
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
            # Clean up aggregated data
            aggregated_data = {}
            # Reset to new date
            previous_date = current_date

        # Process data
        try:
            country_code = subdivisions.lookup(city).country_code
        except LookupError:
            country_code = "XXX"

        clicks = float(ctr[:-1]) / 100 * ads

        # Aggregate data
        if country_code in aggregated_data:
            aggregated_data[country_code][0] += ads
            aggregated_data[country_code][1] += clicks
        else:
            aggregated_data[country_code] = [ads,clicks]

    # Save output to file
    with open("output.csv", "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for row in output_data:
            writer.writerow([row])
