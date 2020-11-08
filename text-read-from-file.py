f = open("text_file.txt", "r")
list_data = [line.replace('\n', '') for line in f.readlines() if line != '\n']

print(list_data)


# method 2
list_data = [line.rstrip('\n') for line in open('text_file.txt')]





