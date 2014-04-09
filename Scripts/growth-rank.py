import networkx as nx
from datetime import *
import csv, math

def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

def date_cmp(a,b):
	date_a = datetime.strptime(a, "%m/%d/%y")
	date_b = datetime.strptime(b, "%m/%d/%y")

	if date_a < date_b: return 1
	elif date_a == date_b: return 0
	else: return -1

f = {}

fin = open("../Data/backend/crunchbase_companies_pruned.csv", "r+").read().replace("\r", "\n")
mycsv = csv.reader(fin.split("\n"), delimiter = ",", quotechar="\"")
ct = 0
for row in mycsv:
	ct += 1
	if ct <= 1 or len(row[1]) == 0: continue

	i = row[0]

	if not i in f: f[i] = float(row[1].replace(",", ""))

d = {}

fin = open("../Data/backend/crunchbase_investments_pruned_2.csv", "r+").read().replace("\r", "\n")
mycsv = csv.reader(fin.split("\n"), delimiter = ",", quotechar="\"")
ct = 0
for row in mycsv:
	ct += 1
	if ct <= 1 or len(row[5]) == 0: continue

	i = row[0]
	v = row[1]
	t = row[3]
	r = float(row[5].replace(",", ""))
	
	if not v in d: d[v] = []
	flag = True
	for j in range(0, len(d[v])):
		if d[v][j][0] == i:
			if date_cmp(t, d[v][j][1]) == 1:
				d[v][j][1] = t
				flag = False
			break
	if flag: d[v].append([i, t, f[i] / float(r)])

rank = {}
for k, v in d.iteritems():
	summ = 0
	for e in v:
		summ += e[2]
	mean = float(summ) / len(v)
	stddev = math.sqrt(sum((x[2] - mean)**2 for x in v) / len(v))
	rank[k] = [str(mean), str(stddev)]

fout = open("../Data/Growth Rank.csv", "w")
fout.write("Name,Mean M1,Std Deviation M1\n")
out = sorted(rank.items(), key=lambda x: float(x[1][0]), reverse=True)
for k, v in out:
	print k + "\t" + "\t".join(v)
	fout.write(c(k) + "," + ",".join(v) + "\n")
fout.close()




