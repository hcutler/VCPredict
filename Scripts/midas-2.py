def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

fin = open("../Data/backend/midas-raw.html", "r").read()
s = fin.split("<table id=\"the_list\"")[1].split("</table>")[0].split("<tr class=\"data\">")

fout = open("../Data/Midas/Midas 2014.csv", "w")
fout.write("Rank,Name,Firm,Big Deal\n")
for i in range(1, len(s)):
	rank = i
	name = s[i].split("<td class=\"name\">")[1].split("</a>")[0].split(">")[-1]
	firm = s[i].split("<td>")[1].split("</td>")[0]
	big_deal = s[i].split("<td>")[2].split("</td>")[0]

	print str(rank) + "\t" + name + "\t" + firm + "\t" + big_deal
	fout.write(str(rank) + "," + c(name) + "," + c(firm) + "," + c(big_deal) + "\n")
fout.close()