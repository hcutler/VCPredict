from os import listdir

def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

def cq(s):
	split = s.replace(">", "<").split("<")
	rtn = ""
	for i in range(0, len(split)):
		if i % 2 == 0:
			rtn += split[i]
	return rtn

root = "../Data/CBInsights/backend/www.cbinsights.com"
f = listdir(root)

fout = open("../Data/CBInsights/CBInsights People.csv", "w")

for file in f:
	fin = open(root + "/" + file, "r").read()

	name = fin.split("<h1 id=\"company_name\">")[1].split("<")[0]
	firm = fin.split("<h1 id=\"company_name\">")[1].split("works at")[1].split("</a>")[0].split(">")[-1]

	bio = fin.split("<div class=\"section\">")[1].split("<div id=\"how_to_reach\"")[0]
	if "bio_long" in bio:
		bio = "<" + bio.split("bio_long")[1]
	bio = cq(bio.split("&nbsp;")[0])

	print c(name) + "\t" + c(firm)
	#print c(bio)
	fout.write(c(name) + "," + c(firm) + "," + c(bio) + "\n\n")
	
	try:
		split = fin.split("Board Positions</h2>")[1].split("</table>")[0].split("<tr>")
		fout.write("Board Positions\n")
		fout.write("Company,Sector/Industry,Funding Amount,Funding Date,Shares Board With\n")
		for i in range(2, len(split)):
			company = split[i].split("<td>")[1].split("</a>")[0].split(">")[-1]
			sector = split[i].split("<td>")[2].split("</td>")[0].replace("&gt;", ">")
			try: funding_amt = split[i].split("<td>")[3].split("<b>")[1].split("</b>")[0]
			except: funding_amt = ""
			try: funding_date = split[i].split("<td>")[3].split("</b> (")[1].split(")</td>")[0]
			except: funding_date = ""
			sbw = cq(split[i].split("<td>")[4]).split(", ")

			#print c(company) + "\t" + c(sector) + "\t" + c(funding_amt) + "\t" + c(funding_date) + "\t" + c(",".join(sbw))
			fout.write(c(company) + "," + c(sector) + "," + c(funding_amt) + "," + c(funding_date) + "," + c(",".join(sbw)) + "\n")
		fout.write("\n")
	except: pass

	try:
		split = fin.split("Shares Boards With</a></h2>")[1].split("</table>")[0].split("<tr>")
		fout.write("Shares Boards With\n")
		fout.write("Name,Firm,Current & Former Shared Boards\n")
		for i in range(2, len(split)):
			name = split[i].split("<td>")[1].split("</a>")[0].split(">")[-1]
			firm = split[i].split("<td>")[2].split("</a>")[0].split(">")[-1]
			cfsb = cq(split[i].split("<td>")[3].split("including ")[1]).split(", ")

			#print c(name) + "\t" + c(firm) + "\t" + c(",".join(cfsb))
			fout.write(c(name) + "," + c(firm) + "," + c(",".join(cfsb)) + "\n")
		fout.write("\n")
	except: pass

	try:
		split = fin.split("Investors They Know</h2>")[1].split("</table>")[0].split("<tr>")
		fout.write("Investors They Know\n")
		fout.write("Name,Firm Name,Bio\n")
		for i in range(2, len(split)):
			name = split[i].split("<td>")[1].split("</a>")[0].split(">")[-1]
			firm = split[i].split("<td>")[2].split("</a>")[0].split(">")[-1]
			bio = split[i].split("<td>")[3].split("</td>")[0]

			#print c(name) + "\t" + c(firm) + "\t" + c(bio)
			fout.write(c(name) + "," + c(firm) + "," + c(bio) + "\n")
		fout.write("\n")
	except: pass

	try:
		split = fin.split("Executives They Know</h2>")[1].split("</table>")[0].split("<tr>")
		fout.write("Executives They Known\n")
		fout.write("Name,Bio\n")
		for i in range(2, len(split)):
			name = split[i].split("<td>")[1].split("</a>")[0].split(">")[-1]
			bio = split[i].split("<td>")[2].split("</td>")[0]

			#print c(name) + "\t" + c(bio)
			fout.write(c(name) + "," + c(bio) + "\n")
		fout.write("\n")
	except: pass

	fout.write("\n")

fout.close()




