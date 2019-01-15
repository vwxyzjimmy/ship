import smopy
from IPython.display import Image
import math
import matplotlib
import matplotlib.pyplot as plt
import pyexcel as pe
import os
import sys
import xlwt
import numpy as np
from interval import Interval
import numpy

filename = sys.argv[1]
filename_split = str(filename.split('.'))
path_here = os.getcwd() + '/' 
file_path = path_here + filename
ro_matrix = pe.get_array(file_name = file_path)

excel_file_name = filename_split[0] + "-lalo.xls"
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("preprocessing_lalo")

in_dif_array = []
ser_lalo_array = []
cross_180 = []
ship_dir = 1
for j in range(len(ro_matrix[0])):
	if ro_matrix[0][j] == "Serial":
		print("got serial")
		ser_lalo_array.append([])
		for i in range(1, len(ro_matrix)):
			try:
				ser_lalo_array[0].append(int(ro_matrix[i][j]))
			except:
				ser_lalo_array[0].append(-999)
	if ro_matrix[0][j] == "Latitude":
		print("got latitude")
		ser_lalo_array.append([])
		for i in range(1, len(ro_matrix)):
			try:
				latitude = float(ro_matrix[i][j])//100 + (float(ro_matrix[i][j])%100)*10/6*0.01
				ser_lalo_array[1].append(latitude)
			except:
				ser_lalo_array[1].append(-999)
	if ro_matrix[0][j] == "Longitude":
		print("got longitude")
		ser_lalo_array.append([])
		for i in range(1, len(ro_matrix)):
			try:
				if (180-float(ro_matrix[i][j])) < (180 - float(ro_matrix[i-1][j])):	
					count = 0	
					while(count < 2880):
						try:
							if (180-float(ro_matrix[i+count][j])) < (180 - float(ro_matrix[i+count+1][j])):
								if ((180-0.01*float(ro_matrix[i][j])) < 20):
									cross_180.append(i+count)
									#print(ro_matrix[i+count][j])
									break
						except:
							pass
						count = count + 1
			except:
				pass
			try:
				tmp_longitude = float(ro_matrix[i][j])//100 + (float(ro_matrix[i][j])%100)*10/6*0.01
				longitude = ship_dir*tmp_longitude
				ser_lalo_array[2].append(longitude)
			except:
				ser_lalo_array[2].append(-999)

cross_180_div = [[]]
cross_count = 0
cross_point = []
for i in range(len(cross_180)):
	if (i > 0) and  (cross_180[i] - cross_180[i-1]) >= 10:
		cross_180_div.append([])
		cross_count = cross_count + 1
	else:
		cross_180_div[cross_count].append(cross_180[i])
for i in range(len(cross_180_div)):
	a = cross_180_div[i][len(cross_180_div[i])-1]
	cross_point.append(a)
	print("cross point: {0}".format(a))

for i in range(len(cross_point)):
	a = math.pow(-1, i)
	if i == 0:
		print("0 th first")
		for j in range(0, int(cross_point[i])):
			ser_lalo_array[2][j] = ser_lalo_array[2][j] * a
			sheet1.write(j+1, 0, float(ser_lalo_array[0][j]))
			sheet1.write(j+1, 1, float(ser_lalo_array[1][j]))
			sheet1.write(j+1, 2, float(ser_lalo_array[2][j]))
	elif i == (len(cross_point) - 1):
		print("{0}th last".format(i))
		print("int(cross_point[i-1], len(ser_lalo_array)):{0}, {1}".format(int(cross_point[i]), len(ser_lalo_array[0])))
		for j in range(int(cross_point[i-1]), int(cross_point[i])):
			ser_lalo_array[2][j] = ser_lalo_array[2][j] * a
			sheet1.write(j+1, 0, float(ser_lalo_array[0][j]))
			sheet1.write(j+1, 1, float(ser_lalo_array[1][j]))
			sheet1.write(j+1, 2, float(ser_lalo_array[2][j]))
	
		for j in range(int(cross_point[i]), len(ser_lalo_array[0])):
			ser_lalo_array[2][j] = ser_lalo_array[2][j] * a * (-1)
			sheet1.write(j+1, 0, float(ser_lalo_array[0][j]))
			sheet1.write(j+1, 1, float(ser_lalo_array[1][j]))
			sheet1.write(j+1, 2, float(ser_lalo_array[2][j]))
	else:
		print("{0}th".format(i))
		for j in range(int(cross_point[i-1]), int(cross_point[i])):
			ser_lalo_array[2][j] = ser_lalo_array[2][j] * a
			sheet1.write(j+1, 0, float(ser_lalo_array[0][j]))
			sheet1.write(j+1, 1, float(ser_lalo_array[1][j]))
			sheet1.write(j+1, 2, float(ser_lalo_array[2][j]))
count = 0
start_stop_pos = [[], []]
while count < len(ser_lalo_array[0])-2:
	if (ser_lalo_array[1][count]) != -999 and (ser_lalo_array[2][count]) != -999 and  (ser_lalo_array[1][count]) != 999 and (ser_lalo_array[2][count]) != 999 :
		if (ser_lalo_array[1][count+1])-(ser_lalo_array[1][count]) == 0 and (ser_lalo_array[2][count+1])-(ser_lalo_array[2][count]) == 0:
			
			#start_stop_pos[0].append(count)
			#print("stop point:{0}".format(count))
			stop_sig = False
			while True:
				if count < len(ser_lalo_array[0])-2:
					is_stop = True
					for i in range(20):
						if count < len(ser_lalo_array[0])-22:
							if (ser_lalo_array[1][count+1+i])-(ser_lalo_array[1][count+i]) != 0 or (ser_lalo_array[2][count+1+i])-(ser_lalo_array[2][count+i]) != 0 :
								is_stop = False
								break
					if is_stop == True:
						start_stop_pos[0].append(count)
						print("stop point:{0}".format(count))
						stop_sig = True
						break
				else:
					stop_sig = False
					break
				count = count + 1
			if stop_sig == True:
				while True:
					if count < len(ser_lalo_array[0])-2:
						if (ser_lalo_array[1][count+1])-(ser_lalo_array[1][count]) != 0 or (ser_lalo_array[2][count+1])-(ser_lalo_array[2][count]) != 0:
							is_start = True
							for i in range(20):
								if count < len(ser_lalo_array[0])-22:
									if (ser_lalo_array[1][count+1+i])-(ser_lalo_array[1][count+i]) == 0 and (ser_lalo_array[2][count+1+i])-(ser_lalo_array[2][count+i]) == 0 :
										is_start = False
										break
							if is_start == True:
								start_stop_pos[1].append(count)
								print("start point:{0}".format(count))
								break
					else:
						break
					count = count + 1
	count = count + 1
for i in range(len(start_stop_pos[0])):
	sheet1.write(i+1, 3, start_stop_pos[0][i])
for i in range(len(start_stop_pos[1])):
	sheet1.write(i+1, 4, start_stop_pos[1][i])
#print(start_stop_pos[0])
#print(start_stop_pos[1])
book.save(excel_file_name)

hz = smopy.Map((30., 180., 45., -180.), z=3)
ax = hz.show_mpl(figsize=(80, 60))
for i in range(len(ser_lalo_array[0])):
	if ser_lalo_array[1][i] != -999 and ser_lalo_array[2][i] != -999 and ser_lalo_array[1][i] != 999 and ser_lalo_array[2][i] != 999:
		x, y = hz.to_pixels(float(double_inverse_matrix[1][i]), float(double_inverse_matrix[2][i]))
		plot = ax.plot(x, y, 'o', color = 'r', ms=5, mew=5)
for i in range(len(start_stop_pos[0])):
	if ser_lalo_array[1][start_stop_pos[0][i]] != -999 and ser_lalo_array[2][start_stop_pos[0][i]] != -999 and ser_lalo_array[1][start_stop_pos[0][i]] != 999 and ser_lalo_array[2][start_stop_pos[0][i]] != 999:
		x, y = hz.to_pixels(float(double_inverse_matrix[1][start_stop_pos[0][i]]), float(double_inverse_matrix[2][start_stop_pos[0][i]]))
		plot = ax.plot(x, y, 'x', color = 'g', ms=35, mew=15)
for i in range(len(start_stop_pos[1])):
	if ser_lalo_array[1][start_stop_pos[1][i]] != -999 and ser_lalo_array[2][start_stop_pos[1][i]] != -999 and ser_lalo_array[1][start_stop_pos[1][i]] != 999 and ser_lalo_array[2][start_stop_pos[1][i]] != 999:
		x, y = hz.to_pixels(float(double_inverse_matrix[1][start_stop_pos[1][i]]), float(double_inverse_matrix[2][start_stop_pos[1][i]]))
		plot = ax.plot(x, y, 'x', color = 'b', ms=35, mew=15)
png_name = filename_split[0] + '.png'
plt.savefig(png_name)

