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
print(total_array[0])
tmp_total_array = map(list, zip(*total_array))

for i in range(len(tmp_total_array)):
	for j in range(len(tmp_total_array[i])):
		if tmp_total_array[i][j] == -999:
			for k in range(j, len(tmp_total_array[i])):
				if tmp_total_array[i][k] != -999:
					dif = (tmp_total_array[i][k] - tmp_total_array[i][j-1])/ (k-(j-1))
					for l in range(j,k):
						tmp_total_array[i][l] = tmp_total_array[i][j-1] + (l-(j-1))*dif
						#print(tmp_total_array[i][l])
					break

total_array = map(list, zip(*tmp_total_array))
print(total_array[0])
count_valid = 0
sum_valid = 0
valid_array = []
for i in range(len(total_array)):
	print(total_array[i])
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

for i in range(len(total_array)):
	if total_array[i][1] != -999 and total_array[i][2] !=-999:
		total_array[i].append((total_array[i][3]-mean)/std)
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
		inverse_matrix[2][i] = -999
		inverse_matrix[1][i] = -999
		if i != 0 :
			inverse_matrix[0][i] = float(inverse_matrix[0][i])
		else:
			inverse_matrix[0][i] = 0

for i in range(len(inverse_matrix)):
	for j in range(len(inverse_matrix[i])):
		if inverse_matrix[i][j] == -999:
			for k in range(j, len(inverse_matrix[i])):
				if inverse_matrix[i][k] != -999:
					if inverse_matrix[i][k]*inverse_matrix[i][j-1] < 0:
						print ("cross: {0}, {1}".format(inverse_matrix[i][j-1], inverse_matrix[i][k]))
						dif = (90-inverse_matrix[i][j-1] + inverse_matrix[i][k]-(-270))/(k-(j-1))
						for l in range(j, k):
							inverse_matrix[i][l] = inverse_matrix[i][j-1] + (l-(j-1))*dif
							if inverse_matrix[i][l] > 90:
								inverse_matrix[i][l] = inverse_matrix[i][l] -360
						break
					else:
						dif = (inverse_matrix[i][k] - inverse_matrix[i][j-1])/ (k-(j-1))
						for l in range(j,k):
							inverse_matrix[i][l] = inverse_matrix[i][j-1] + (l-(j-1))*dif
							#print(inverse_matrix[i][l])
						break


double_inverse_matrix = map(list, zip(*inverse_matrix))

color_dir = { 1:'ob', -1:'og', 2:'or', -2:'oc', 3:'om', -3:'oy'}
five_day = []
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
		for k in range( int(total_array[i][0]) - int(double_inverse_matrix[i][0])-100 ,int(double_inverse_matrix[i][0])- int(total_array[i][0]) + 100 ):
			try:
				if int(double_inverse_matrix[i][0]) == total_array[i+k][0]:
					x, y = hz.to_pixels(float(double_inverse_matrix[i][1]),float(double_inverse_matrix[i][2]))
					if total_array[i+k][4] < 1 and  total_array[i+k][4] >= 0 :
						plot = ax.plot(x, y, 'o',color = '#F0FFF0', ms=5,mew=5)
					elif total_array[i+k][4] < 2 and  total_array[i+k][4] >= 1 :
						plot = ax.plot(x, y, 'o', color = '#EF3038',ms=5,mew=5)			
					elif total_array[i+k][4] >= 2:
						plot = ax.plot(x, y, 'o', color = '#9e1b32', ms=5,mew=5)
					elif total_array[i+k][4] < 0 and  total_array[i+k][4] >= -1 :
						plot = ax.plot(x, y, 'og', color = '#F0FFF0',  ms=5,mew=5)
					elif total_array[i+k][4] < -1 and  total_array[i+k][4] >= -2 :
						plot = ax.plot(x, y, 'o',color = '#687681', ms=5,mew=5)
					elif total_array[i+k][4] < -2 :
						plot = ax.plot(x, y, 'o', color = '#2C3539', ms=5,mew=5)
					else:
						pass
					if int(total_array[i+k][4]) != int(total_array[i+k-1][4] ) or total_array[i+k][4]*total_array[i+k-1][4] < 0 :
						pass
						#print (total_array[i+k][0] )
						#00ff00
					if( (int(double_inverse_matrix[i][0])-int(double_inverse_matrix[0][0]))%1440 == 0 and (int(double_inverse_matrix[i][0])-int(double_inverse_matrix[0][0]))/1440 > 0 and (int(double_inverse_matrix[i][0])-int(double_inverse_matrix[0][0]))/1440 < 4): 
						five_day.append(float(double_inverse_matrix[i][1]))
						five_day.append(float(double_inverse_matrix[i][2]))

					for j in range(len(total_array[i+k])):
						if total_array[i+k][j] != -999:
							#print(total_array[i+k][0])
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
for i in range(len(five_day)/2):
	x, y = hz.to_pixels(five_day[2*i],five_day[2*i+1])
	plot = ax.plot(x, y, 'x', color = '#000000', ms=35,mew=15)	
#...........................................................

book.save(filename_output)
png_name = th + '-std.png'
plt.savefig(png_name)

