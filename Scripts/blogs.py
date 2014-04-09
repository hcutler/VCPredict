import urllib2

def getHTML(url):
	return urllib2.urlopen(url).read()

def c(s):
	return s.replace(",", ";")

fout = open("../Data/Blog Directory/Blog Directory.csv", "w")

link = "http://larrycheng.com/2010/01/13/global-venture-capital-vc-blog-directory-ranked-by-monthly-uniques/"
raw = getHTML(link)

fout.write("Name,Firm,Blog,Link,Average Monthly Uniques\n")
split = raw.split("The Global VC Blog Directory (Avg. Monthly Uniques &ndash; Q409)")[1].split("</ol>")[0].split("<li>")
for i in range(1, len(split)):
	name = split[i].split(",")[0]
	if "<font" in name:
		name = name.split(">")[-1]
	firm = split[i].split(", ")[1].split(",")[0]
	blog = split[i].split("</a>")[0].split(">")[-1]
	link = split[i].split("href=\"")[1].split("\"")[0]
	traffic = split[i].split("</a>")[1].split("(")[1].split(")")[0].replace(",", "")

	print name + "\t" + firm + "\t" + blog + "\t" + link + "\t" + traffic
	fout.write(c(name) + "," + c(firm) + "," + c(blog) + "," + c(link) + "," + c(traffic) + "\n")