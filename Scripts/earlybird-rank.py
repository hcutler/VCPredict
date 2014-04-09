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

def wilson(upvotes, dvotes):
	n = float(upvotes + dvotes)

	if n == 0: return 0

	z = 1.281551565545 #80% confidence
	p = upvotes / n

	left = p + 1/(2 * n) * z * z
	right = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
	under = 1 + 1 / n * z * z

	return (left - right) / under

d = {}

fin = open("../Data/backend/crunchbase_investments_pruned_2.csv", "r+").read().replace("\r", "\n")
mycsv = csv.reader(fin.split("\n"), delimiter = ",", quotechar="\"")
ct = 0
for row in mycsv:
	ct += 1
	if ct <= 1: continue

	i = row[0]
	v = row[1]
	t = row[3]

	if not i in d: d[i] = []

	flag = True
	for j in range(0, len(d[i])):
		if d[i][j][0] == v:
			if date_cmp(t, d[i][j][1]) == 1:
				d[i][j][1] = t
				flag = False
			break
	if flag: d[i].append([v, t])

g_n = {}
g_e = {}
for k, v in d.iteritems():
	for i in range(0, len(v)):
		if not v[i][0] in g_n: 
			g_n[v[i][0]] = []
			g_e[v[i][0]] = {}
		for j in range(0, len(v)):
			if i == j: continue
			
			if not v[j][0] in g_n[v[i][0]]:
				g_n[v[i][0]].append(v[j][0])
				g_e[v[i][0]][v[j][0]] = 0
			
			if date_cmp(v[i][1], v[j][1]) == -1:
				g_e[v[i][0]][v[j][0]] += 1

for k, v in g_n.iteritems():
	for p, q in g_e[k].iteritems():
		w_k = wilson(g_e[k][p], g_e[p][k])
		w_p = wilson(g_e[p][k], g_e[k][p])

		g_e[k][p] = w_k
		g_e[p][k] = w_p

G = nx.DiGraph()
for k in g_n.keys():
	G.add_node(k)
for k, v in g_n.iteritems():
	sum = 0
	for p, q in g_e[k].iteritems():
		sum += q
	if sum == 0: continue
	for p, q in g_e[k].iteritems():
		if q == 0: continue
		G.add_weighted_edges_from([(k, p, float(q)/float(sum))])

rank = nx.pagerank(G)#, max_iter = 200)

fout = open("../Data/EarlyBird Rank.csv", "w")
out = sorted(rank.items(), key=lambda x: x[1], reverse=True)
for k, v in out:
	print k + "\t" + str(v)
	fout.write(c(k) + "," + c(str(v)) + "\n")
fout.close()




