fin = open("../Data/AngelList/backend/curated-list.csv", "r").read().split("\r")
fout = open("../Data/AngelList/backend/curated-list-2.csv", "w")
fout.write(fin[0] + "\n")
for i in range(1, len(fin)):
	if len(fin[i]) == 3: continue
	fout.write(fin[i] + "\n")
fout.close()