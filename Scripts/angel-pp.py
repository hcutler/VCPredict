import urllib2,csv

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

l = {}
with open("../Data/angel-vc.csv", "r+") as f:
	reader = csv.reader(f)
	for line in reader:
		links = (",".join(line[9:12])).split(",")
		for e in links:
			if len(e) > 0 and "http" in e:
				l[e] = 1

fout = open("../Data/AngelList/AngelList People.csv", "w")
head = "Name,Founder,Team Member,Investor,Board Member,About,Markets Seeking,Locations Seeking,Founder Links,Team Links,Investor Links,Board Links\n"
fout.write(head)

ct = 0
for k in l:
	ct += 1
	try:
		g = getHTML(k)

		#name
		name = g.split("<h1 itemprop=\'name\'>")[1].split("<")[0]

		#founder
		fnames = ""
		flinks = ""
		try:
			s = g.split("<div class=\'left_block\'>Founder</div>")[1].split("<div class=\'right_block body_tags\'>")[1].split("</div>")[0].split("<span")
			for j in range(1, len(s)):
				if not "data-type=\"Startup\"" in s[j]: 
					print "FLAGGG"
					continue
				sname = s[j].split("</a>")[0].split(">")[-1]
				slink = s[j].split("href=\"")[1].split("\"")[0]
				fnames += sname.replace(",", "") + ","
				flinks += slink + ","
			fnames = fnames[:-1]
			flinks = flinks[:-1]
		except: pass
		#team member
		tnames = ""
		tlinks = ""
		try:
			s = g.split("<div class=\'left_block\'>Team Member</div>")[1].split("<div class=\'right_block body_tags\'>")[1].split("</div>")[0].split("<span")
			for j in range(1, len(s)):
				if not "data-type=\"Startup\"" in s[j]: 
					print "FLAGGG"
					continue
				sname = s[j].split("</a>")[0].split(">")[-1]
				slink = s[j].split("href=\"")[1].split("\"")[0]
				tnames += sname.replace(",", "") + ","
				tlinks += slink + ","
			tnames = tnames[:-1]
			tlinks = tlinks[:-1]
		except: pass

		#investor
		inames = ""
		ilinks = ""
		try:
			s = g.split("<div class=\'left_block\'>Investor</div>")[1].split("<div class=\'right_block body_tags\'>")[1].split("</div>")[0].split("<span")
			for j in range(1, len(s)):
				if not "data-type=\"Startup\"" in s[j]: continue
				sname = s[j].split("</a>")[0].split(">")[-1]
				slink = s[j].split("href=\"")[1].split("\"")[0]
				inames += sname.replace(",", "") + ","
				ilinks += slink + ","
			inames = inames[:-1]
			ilinks = ilinks[:-1]
		except: pass

		#board member
		bnames = ""
		blinks = ""
		try:
			s = g.split("<div class=\'left_block\'>Board Member</div>")[1].split("<div class=\'right_block body_tags\'>")[1].split("</div>")[0].split("<span")
			for j in range(1, len(s)):
				if not "data-type=\"Startup\"" in s[j]: continue
				sname = s[j].split("</a>")[0].split(">")[-1]
				slink = s[j].split("href=\"")[1].split("\"")[0]
				bnames += sname.replace(",", "") + ","
				blinks += slink + ","
			bnames = bnames[:-1]
			blinks = blinks[:-1]
		except: pass

		#what i do
		try: wid = cq(g.split("id=\"profile_summary\"")[1].split("<div class=\'section content\'>")[1].split("<script type=\"text/javascript\">")[0])
		except: wid = ""

		#what i'm looking for: markets
		wilfm = ""
		try:
			s = g.split("id=\"profile_criteria\"")[1].split("<div class=\'left_block\'>Markets</div>")[1].split("</div>")[0].split("<span")
			for j in range(1, len(s)):
				wilfm += s[j].split("</a>")[0].split(">")[-1].replace(",", "") + ","
			wilfm = wilfm[:-1]
		except: pass

		#what i'm looking for: locations
		wilfl = ""
		try:
			s = g.split("id=\"profile_criteria\"")[1].split("<div class=\'left_block\'>Locations</div>")[1].split("</div>")[0].split("<span")
			for j in range(1, len(s)):
				wilfl += s[j].split("</a>")[0].split(">")[-1].replace(",", "") + ","
			wilfl = wilfl[:-1]
		except: pass

		print name + "\t" + str(ct) + "\t" + str(len(l))# + "\t" + c(wilfm) + "\t" + c(wilfl)
		fout.write(c(name) + "," + c(fnames) + "," + c(tnames) + "," + c(inames) + "," + c(bnames) + "," + c(wid) + "," + c(wilfm) + "," + c(wilfl) + "," + c(flinks) + "," + c(tlinks) + "," + c(ilinks) + "," + c(blinks) + "\n")
	except: pass
fout.close()