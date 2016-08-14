## Python tips -- 7 Simple Tricks to Write Better Python Code 
## https://www.youtube.com/watch?v=VBokjWj_cEA

#1 if __name__ == '__main__'
#2 enumerate
#3 zip
#4 exchange values
#5 dictionary
#6 print file lines
#7 Exception

cities = ['Beijing', 'Shanghai', 'Vancouver', 'Toronto', 'Seattle']

x_list = [11, 12, 13]
y_list = [21, 22, 23]
z_list = [31, 32, 33]

# or a, b = 10, 20
a = 10
b = 20

ages = {
    'Tom' : 19,
    'Max' : 22,
    # 'Mike' : 30
}

x = 'I am X'

#1, 2
# if __name__ == '__main__':
#     for x, city in enumerate(cities):
#         print(x, city)

#3 
# for x, y, z in x_list, y_list, z_list:
#     print(x, y, z)

# for x, y, z in zip(x_list, y_list, z_list):
#     print(x, y, z)

# 4
# print(a, b)
# a, b = b, a
# print(a, b)

#5
# print(ages.get('Mike', 'Unknow'))

#6 
# with open('filename') as f:
#     for line in f:
#         print(line)

#7

# try:
#     print(x)
# except:
#     print('this except')
# else:
#     print('This is else for there is no except')
# finally:
#     print('I am alwasy there')

try:
    print(y)
finally:
    print('I am alwasy there')