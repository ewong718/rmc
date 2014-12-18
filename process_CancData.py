'''
Created on Dec 18, 2014

@author: Edmund Wong
'''

import sys
import csv
import getopt
from datetime import time, datetime


def main():

    opts, unused = getopt.getopt(sys.argv[1:], "hi:o:")
    for option, value in opts:
        if option in ("-i"):
            inputFile = value
        if option in ("-o"):
            outputdir = value

    rawCsvData = []

    with open(inputFile, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        next(iter(csvreader))
        for row in csvreader:
            rawCsvData.append(row)

    time_int = [[time(8, 0), time(8, 15)],
                [time(8, 15), time(8, 30)],
                [time(8, 30), time(8, 45)],
                [time(8, 45), time(9, 0)],
                [time(9, 0), time(9, 15)],
                [time(9, 15), time(9, 30)],
                [time(9, 30), time(9, 45)],
                [time(9, 45), time(10, 0)],
                [time(10, 0), time(10, 15)],
                [time(10, 15), time(10, 30)],
                [time(10, 30), time(10, 45)],
                [time(10, 45), time(11, 0)],
                [time(11, 0), time(11, 15)],
                [time(11, 15), time(11, 30)],
                [time(11, 30), time(11, 45)],
                [time(11, 45), time(12, 0)],
                [time(12, 0), time(12, 15)],
                [time(12, 15), time(12, 30)],
                [time(12, 30), time(12, 45)],
                [time(12, 45), time(13, 0)],
                [time(13, 0), time(13, 15)],
                [time(13, 15), time(13, 30)],
                [time(13, 30), time(13, 45)],
                [time(13, 45), time(14, 0)],
                [time(14, 0), time(14, 15)],
                [time(14, 15), time(14, 30)],
                [time(14, 30), time(14, 45)],
                [time(14, 45), time(15, 0)],
                [time(15, 0), time(15, 15)],
                [time(15, 15), time(15, 30)],
                [time(15, 30), time(15, 45)],
                [time(15, 45), time(16, 0)],
                [time(16, 0), time(16, 15)],
                [time(16, 15), time(16, 30)],
                [time(16, 30), time(16, 45)],
                [time(16, 45), time(17, 0)]]

    for idx, val in enumerate(rawCsvData):
        # cast resource id into ints
        rawCsvData[idx][0] = int(val[0])
        # cast scandates and times into date/time objects
        rawCsvData[idx][1] = datetime.strptime(val[1], '%Y-%m-%d').date()
        rawCsvData[idx][2] = datetime.strptime(val[2], '%H:%M:%S').time()
        rawCsvData[idx][3] = datetime.strptime(val[3], '%H:%M:%S').time()

    for resource_id in range(1, 4):
        # Filters for resource-specific scans
        data_spec = []
        for row in rawCsvData:
            if row[0] == resource_id:
                data_spec.append(row)

        datelist = []
        for idx, val in enumerate(data_spec):
            datelist.append(data_spec[idx][1])
        datelist = sorted(set(datelist))

        output = [["Date(Weekdays)", "Total minutes with at least one cancellation without replacement"]]
        for scandate in datelist:
            # not count weekends
            if (scandate.weekday() == 5) or (scandate.weekday() == 6):
                continue
            date_booking_times = []
            for idx, bookings in enumerate(data_spec):
                if scandate == bookings[1]:
                    date_booking_times.append(bookings)
            total_minutes_cancelled = 0
            for gap in time_int:
                bad_cancel = 0
                for single_booking in date_booking_times:
                    if (gap[0] >= single_booking[2]) and (gap[1] <= single_booking[3]) and (single_booking[4] == 'CANCELLED'):
                        bad_cancel = 1
                    if (gap[0] >= single_booking[2]) and (gap[1] <= single_booking[3]) and (single_booking[4] == 'APPROVED'):
                        bad_cancel = 0
                        break
                if bad_cancel == 1:
                    total_minutes_cancelled = total_minutes_cancelled + 15
            row = [scandate.strftime("%Y-%m-%d"), total_minutes_cancelled]
            output.append(row)

        with open(outputdir + '/cancel_data' + str(resource_id) + '.csv', 'wb') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(output)


if __name__ == "__main__":
    sys.exit(main())
