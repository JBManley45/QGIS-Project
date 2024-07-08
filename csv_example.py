import csv

def load_data(filename):
    mylist = []
    with open(filename) as numbers:
        numbers_data = csv.reader(numbers, delimiter=',')
        next(numbers_data) #skip header
        for row in numbers_data:
            mylist.append(row)
        return mylist
        
data = load_data('C:\\CODE\\Input\\TEST.csv')
print(data)