import csv

with open('report.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    header = [['Date', 'Status']]
    csvData = [['09/03/2019', 'OK'], ['22/03/2019', 'BAD'], ['30/03/2019', 'OK'], ['24/03/2019', 'BAD']]
    writer.writerow(header)
    writer.writerow(csvData)

csvfile.close()

with open('report.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Header {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} , {row[1]} , {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')