import csv
a_csv_file = open("results.csv", "r")
dict_reader = csv.DictReader(a_csv_file)
ordered_dict_from_csv = list(dict_reader)
raise Exception(ordered_dict_from_csv)
