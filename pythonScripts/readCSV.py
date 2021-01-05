import csv

class readTimestampCSV:
    def __init__(self):
        self.data = []
        with open('Participant and Computer Timestamp Info.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    self.data.append([row[0], float(row[1]), float(row[2]), float(row[3])])
                    line_count += 1

    def getFolderInfo(self, name):
        for item in self.data:
            if name == item[0]:
                return [item[1], item[2], item[3]]
        return []