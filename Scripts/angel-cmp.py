import urllib2,csv

def getHTML(url):
	return urllib2.urlopen(url).read()

def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

def cc(s):
	return "\"" + str(s).replace("\"", "").strip() + "\""

def cq(s):
	split = s.replace(">", "<").split("<")
	rtn = ""
	for i in range(0, len(split)):
		if i % 2 == 0:
			rtn += split[i]
	return rtn

l = {}
with open("../Data/AngelList/AngelList VC.csv", "r+") as f:
	reader = csv.reader(f)
	for line in reader:
		links = line[8].split(",")
		for e in links:
			if len(e) > 0 and "http" in e:
				l[e] = 1

fout = open("../Data/AngelList/AngelList Companies (human readable).csv", "w")
ffout = open("../Data/AngelList/AngelList Companies.csv", "w")
head = "Name,About,Founders,Past Investors,Employees,Advisors,Board Members,Profile Claimed,Founder Links,Investor Links,Employee Links,Advisor Links,Board Links,Funding History\n"
fout.write(head)
ffout.write(head)

ct = 0
for k in l:
	ct += 1
	try:
		g = getHTML(k)

		#name
		name = g.split("<h1 class=\'name\'>")[1].split("<")[0]

		#id
		id = g.split("data-id=\"")[1].split("\"")[0]

		claimed = "Yes"
		if "This is a community-generated profile &middot; If you would like to claim it, please" in g:
			claimed = "No"

		#product
		try: 
			product = cq(g.split("<div class=\'product_desc editable_region\'>")[1].split("</div>")[0])
		except: product = ""

		#founders
		fnames = ""
		flinks = ""
		try:
			s = getHTML("https://angel.co/startup_roles?role=founder&startup_id=" + id).split("<div class=\'name\'>")
			for j in range(1, len(s)):
				try:
					sname = s[j].split("</a>")[0].split(">")[-1]
					slink = s[j].split("href=\\\"")[1].split("\\\"")[0]
					if not "data-type=\\\"User\\\"" in s[j]: continue
					fnames += sname + ","
					flinks += slink + ","
				except: pass
			fnames = fnames[:-1]
			flinks = flinks[:-1]
		except: pass

		#funding rounds
		f = ""
		try:
			s = g.split("</div><ul class=\'startup_rounds with_rounds\'>")[1].split("</ul>")[0].split("<div class=\'header\'>")
			for j in range(1, len(s)):
				try:
					sstage = s[j].split("</div>")[0].split(">")[-1]
					sdate = s[j].split("</div>")[1].split(">")[-1].replace("  ", " ")
					samount = s[j].split("<div class=\'raised\'>")[1].split("</a>")[0].split(">")[-1]
					slink = s[j].split("<div class=\'raised\'>")[1].split("href=\"")[1].split("\"")[0]
					sinames = ""
					silinks = ""
					try:
						sinames = ",".join(cq(s[j].split("<div class=\'participant_list inner_section\'>")[1].split("</div>")[0]).split(", "))
						tmp = s[j].split("<div class=\'participant_list inner_section\'>")[1].split("</div>")[0].split("href=\"")
						for k in range(1, len(tmp)):
							silinks += tmp[k].split("\"")[0] + ","
						silinks = silinks[:-1]
					except: pass
					f += cc(sstage) + "," + cc(sdate) + "," + cc(samount) + "," + cc(slink) + "," + cc(sinames) + "," + cc(silinks) + "\n"
				except: pass
			f = f[:-1]
		except: pass

		#past investors
		inames = ""
		ilinks = ""
		try:
			s = getHTML("https://angel.co/startup_roles?role=past_investor&startup_id=" + id).split("<div class=\'name\'>")
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
			s = getHTML("https://angel.co/startup_roles?role=employee&startup_id=" + id).split("<div class=\'name\'>")
			for j in range(1, len(s)):
				try:
					sname = s[j].split("</a>")[0].split(">")[-1]
					slink = s[j].split("href=\\\"")[1].split("\\\"")[0]
					if not "data-type=\\\"User\\\"" in s[j]: continue
					enames += sname.replace(",", "") + ","
					elinks += slink + ","
				except: pass
			enames = enames[:-1]
			elinks = elinks[:-1]
		except: pass

		#advisors
		anames = ""
		alinks = ""
		try:
			s = getHTML("https://angel.co/startup_roles?role=advisor&startup_id=" + id).split("<div class=\'name\'>")
			for j in range(1, len(s)):
				try:
					sname = s[j].split("</a>")[0].split(">")[-1]
					slink = s[j].split("href=\\\"")[1].split("\\\"")[0]
					if not "data-type=\\\"User\\\"" in s[j]: continue
					anames += sname.replace(",", "") + ","
					alinks += slink + ","
				except: pass
			anames = anames[:-1]
			alinks = alinks[:-1]
		except: pass

		#board members
		bnames = ""
		blinks = ""
		try:
			s = getHTML("https://angel.co/startup_roles?role=board_member&startup_id=" + id).split("<div class=\'name\'>")
			for j in range(1, len(s)):
				try:
					sname = s[j].split("</a>")[0].split(">")[-1]
					slink = s[j].split("href=\\\"")[1].split("\\\"")[0]
					if not "data-type=\\\"User\\\"" in s[j]: continue
					bnames += sname.replace(",", "") + ","
					blinks += slink + ","
				except: pass
			bnames = bnames[:-1]
			blinks = blinks[:-1]
		except: pass

		if len(f) > 0: fhead = "Stage,Date,Amount,Press,Investors,Investor Links\n"
		else: fhead = ""

		print name + "\t" + str(ct) + "\t" + str(len(l))# + "\t" + c(fnames) + "\t" + c(inames) + "\t" + c(enames) + "\t" + c(anames) + "\t" + c(bnames) + "\t" + c(claimed)#str(ct) + "\t" + str(len(l))
		fout.write(c(name) + "," + c(product) + "," + c(fnames) + "," + c(inames) + "," + c(enames) + "," + c(anames) + "," + c(bnames) + "," + c(claimed) + "," + c(flinks) + "," + c(ilinks) + "," + c(elinks) + "," + c(alinks) + "," + c(blinks) + "," + (fhead + f).replace("\n", "\n" + "".join([","] * 13)) + "\n")
		ffout.write(c(name) + "," + c(product) + "," + c(fnames) + "," + c(inames) + "," + c(enames) + "," + c(anames) + "," + c(bnames) + "," + c(claimed) + "," + c(flinks) + "," + c(ilinks) + "," + c(elinks) + "," + c(alinks) + "," + c(blinks) + "," + c(fhead + f) + "\n")
	except: pass
fout.close()
ffout.close()
