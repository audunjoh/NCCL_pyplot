import matplotlib.pyplot as plt
import csv
import bitmath
import sys
import os

class Graph:
	def __init__(self):
		self.file_path = ""
		self.file_name = ""
		self.xByteSize = []
		self.yBusbw = []
		self.yAlgbw = []
		self.yTime = []

graphList = []
args = len(sys.argv)

if args == 1:
	print("How to use:\npython3 PlotCSV.py file1.csv file2.csv")
	quit()

for i in range(args-1):
	graphList.append(Graph())
	try:
		graphList[i].file_path = sys.argv[i+1]
		graphList[i].file_name, tmp = os.path.splitext(os.path.basename(graphList[i].file_path))
	except:
		print("Error reading argument " + i+1)
		quit()

	with open(graphList[i].file_path,'r') as csvfile:
		lines = csv.reader(csvfile, delimiter=',')
		header = next(lines)

		#Set column indexes
		sizeIndex = header.index('size')
		algbwIndex = header.index('algbw')
		busbwIndex = header.index('busbw')
		timeIndex = header.index('time')

		# Define bitmath output form
		bitmath.format_string = '{value:0.0f} {unit}'

		# Fill graphobject with data
		for row in lines:
			graphList[i].xByteSize.append(str(bitmath.Byte(int(row[sizeIndex])).best_prefix()))
			graphList[i].yBusbw.append(float(row[busbwIndex]))
			graphList[i].yAlgbw.append(float(row[algbwIndex]))
			graphList[i].yTime.append(float(row[timeIndex]))
	

#fig, ax = plt.subplots(figsize=(12,8))
#ax.set_yscale('symlog', base=2) # logarithmic scale
for g in range(args-1):
	if not(g % 2):
		plt.plot(graphList[g].xByteSize, graphList[g].yAlgbw, linestyle = 'solid', marker = 'o', label=graphList[g].file_name+" Algorithm bandwidth")
	else:
		plt.plot(graphList[g].xByteSize, graphList[g].yAlgbw, linestyle = 'dashed', marker = 'x', label=graphList[g].file_name+" Algorithm bandwidth")

for g in range(args-1):
	if not(g % 2):
		plt.plot(graphList[g].xByteSize, graphList[g].yBusbw, linestyle = 'solid', marker = 'o', label=graphList[g].file_name+" Bus bandwidth")
	else:
		plt.plot(graphList[g].xByteSize, graphList[g].yBusbw, linestyle = 'dashed', marker = 'x', label=graphList[g].file_name+" Bus bandwidth")

#plt.xlabel('Byte size')
plt.ylabel('GB/s')
plt.xticks(rotation=-45)
plt.grid(alpha=0.5)
#plt.locator_params(axis='y', nbins=10)
#plt.gca().set_aspect("equal")
plt.legend()
plt.tight_layout()

# Save to file
#dir_path = os.path.dirname(graphList[0].file_path)
#plt.savefig(graphList[0].file_name + graphList[1].file_name + "_bw.png", bbox_inches='tight')

plt.show()
