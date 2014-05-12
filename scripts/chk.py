import csv

angel = {}

fin = open("../data/munge/angel-cmp.csv", "r+").read().replace("\r", "\n")
mycsv = csv.reader(fin.split("\n"), delimiter = ",", quotechar="\"")
ct = 0
for row in mycsv:
	ct += 1
	if ct <= 1 or len(row) == 0: continue

	if len(row[0]) > 0: angel[row[0]] = 1

crunch = {}

fin = open("../data/munge/crunchbase_full.csv", "r+").read().replace("\r", "\n")
mycsv = csv.reader(fin.split("\n"), delimiter = ",", quotechar="\"")
ct = 0
pt = 0
for row in mycsv:
	ct += 1
	if ct <= 1 or len(row) == 0: continue

	if len(row[0]) > 0: crunch[row[0]] = 1
	if row[0] in angel:
		pt += 1

print str(pt) + "\t" + str(len(fin.split("\n"))) + "\t" + str(float(pt) / len(fin.split("\n")))

ct = 0
for k in crunch.keys():
	if k in angel:
		ct += 1

print str(ct) + "\t" + str(len(crunch.keys())) + "\t" + str(float(ct) / len(crunch.keys()))


