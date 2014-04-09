import urllib2,string

def getHTML(url):
	return urllib2.urlopen(url).read()

def nasc(s):
	return filter(lambda x: x in string.printable, s)

fin = open("../Data/Mattermark/backend/Workbook6-fr.csv", "r").read()
fout = open("../Data/Mattermark/Mattermark Funding Rounds.csv", "w")

head = fin.split("\r")[19]
#print head
fout.write(nasc(head) + "\n")

split = fin.split("Showing ")
d = {}
for i in range(1, len(split)):
	entry = split[i].split(" of ")[0]
	if entry in d: continue
	else: d[entry] = 1

	#print entry
	if not "FirstPrevious" in split[i]: bk = "mattermark"
	else: bk = "FirstPrevious"

	rows = split[i].split(head)[1].split(bk)[0].split("\r")
	for j in rows[1:-1]:
		if not "," in j: break
		fout.write(nasc(j) + "\n")

fout.close()