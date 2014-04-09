def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

fin = open("../Data/backend/al-ppl-pruned.csv", "r").read().split("\r")

m = {}
l = {}
for i in range(1, len(fin)):
	try:
		for e in fin[i].split("\"")[1].split(","):
			if not e in m: m[e] = 1
			else: m[e] += 1 
		for e in fin[i].split("\"")[2].split(","):
			if not e in l: l[e] = 1
			else: l[e] += 1
	except: pass

fout = open("../Data/backend/dim-red-1.csv", "w")
#fout.write("Name," + ",".join(m.keys() + l.keys()) + "\n")
head = "Name,"
for k in m.keys():
	if m[k] >= 0.01 * len(fin):
		head += k + ","
for k in l.keys():
	if l[k] >= 0.01 * len(fin):
		head += k + ","
fout.write(head[:-1] + "\n")

for i in range(1, len(fin)):
	out = c(fin[i].split(",")[0]) + ","
	'''for k in (m.keys() + l.keys()):
		if k in fin[i]: out += "1,"
		else: out += "0,"'''
	for k in m.keys():
		if m[k] < 0.01 * len(fin): continue
		if k in fin[i]: out += "1,"
		else: out += "0,"
	for k in l.keys():
		if l[k] < 0.01 * len(fin): continue
		if k in fin[i]: out += "1,"
		else: out += "0,"

	fout.write(out[:-1] + "\n")
fout.close()