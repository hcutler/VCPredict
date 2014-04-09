import urllib,urllib2,json

def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

list = open("../Data/backend/vc-list.csv", "r").read().split("\n")
fout = open("../Data/AngelList/backend/list.csv", "w")

fout.write("Name,AL Name,AL ID,AL Link\n")

#ct = 0
for vc in list:
	#ct += 1
	#if ct > 10: break

	try:
		query = "https://api.angel.co/1/search?" + urllib.urlencode({'query': vc, 'type': 'Startup'})
		j = json.load(urllib2.urlopen(query))

		if len(j) == 0:
			name = ""
			id = ""
			link = ""
		else:
			name = j[0]['name']
			id = j[0]['id']
			link = j[0]['url']

		print c(vc) + "\t" + c(name)# + "\t" + c(id) + "\t" + c(link)
		fout.write(c(vc) + "," + c(name) + "," + c(id) + "," + c(link) + "\n")
	except:
		pass

fout.close()



