fin = open("../Data/Mattermark/backend/vc-list_raw.html", "r")
fread = fin.read()

fout = open("../Data/backend/vc-list.csv", "w")

split = fread.split("alphabet-directory-header")[1].split("<li>")
for i in range(1, len(split)):
	name = split[i].split("</a>")[0].split(">")[-1]

	print name
	fout.write(name + "\n")

fout.close()