import pymysql
import numpy as np 
import sys
import xlwt
import matplotlib.pyplot as plt
key_word = sys.argv[1]

filename = key_word + ".xls"
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet1")
sheet2 = book.add_sheet("Sheet2")
db_connect = pymysql.connect("140.116.39.173", "root", "rootroot", "shipping", charset="utf8")
cursor = db_connect.cursor()
mysql_show_db_command = 'show databases'
cursor.execute(mysql_show_db_command)

mysql_table_command = "describe " + key_word
cursor.execute(mysql_table_command)
table = str(cursor.fetchall())
temp = table.split("), ")
column_matrix = []
for i in range(len(temp)):
	temp2 = temp[i].split(",")
	column = temp2[0].strip("'").strip("(u").strip("'")
	column_matrix.append(column)
	sheet1.write(0, i, column)
	sheet2.write(0, i, column)

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
			sheet1.write(i+1, j, float(data_matrix[i][j]))
			
		except:
			sheet1.write(i+1, j, data_matrix[i][j])
inverse_matrix = map(list, zip(*float_matrix))

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
			sheet2.write(j+1, i, int(inverse_matrix[i][j]))
		else:
			try:
				if inverse_matrix[i][j] != -999:
					percent[i].append((inverse_matrix[i][j]-temp_min[i])/temp_range)
					sheet2.write(j+1, i, percent[i][j])
				else:
					sheet2.write(j+1, i, 'None')
			except:
				sheet2.write(j+1, i, (inverse_matrix[i][j]-temp_min[i])/temp_range)
book.save(filename)
'''
cursor.execute("select * from mfm order by `Serial` DESC limit 1 ")
mfm = cursor.fetchall()
cursor.execute("select * from kyma order by `Serial` DESC limit 1 ")
kyma = cursor.fetchall()
'''
db_connect.close()
