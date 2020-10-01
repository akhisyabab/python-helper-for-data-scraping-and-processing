f = open("text_file.txt", "r")
list_data = [line.replace('\n', '') for line in f.readlines() if line != '\n']

print(list_data)





