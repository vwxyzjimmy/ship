import pymysql
import numpy as np 
import sys
import xlwt
import matplotlib.pyplot as plt
from interval import Interval
key_word = sys.argv[1]

filename = key_word + ".xls"
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("original-data")
sheet2 = book.add_sheet("min-max")
sheet3 = book.add_sheet("z-score-1")
sheet4 = book.add_sheet("z-score-2 std distribute number")

db_connect = pymysql.connect("140.116.39.173", "root", "rootroot", "shipping", charset="utf8")
cursor = db_connect.cursor()
mysql_show_db_command = 'show databases'
cursor.execute(mysql_show_db_command)

mysql_table_command = "describe " + key_word
cursor.execute(mysql_table_command)
table = str(cursor.fetchall())
temp = table.split("), ")
column_matrix = []
excel1_y = 0
excel2_y = 0
excel3_y = 0
excel4_y = 0
for i in range(len(temp)):
	temp2 = temp[i].split(",")
	column = temp2[0].strip("'").strip("(u").strip("'")
	column_matrix.append(column)
	sheet1.write(excel1_y,  i, column)
	sheet2.write(excel2_y, i, column)
	sheet3.write(excel3_y, i, column)
	if i != 0:
		sheet4.write(excel4_y, i*2, 'Number')
		sheet4.write(excel4_y, i*2-1, column + ' std distribute')
	else:
		sheet4.write(excel4_y, i, column)
excel1_y = excel1_y + 1
excel2_y = excel2_y + 1
excel3_y = excel3_y + 1
excel4_y = excel4_y + 1

mysql_data_command = "select * from " + key_word
cursor.execute(mysql_data_command)
data = cursor.fetchall()
tmp = str(data)
data = tmp.split("), (")
data[0] = data[0].strip("((")
data[len(data)-1] = data[len(data)-1].strip("))")
data_matrix = []
float_matrix = []
for i in range(len(data)):
	data_matrix.append([])
	float_matrix.append([])
	tmp = data[i].split(", ")
	for j in range(len(tmp)):
		data_matrix[i].append(tmp[j].strip("u").strip("'"))
		try:
			float_matrix[i].append(float(tmp[j].strip("u").strip("'")))
		except:
			float_matrix[i].append(-999)
		try:
			sheet1.write(i+excel1_y, j, float(data_matrix[i][j]))
			
		except:
			sheet1.write(i+excel1_y, j, data_matrix[i][j])
inverse_matrix = map(list, zip(*float_matrix))

#min-max normalization
excel_y_offset = 0
temp_max= []
temp_min= []
for i  in range(len(inverse_matrix)):
	try:
		temp_max.append(inverse_matrix[i][1])
		temp_min.append(inverse_matrix[i][1])
	except:
		pass
for i in range(len(inverse_matrix)):
	for j in range(len(inverse_matrix[i])):
		try:
			if temp_max[i] < inverse_matrix[i][j]:
				temp_max[i] = inverse_matrix[i][j]
			if temp_min[i] > inverse_matrix[i][j] and inverse_matrix[i][j] != -999:
				temp_min[i] = inverse_matrix[i][j]
		except:
			pass
percent = []
for i in range(len(inverse_matrix)):
	temp_range = temp_max[i] - temp_min[i]
	percent.append([])
	count = 0
	for j in range(len(inverse_matrix[i])):
		if i == 0:
			sheet2.write(j+excel2_y, i, int(inverse_matrix[i][j]))
		else:
			try:
				if inverse_matrix[i][j] != -999:
					percent[i].append((inverse_matrix[i][j]-temp_min[i])/temp_range)
					sheet2.write(j+excel2_y, i, percent[i][j])
				else:
					sheet2.write(j+excel2_y, i, 'None')
			except:
				sheet2.write(j+excel2_y, i, (inverse_matrix[i][j]-temp_min[i])/temp_range)

#z-score normalization
mean_number = []
valid_number = []
mean_matrix = []
for i in range(len(inverse_matrix)):
	mean_number.append(0)
	valid_number.append(0)
	mean_matrix.append([])
	valid_count = 0
	add_total = 0
	for j in range(len(inverse_matrix[i])):
		if inverse_matrix[i][j] != -999:
			add_total = add_total + inverse_matrix[i][j]
			valid_number[i] = valid_number[i] + 1
		else:
			pass
	try:
		mean = add_total/valid_number[i]
	except:
		mean = 0
	mean_number[i] = mean

without_None_matrix = []
for i in range(len(inverse_matrix)):
	without_None_matrix.append([])
	test = 0
	for j in range(len(inverse_matrix[i])):
		if inverse_matrix[i][j] != -999:
			without_None_matrix[i].append(inverse_matrix[i][j])
		else:
			pass

std_number = []
for i in range(len(without_None_matrix)):
	a = np.array(without_None_matrix[i])
	std_number.append(np.std(a))
	if i == 0:
		sheet3.write(1, 0, "mean")
		sheet3.write(2, 0, "std")
	else:
		sheet3.write(1, i, mean_number[i])
		sheet3.write(2, i, std_number[i])
excel3_y = excel3_y + 2 

std_matrix = []
for i in range(len(inverse_matrix)):
	std_matrix.append([])
	dic = {}
	for j in range(len(inverse_matrix[i])):
		if i == 0:
			try:
				std_matrix[i].append(int(inverse_matrix[i][j]))
			except:
				std_matrix[i].append(0)
		else:
			if inverse_matrix[i][j] != -999:
				std_matrix[i].append((inverse_matrix[i][j]-mean_number[i])/std_number[i])
				if dic.has_key(int(std_matrix[i][j])) == True:
					dic[int(std_matrix[i][j])] = dic[int(std_matrix[i][j])] + 1
				else:
					dic[int(std_matrix[i][j])] = 1
			else:
				std_matrix[i].append("None")
			sheet3.write(j+excel3_y, i, std_matrix[i][j])
	print("dic: {0}".format(dic))
	for k in dic.items():
		sheet4.write(excel4_y, 2*i-1, k[0] )
		sheet4.write(excel4_y, 2*i, k[1] )
		excel4_y = excel4_y + 1
	excel4_y = 1

book.save(filename)
'''
cursor.execute("select * from mfm order by `Serial` DESC limit 1 ")
mfm = cursor.fetchall()
cursor.execute("select * from kyma order by `Serial` DESC limit 1 ")
kyma = cursor.fetchall()
'''
db_connect.close()
a = -0.123
print(int(a))
