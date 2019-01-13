import pyexcel as pe
#import pyexcel.ext.xls
import os
import sys
import xlwt
import numpy as np
from interval import Interval

filename = sys.argv[1]
split_name = filename.split('.')
ori_file = split_name[0]

path_here = os.getcwd() + '/'
file_path = path_here + filename
total_matrix = pe.get_array(file_name = file_path)

filename_output = ori_file + "-std.xls"
book = xlwt.Workbook(encoding="utf-8") 
sheet1 = book.add_sheet("std") 

dir_array = []
total_array = []

excel_row = 0
excel_column = 0
for i  in range(len(total_matrix)):
	excel_row = excel_row + 1
	total_array.append([])
	for j in range(len(total_matrix[i])):
		try:
			total_array[excel_row-1].append(float(total_matrix[i][j]))
		except:
			total_array[excel_row -1].append(-999)

count_valid = 0
sum_valid = 0
valid_array = []
for i in range(len(total_array)):
	if total_array[i][1] != -999 and total_array[i][2] !=-999:
		total_array[i].append(total_array[i][1] - total_array[i][2])
		sum_valid = sum_valid + (total_array[i][1] - total_array[i][2])
		count_valid = count_valid + 1
		valid_array.append(total_array[i][1] - total_array[i][2])
	else:
		total_array[i].append(-999)
mean = sum_valid/count_valid
a = np.array(valid_array)
std = np.std(a)
sheet1.write(0, 0, "mean")
sheet1.write(0, 1, mean)
sheet1.write(1, 0, "std")
sheet1.write(1, 1, std)

dic = {}
for i in range(len(total_array)):
	if total_array[i][1] != -999 and total_array[i][2] !=-999:
		total_array[i].append((total_array[i][3]-mean)/std)
		if dic.has_key(int(total_array[i][j])) == True:
			dic[int(total_array[i][j])] = dic[int(total_array[i][j])] + 1 
		else: 
			dic[int(total_array[i][j])] = 1 
	else:
		total_array[i].append(-999)
print(total_array)
for i in range(1, len(total_array)):
	for j in range(len(total_array[i])):
		if total_array[i][j] != -999:
			sheet1.write(i+2, j, total_array[i][j])
		else:
			sheet1.write(i+2, j, "None")
key = dic.keys()
key.sort()
excel_y = 5
for k in key: 
	sheet1.write(0, excel_y, k )  
	sheet1.write(1, excel_y, dic[k] ) 
	excel_y = excel_y + 1   


book.save(filename_output)





