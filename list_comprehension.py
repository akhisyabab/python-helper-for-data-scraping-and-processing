def segreate(arrays):
    return [i for i in arrays if i % 2 == 0] + [i for i in arrays if i % 2 !=0]

if __name__=='__main__':
    arrays = [1, 8, 5, 3, 4, 6, 9, 7, 10]
    arrays = segreate(arrays)
    print(arrays)