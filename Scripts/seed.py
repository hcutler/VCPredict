import urllib2

def getHTML(url):
	return urllib2.urlopen(url).read()

def c(s):
	return "\"" + s.replace("\"", "\'").strip() + "\""

fout = open("../Data/Seed DB/Seed DB.csv", "w")
fin = open("../Data/Seed DB/backend/raw.html", "r")

grab = fin.read()#getHTML("http://www.seed-db.com/companies/funding?value=exit")
s = grab.split("<table")[1].split("</table>")[0].split("<tr")

fout.write("State,Company Name,Website link,Crunchbase link,Seed Accelerator,Exit Value,,Funding,Employees,Rounds,Country,-\n")

for i in range(2, len(s)):
	try: state = s[i].split("<td>")[1].split("</button")[0].split(">")[-1]
	except: state = ""
	try: name = s[i].split("<td>")[2].split("<strong>")[1].split("</strong>")[0]
	except: name = ""
	try: wlink = s[i].split("<td>")[3].split("href=\"")[1].split("\"")[0]
	except: wlink = ""
	try: cblink = s[i].split("<td>")[3].split("href=\"")[2].split("\"")[0]
	except: cblink = ""
	try: accel = s[i].split("<td>")[4].split("</a>")[0].split(">")[-1]
	except: accel = ""
	try: exit = s[i].split("<td>")[5].split("</")[0].split(">")[-1]
	except: exit = ""
	try: stat = s[i].split("<td>")[6].split("</span>")[0].split(">")[-1]
	except: stat = ""
	try: funding = s[i].split("<td>")[7].split("</span>")[0].split(">")[-1]
	except: funding = ""
	try: employees = s[i].split("<td>")[8].split("</span>")[0].split(">")[-1]
	except: employees = ""
	try: rounds = s[i].split("<td>")[9].split("</span>")[0].split(">")[-1]
	except: rounds = ""
	try: country = s[i].split("<td>")[10].split("<")[0]
	except: country = ""
	try: country_2 = s[i].split("<td>")[11].split("<")[0]
	except: country_2 = ""

	print c(state) + "\t" + c(name) + "\t" + c(accel) + "\t" + c(exit) + "\t" + c(stat) + "\t" + c(funding) + "\t" + c(employees) + "\t" + c(rounds) + "\t" + c(country) + "\t" + c(country_2)
	fout.write(c(state) + "," + c(name) + "," + c(wlink) + "," + c(cblink) + "," + c(accel) + "," + c(exit) + "," + c(stat) + "," + c(funding) + "," + c(employees) + "," + c(rounds) + "," + c(country) + "," + c(country_2) + "\n")

fout.close()