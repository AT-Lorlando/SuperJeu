import json as json

dictionary=dict()
for i in range(0,ord('z')+1-ord('a')):
    dictionary[i]=chr(ord('a')+i)

# print(dictionary)

with open("test.json", mode = 'w') as f :
    json.dump(dictionary, f)
    print(dictionary)

with open("test.json", mode = 'r') as f :
    dict=json.load(f)['2']
    print(dict)

# get = dict.get('2')

# with open("test.json",mode = 'w') as f :
#     json.dump(get,f)


