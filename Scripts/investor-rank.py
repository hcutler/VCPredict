import networkx as nx

def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

d = {}

fin = open("../Data/backend/crunchbase_investments_pruned.csv", "r").read().split("\r")
ct = 0
for line in fin:
	ct += 1
	if ct <= 1: continue

	i = line.split(",")[0]
	v = line.split("\n")[0].split(",")[1]

	if not i in d: d[i] = [v]
	elif not v in d[i]: d[i].append(v)

g_n = {}
g_e = {}
for k, v in d.iteritems():
	#print k + "\t" + str(v)

	for i in range(0, len(v)):
		if not v[i] in g_n: 
			g_n[v[i]] = []
			g_e[v[i]] = {}
		for j in range(0, len(v)):
			if i == j: continue
			if not v[j] in g_n[v[i]]:
				g_n[v[i]].append(v[j])
				g_e[v[i]][v[j]] = 1
			else:
				g_e[v[i]][v[j]] += 1

G = nx.DiGraph()
for k in g_n.keys():
	G.add_node(k)
for k, v in g_n.iteritems():
	sum = 0
	for p, q in g_e[k].iteritems():
		sum += q
	if sum == 0: continue
	for p, q in g_e[k].iteritems():
		G.add_weighted_edges_from([(k, p, float(q)/float(sum))])

rank = nx.pagerank(G)

fout = open("../Data/Investor Rank.csv", "w")
out = sorted(rank.items(), key=lambda x: x[1], reverse=True)
for k, v in out:
	print k + "\t" + str(v)
	fout.write(c(k) + "," + c(str(v)) + "\n")
fout.close()