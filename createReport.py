import csv
from monitorAndNotify import Data
from monitorAndNotify import Database
from virtual_sense_hat import VirtualSenseHat

CONFIG_FILE = "config.json"

class CSVreport:
    pass
            

def main():
    """
    Main Method
    """
    database = Database()
    dataread = database.read_data()
    sense = VirtualSenseHat.getSenseHat()
    data = Data(sense, CONFIG_FILE)
    
    result = []
    for d in dataread:
        result.append([d[0], d[1], d[2]])

    csvdata = []
    temp_min, temp_max, humid_min, humid_max = data.read_config()
    print(result)
    for r in result:
        while (r[2] != r[2]):
            date = r[2].strftime('%d/%m/%Y')
            if(data.data_out_of_range(r[0], r[1])):
                status = "OK"
                #csvdata.append([date, status])
            else:
                if(r[0]< temp_min):
                    status = "BAD: %s below minimum temperature" %round((temp_min-r[0]), 1)
                if(r[0]> temp_max):
                    status = "BAD: %s over maximum temperature" %round((r[0]-temp_max), 1)
                if(r[1]< humid_min):
                    status = "BAD: %s below minimum humidity" %round((humid_min-r[1]), 1)
                if(r[1]< humid_max):
                    status = "BAD: %s over maximum humidity" %round((r[1]-humid_max), 1)
            print(date,status)
            csvdata.append([date, status])
        print(csvdata)
    
    with open('report.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        header = ['Date', 'Status']
        writer.writerow(header)
        for data in csvdata:
            writer.writerow(data)
    csvfile.close()


if __name__ == "__main__":
    main()
