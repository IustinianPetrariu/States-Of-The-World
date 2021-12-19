import os
import csv
import re

def main():
   pass
# nr2 = '31.822.848'
# nr1 = '1.2313 21312'
# nr1 = re.sub(r"(\.|,| )", "", nr2)
# print(nr1)

csv_file = "crawler/Content/data.csv"
with open(csv_file,encoding='UTF8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    next(csv_reader)
    line_count = 0
    for row in csv_reader:
         print(row[0],'->',row[5])
         # number = float(row[2])
         #   to_float = re.sub(r"(\.| )", ",", row[2])
         #   print('modified: ', to_float)
         line_count += 1
        
    print(f'Processed {line_count} lines.')


# writing
# header = ['Name', 'Capital', 'Surface', 'Neighbors','Time-zone']
# with open(csv_file, 'w', encoding='UTF8') as f:
#     writer = csv.writer(f)
#     # write the header
#     writer.writerow(header)


if __name__ == "__main__":
    main()

