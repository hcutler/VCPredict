import urllib2

def getHTML(url):
	return urllib2.urlopen(url).read()

def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

def cq(s):
	split = s.replace(">", "<").split("<")
	rtn = ""
	for i in range(0, len(split)):
		if i % 2 == 0:
			rtn += split[i]
	return rtn

fin = open("../Data/AngelList/backend/curated-list-2.csv", "r").read().split("\r")
fout = open("../Data/AngelList/AngelList VC.csv", "w")

fout.write("Name,About,Portfolio,Founders,Past Investors,Employees,Advisors,Profile Claimed,Portfolio Links,Founder Links,Investor Links,Employee Links,Advisor Links\n")

for i in range(1, len(fin)):
	grab = getHTML(fin[i].split(",")[3])
	if not "href=\"https://angel.co/vc-3\" class=\"tag\"" in grab: continue

	claimed = "Yes"
	if "This is a community-generated profile &middot; If you would like to claim it, please" in grab:
		claimed = "No"

	#name
	name = fin[i].split(",")[1]#grab.split("<h1 class=\'name\'>")[1].split("</h1>")[0]

	#about
	try: about = cq(grab.split("<div class=\'header product\'>")[1].split("<script type=\"text/javascript\">")[0].split("<div class=\'content\'>")[-1].split("</div>")[0])
	except: about = "" 

	#portfolio
	pnames = ""
	plinks = ""
	try:
		s = grab.split("<div class=\'left_block\'>Investor</div>")[1].split("</div>")[0].split("<span")
		for j in range(1, len(s)):
			#if not "data-type=\"Startup\"" in s[j]: print "FLAG"
			sname = s[j].split("</a>")[0].split(">")[-1]
			slink = s[j].split("href=\"")[1].split("\"")[0]
			if "," in slink: print "FLAGG"
			pnames += sname.replace(",", ";") + ","
			plinks += slink + ","
		pnames = pnames[:-1]
		plinks = plinks[:-1]
	except: pass

	#founders
	fnames = ""
	flinks = ""
	try:
		s = getHTML("https://angel.co/startup_roles?role=founder&startup_id=" + fin[i].split(",")[2]).split("<div class=\'name\'>")
		for j in range(1, len(s)):
			try:
				sname = s[j].split("</a>")[0].split(">")[-1]
				slink = s[j].split("href=\\\"")[1].split("\\\"")[0]
				if not "data-type=\\\"User\\\"" in s[j]: 
					print "FLAGGG"
					continue
				fnames += sname + ","
				flinks += slink + ","
			except: pass
		fnames = fnames[:-1]
		flinks = flinks[:-1]
	except: pass
	
	#investors
	inames = ""
	ilinks = ""
	try:
		s = getHTML("https://angel.co/startup_roles?role=past_investor&startup_id=" + fin[i].split(",")[2]).split("<div class=\'name\'>")
		for j in range(1, len(s)):
			try:
				sname = s[j].split("</a>")[0].split(">")[-1]
				slink = s[j].split("href=\\\"")[1].split("\\\"")[0]
				if not "data-type=\\\"User\\\"" in s[j]: continue
				inames += sname + ","
				ilinks += slink + ","
			except: pass
		inames = inames[:-1]
		ilinks = ilinks[:-1]
	except: pass

	#employees
	enames = ""
	elinks = ""
	try:
		s = getHTML("https://angel.co/startup_roles?role=employee&startup_id=" + fin[i].split(",")[2]).split("<div class=\'name\'>")
		for j in range(1, len(s)):
			try:
				sname = s[j].split("</a>")[0].split(">")[-1]
				slink = s[j].split("href=\\\"")[1].split("\\\"")[0]
				if not "data-type=\\\"User\\\"" in s[j]: 
					print "FLAGGG"
					continue
				enames += sname + ","
				elinks += slink + ","
			except: pass
		enames = enames[:-1]
		elinks = elinks[:-1]
	except: pass

	#advisors
	anames = ""
	alinks = ""
	try:
		s = getHTML("https://angel.co/startup_roles?role=founder&startup_id=" + fin[i].split(",")[2]).split("<div class=\'name\'>")
		for j in range(1, len(s)):
			try:
				sname = s[j].split("</a>")[0].split(">")[-1]
				slink = s[j].split("href=\\\"")[1].split("\\\"")[0]
				if not "data-type=\\\"User\\\"" in s[j]: 
					print "FLAGGG"
					continue
				anames += sname + ","
				alinks += slink + ","
			except: pass
		anames = anames[:-1]
		alinks = alinks[:-1]
	except: pass

	print c(name)# + "\t" + c(fnames) + "\t" + c(flinks)#c(fnames) + "\t" + c(flinks) + "\t" + c(froles)#c(about) + "\t" + c(claimed) + "\t" + c(pnames) + "\t" + c(plinks)
	fout.write(c(name) + "," + c(about) + "," + c(pnames) + "," + c(fnames) + "," + c(inames) + "," + c(enames) + "," + c(anames) + "," + claimed + "," + c(plinks) + "," + c(flinks) + "," + c(ilinks) + "," + c(elinks) + "," + c(alinks) + "\n")

fout.close()