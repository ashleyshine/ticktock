#!python3.6
import pandas as pd
import csv
import re

# A handy script to convert the text files in directory ./txt-files/
# in the format given by running .ics files through https://icsconvert.appspot.com/
# to csv files in ./data/ with format: Summary,Start,End

file_names = ['exercise', 'general', 'social', 'work']

for file in file_names:
	with open('./txt-files/{}.txt'.format(file), encoding='utf-8') as f:
		lines = f.readlines()

	lines = [x.strip() for x in lines]

	data = pd.DataFrame(columns=['Summary', 'Start', 'End'])

	def parse_line(line):
		mo = re.match(r"(\w+):\s*(.*)", line)
		if mo:
			return [mo.group(1), mo.group(2)]
		else:
			return ['', '']

	x = 0
	while x < (len(lines)):
		row = {'Summary': '', 'Start': '', 'End': ''}
		field, content = parse_line(lines[x])

		if field == 'Summary':
			row[field] = content
			while(field != 'Created'):
				x += 1
				field, content = parse_line(lines[x])
				if field == 'Start' or field == 'End':
					row[field] = content

		# only want the rows where all three fields are present
		if row['Summary'] != '' and row['Start'] != '' and row['End'] != '':
			data = data.append(row, ignore_index=True)
		x += 1

	print("Writing to ./data/{}.csv".format(file))
	data.to_csv('./data/{}.csv'.format(file), sep=',', index=None)
	
