def c(s):
	return "\"" + str(s).replace("\"", "\'").replace("\n", "") + "\""

fout = open("../Data/Find The Best/Find The Best.csv", "w")
fin = open("../Data/Find The Best/backend/raw.html", "r") #http://venture-capital-firms.findthebest.com/

fout.write("Firm,Investment Stage,Minimum Investment,Maximum Investment,Location,Country,Fund Size,Link\n")
split = fin.read().split("<tr id=\"listing_row_")
for i in range(1, len(split)):
	firm = split[i].split("<h3><a class=\"srp-listing-title")[1].split(">")[1].split("<")[0]
	link = split[i].split("<h3><a class=\"srp-listing-title")[1].split("href=\"")[1].split("\"")[0]
	stage = ""
	try:
		tmp = split[i].split("<td ")[2].split("</td>")[0].split("<li>")
		for j in range(1, len(tmp)):
			stage += tmp[j].split("</li>")[0] + "/"
		stage = stage[:-1]
	except: pass

	try:
		mini = split[i].split("<td ")[3].split("<div class=\"val\"")[1].split("</span>")[1].split("<")[0] + " " + split[i].split("<td ")[7].split("<div class=\"val\"")[1].split("<div class=\"number_suffix\"")[1].split(">")[1].split("<")[0]
		if "," in mini:
			mini = float(mini.split(" ")[0])
		elif "Billion" in mini:
			mini = float(mini.split(" ")[0]) * 1000000000
		elif "Million" in mini:
			mini = float(mini.split(" ")[0]) * 1000000
	except: mini = ""
	try:
		maxi = split[i].split("<td ")[4].split("<div class=\"val\"")[1].split("</span>")[1].split("<")[0] + " " + split[i].split("<td ")[7].split("<div class=\"val\"")[1].split("<div class=\"number_suffix\"")[1].split(">")[1].split("<")[0]
		if "," in maxi:
			maxi = float(maxi.split(" ")[0])
		elif "Billion" in maxi:
			maxi = float(maxi.split(" ")[0]) * 1000000000
		elif "Million" in maxi:
			maxi = float(maxi.split(" ")[0]) * 1000000
	except: maxi = ""
	try:
		loc = split[i].split("<td ")[5].split(">")[1].split("<")[0]
	except: loc = ""
	try:
		country = split[i].split("<td ")[6].split(">")[1].split("<")[0]
	except: country = ""
	try:
		size = split[i].split("<td ")[7].split("<div class=\"val\"")[1].split("</span>")[1].split("<")[0] + " " + split[i].split("<td ")[7].split("<div class=\"val\"")[1].split("<div class=\"number_suffix\"")[1].split(">")[1].split("<")[0]
		if "," in size:
			size = size.split(" ")[0]
		elif "Billion" in size:
			size = float(size.split(" ")[0]) * 1000000000
		elif "Million" in size:
			size = float(size.split(" ")[0]) * 1000000
	except: size = ""

	#print mini + "\t" + maxi + "\t" + size
	fout.write(c(firm) + "," + c(stage) + "," + c(mini) + "," + c(maxi) + "," + c(loc) + "," + c(country) + "," + c(size) + "," + c(link) + "\n")

fout.close()
fin.close()