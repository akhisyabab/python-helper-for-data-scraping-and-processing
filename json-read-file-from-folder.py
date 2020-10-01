files = sorted(glob.glob('./folder_name/*.json'),key=lambda x:float(re.findall("(\d+)",x)[0]))
all_datas = []
for file in files:
    print(file)
    with open(file) as json_file:
        datas = json.load(json_file)
    all_datas.append(datas)