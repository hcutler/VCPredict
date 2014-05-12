import networkx as nx
import csv
import numpy as np
import json

def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

'''vc_list = open("../Data/backend/vc-list.csv", "r").read().split("\n")
vcl = {}
for x in vc_list: vcl[x.replace("\"", "")] = 1'''

vcl = {}
fin = open("../data/munge/vc-clust.csv", "r").read().replace("\r", "\n").split("\n")
for line in fin:
	vcl[line.split(",")[0]] = line.split(",")[1]

d = {}
C = {}
V = {}

fin = open("../data/munge/crunchbase_investments_pruned.csv", "r").read().replace("\r", "\n")
mycsv = csv.reader(fin.split("\n"), delimiter = ",", quotechar="\"")
ct = 0
head = []
for row in mycsv:
	ct += 1
	if ct <= 1 or len(row[3].split("-")[0]) < 1: continue
	if int(row[3].split("-")[0]) < 2008: continue
	if not row[1] in vcl: continue

	i = row[0]
	v = row[1]
	cat = row[2]
	if len(v) == 0: continue

	if not i in d: d[i] = [v]
	elif not v in d[i]: d[i].append(v)

	C[v] = cat
	V[v] = 1

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
'''
fout = open("/Users/ap/Downloads/dump.csv", "w")
fout.write("label," + ",".join(g_n.keys()) + "\n")
for k in g_n.keys():
	out = k + ","
	for i in g_n.keys():
		if i in g_e[k]: out += str(g_e[k][i]) + ","
		else: out += "0,"
	fout.write(out[:-1] + "\n")
fout.close()'''

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
idc = nx.in_degree_centrality(G)
odc = nx.out_degree_centrality(G)
cc = nx.closeness_centrality(G)
bc = nx.betweenness_centrality(G)
#cfcc = nx.current_flow_closeness_centrality(G)
#cfbc = nx.current_flow_betweenness_centrality(G)
#ec = nx.eigenvector_centrality(G)
'''
fout = open("../Data/Investor Rank.csv", "w")
fout.write("Name,Pagerank,In-degree Centrality,Out-degree Centrality,Closeness Centrality,Betweenness Centrality\n")
out = sorted([[k,v] for k, v in rank.items()], key=lambda x: x[1], reverse=True)
for k, v in out:
	print k + "\t" + str(v)
	fout.write(c(k) + "," + c(str(v)) + "," + c(str(idc[k])) + "," + c(str(odc[k])) + "," + c(str(cc[k])) + "," + c(str(bc[k])) + "\n")
fout.close()

'''

thresh = 1000

fout = open("/Applications/MAMP/htdocs/investor-rank/verts.csv", "w")
out = sorted([[k,v] for k, v in rank.items() if k in vcl], key=lambda x: x[1], reverse=True)[:min(thresh,len(rank.items()))]
for k, v in out:
	fout.write(c(k) + "," + c(str(v)) + "," + vcl[k] + "\n")
fout.close()

fout = open("/Applications/MAMP/htdocs/investor-rank/adj.csv", "w")
for k, v in out:
	if len(g_e[k]) == 0: continue
	tow = c(k) + ","
	for e in g_e[k]:
		if not e in [x[0] for x in out]: continue
		tow += c(e + "||" + str(g_e[k][e])) + ","
	fout.write(tow[:-1] + "\n")
fout.close()


