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

filename = argv[1]
path_here = os.getcwd() + '/' 
file_path = path_here + filename
ro_matrix = pe.get_array(file_name = file_path)

in_dif_array = []

excel_row = 0
excel_column = 0
for i in range(len(ro_matrix)):
	excel_row = excel_row + 1
	in_dif_array.append([])
	for j in range(len(ro_matrix[i])):
		try:
			in_dif_array[excel_row - 1].append(float(ro_matrix[i][j]))
		except:
			in_dif_array[excel_row - 1].append(-999)

for i in range(len(in_dif_matrix)):
	for j in range(len(in_dif_matrix[i])):
		if in_dif_matrix[i][j] == -999:
			for k in range(j, len(in_dif_matrix[i])):
				if in_dif_matrix[i][k] != -999:
					dif = (in_dif_matrix[i][k] - in_dif_matrix[i][j-1])/ (k-(j-1))
					for l in range(j,k):
						in_dif_matrix[i][l] = in_dif_matrix[i][j-1] + (l-(j-1))*dif
					break

				
				
	

