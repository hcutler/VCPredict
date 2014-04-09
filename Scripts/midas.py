import urllib2

def getHTML(url):
	return urllib2.urlopen(url).read()

fout = open("../Data/Midas/Midas.csv", "w")

link = "http://www.forbes.com/midas/list/"
raw = getHTML(link)

fout.write("Rank,Name,Firm,Big Deal\n")
split = raw.split("<table>")[1].split("</table>")[0].split("<tr>")
for i in range(2, len(split)):
	rank = split[i].split("<td class=\"rank\">")[1].split("<")[0]
	name = split[i].split("<td class=\"company\">")[1].split("<h3>")[1].split("<")[0]
	firm = split[i].split("<td>")[1].split("<")[0]
	deal = split[i].split("<td>")[2].split("<")[0]

	print rank + "\t" + name + "\t" + firm + "\t" + deal
	fout.write(rank + "," + name + "," + firm + "," + deal + "\n")