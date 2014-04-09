fin = open("../Data/CBInsights/backend/graph_raw.html", "r")
fread = fin.read()

fout = open("../Data/cbinsights-list.csv", "w")

s = fread.split("<tr id=\"p-210115\">")[1].split("/ip-")

for i in range(1, len(s)):
	link = "https://www.cbinsights.com/ip-" + s[i].split("\"")[0]

	print link
	fout.write(link + "\n")

fout.close()