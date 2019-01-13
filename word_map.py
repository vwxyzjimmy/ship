import smopy
from IPython.display import Image
import matplotlib
import matplotlib.pyplot as plt
import pyexcel as pe
import os
import sys
import xlwt
import numpy as np
from interval import Interval

###.........................
th = sys.argv[3]
filename = sys.argv[2]
split_name = filename.split('.')
ori_file = split_name[0]
path_here = os.getcwd() + '/'
file_path = path_here + filename
flow_matrix = pe.get_array(file_name = file_path)

filename_output = th + '-' + ori_file +"-pos-std.xls"
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("std")

dir_array = []
total_array = []

excel_row = 0
excel_column = 0
for i  in range(len(flow_matrix)):
	excel_row = excel_row + 1
	total_array.append([])
	for j in range(len(flow_matrix[i])):
		try:
			total_array[excel_row-1].append(float(flow_matrix[i][j]))
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

sheet1.write(10,10, "mean")
sheet1.write(10,11, mean)
sheet1.write(11,10, "std")
sheet1.write(11,11, std)

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
mass_inverse_matrix = map(list, zip(*total_array))

#...........................................
filename = sys.argv[1]
path_here = os.getcwd() + '/'
file_path = path_here + filename
total_matrix = pe.get_array(file_name = file_path)

hz = smopy.Map((30.,180.,45.,-180.), z=3)
ax = hz.show_mpl(figsize=(80,60))


inverse_matrix = map(list, zip(*total_matrix))

for i in range(len(inverse_matrix[1])):
	try:
		inverse_matrix[2][i] = float(inverse_matrix[2][i]) - 90
		inverse_matrix[1][i] = float(inverse_matrix[1][i])
		inverse_matrix[0][i] = float(inverse_matrix[0][i])

	except:
		inverse_matrix[2][i] = -90
		inverse_matrix[1][i] = 0
		if i != 0 :
			inverse_matrix[0][i] = float(inverse_matrix[0][i])
		else:
			inverse_matrix[0][i] = 0

double_inverse_matrix = map(list, zip(*inverse_matrix))
'''
for i in range(len(inverse_matrix[1])):
	try:
		x, y = hz.to_pixels(inverse_matrix[1][i],inverse_matrix[2][i])	
		plot = ax.plot(x, y, 'or', ms=10,mew=10)
	except:
		print('fail')
plt.savefig('test4.png')
'''
color_dir = { 1:'ob', -1:'og', 2:'or', -2:'oc', 3:'om', -3:'oy'}
count = 0
for i in range(len(double_inverse_matrix)):
	for j in range(len(double_inverse_matrix[i])):
		if double_inverse_matrix[i][j] != 0:
			if j != 2:
				sheet1.write(i+2, j, double_inverse_matrix[i][j])
			else:
				sheet1.write(i+2, j, double_inverse_matrix[i][j] + 90)
		else:
			sheet1.write(i+2, j, "None")
	if i <	len(double_inverse_matrix) and i < len(total_array):
		#print('i: {0},  len(double_inverse_matrix): {1}, len(total_array): {2}'.format(i, len(double_inverse_matrix), len(total_array)))
		for k in range( int(total_array[i][0]) - int(double_inverse_matrix[i][0])-100 ,int(double_inverse_matrix[i][0])- int(total_array[i][0]) + 100 ):
			#print(k)
			try:
				if int(double_inverse_matrix[i][0]) == total_array[i+k][0]:
					#print('i, i+k: {0}, {1}'.format(i,i+k))
					x, y = hz.to_pixels(float(double_inverse_matrix[i][1]),float(double_inverse_matrix[i][2]))
					if total_array[i+k][4] < 1 and  total_array[i+k][4] >= 0 :
						plot = ax.plot(x, y, 'ob', ms=5,mew=5)
					elif total_array[i+k][4] < 2 and  total_array[i+k][4] >= 1 :
						plot = ax.plot(x, y, 'oc', ms=5,mew=5)			
					elif total_array[i+k][4] >= 2:
						#print('serial : {0}'.format(total_array[i+k][0]))
						plot = ax.plot(x, y, 'ow', ms=5,mew=5)
					elif total_array[i+k][4] < 0 and  total_array[i+k][4] >= -1 :
						plot = ax.plot(x, y, 'og', ms=5,mew=5)
					elif total_array[i+k][4] < -1 and  total_array[i+k][4] >= -2 :
						plot = ax.plot(x, y, 'om', ms=5,mew=5)
					elif total_array[i+k][4] < -2 :
						plot = ax.plot(x, y, 'ok', ms=5,mew=5)
					else:
						pass

					for j in range(len(total_array[i+k])):
						if total_array[i+k][j] != -999:
							print(total_array[i+k][0])
							sheet1.write(i+2, j+3, total_array[i+k][j])
						else:
							sheet1.write(i+2, j+3, "None")
					#print(total_array[0][0] )
			except:
				#print('fail')
				pass
			else:
				pass
	else:
		pass
#...........................................................
'''
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
'''
book.save(filename_output)
png_name = th + '-std.png'
plt.savefig(png_name)

