'''
Features:

company_country
company_category_code

number_investments_received_from_{investor_name}
number_investments_received_from_{investor_category_code}
number_investments_received_from_{investor_countries}
age
total_funds_raised_to_date
number_{funding round type}_raised

Labels:

will_receive_investment_from_{investor}
amount_will_receive_from_{investor}
'''

import csv, re
from datetime import *

def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

def rhclean(s):
	return s.strip().replace(" ", "_")

def date_diff(a,b):
	date_a = datetime.strptime(a, "%m/%d/%y")
	date_b = datetime.strptime(b, "%m/%d/%y")

	return (date_a - date_b).days

def num_dates_after(l,d):
	d_d = datetime.strptime(d, "%m/%d/%y")
	rtn = 0
	for e in l:
		d_e = datetime.strptime(e, "%m/%d/%y")
		if (d_e - d_d).days > 0: rtn += 1
	return rtn

def amt_raised_after(l,d):
	d_d = datetime.strptime(d, "%m/%d/%y")
	rtn = 0
	for e in l:
		d_e = datetime.strptime(e[0], "%m/%d/%y")
		if (d_e - d_d).days >= 0 and len(e[1]) > 0: rtn += int(e[1].replace(",", ""))
	return rtn

vc_list = open("../data/vc-list.csv", "r").read().split("\n")
vcl = {}
for x in vc_list: vcl[x.replace("\"", "")] = 1

vcc = {}

fin = open("../data/vc-clust.csv", "r+").read().replace("\r", "\n")
mycsv = csv.reader(fin.split("\n"), delimiter = ",", quotechar="\"")
ct = 0
for row in mycsv:
	ct += 1
	if ct <= 1 or len(row) == 0: continue

	vcc[row[0]] = row[1].strip()

nvcl = {}

#zeroth pass
fin = open("../data/crunchbase_full.csv", "r+").read().replace("\r", "\n")
mycsv = csv.reader(fin.split("\n"), delimiter = ",", quotechar="\"")
ct = 0
for row in mycsv:
	ct += 1
	if ct <= 1 or len(row[3]) == 0: continue
	if not row[3] in vcl: continue

	if not row[3] in nvcl: nvcl[row[3]] = 0
	nvcl[row[3]] += 1
nvcl_thresh = 100

company_category_codes = {}
company_countries = {}
funding_round_types = {}
investor_names = {}
investor_category_codes = {}
investor_countries = {}

investor_names_hist = {}
funding_rounds_hist = {}

#first pass
fin = open("../data/crunchbase_full.csv", "r+").read().replace("\r", "\n")
mycsv = csv.reader(fin.split("\n"), delimiter = ",", quotechar="\"")
ct = 0
for row in mycsv:
	ct += 1
	if ct <= 1 or len(row[1]) == 0 or len(row[3]) == 0: continue

	if not row[3] in vcl or nvcl[row[3]] < nvcl_thresh: continue

	if len(row[1]) > 0 and not row[1] in company_category_codes: company_category_codes[row[1]] = len(company_category_codes.keys())
	if len(row[2]) > 0 and not row[2] in company_countries: company_countries[row[2]] = len(company_countries.keys())
	if len(row[6]) > 0 and not row[6] in funding_round_types: funding_round_types[row[6]] = len(funding_round_types.keys())
	if len(row[3]) > 0 and not vcc[row[3]] in investor_names: investor_names[vcc[row[3]]] = len(investor_names.keys())
	if len(row[4]) > 0 and not row[4] in investor_category_codes: investor_category_codes[row[4]] = len(investor_category_codes.keys())
	if len(row[5]) > 0 and not row[5] in investor_countries: investor_countries[row[5]] = len(investor_countries.keys())

	if not vcc[row[3]] in investor_names_hist: investor_names_hist[vcc[row[3]]] = {}
	if not row[0] in investor_names_hist[vcc[row[3]]]: investor_names_hist[vcc[row[3]]][row[0]] = []
	investor_names_hist[vcc[row[3]]][row[0]].append([row[7], row[-1]])

	if not row[6] in funding_rounds_hist: funding_rounds_hist[row[6]] = {}
	if not row[0] in funding_rounds_hist[row[6]]: funding_rounds_hist[row[6]][row[0]] = []
	if len(row[-1]) > 0: funding_rounds_hist[row[6]][row[0]].append([row[7], row[-1]])

cmp = {}

fout = open("../data/crunchbase_munged_t2.csv", "w")
head = "\"company_name\",\"age\",\"total_funds_raised_to_date\","
for i in company_category_codes.keys(): head += c("is_" + rhclean(i)) + ","
for i in company_countries.keys(): head += c("is_" + rhclean(i)) + ","
for i in investor_names.keys(): head += c("from_" + rhclean(i)) + ","
#for i in investor_category_codes.keys(): head += c("from_" + rhclean(i)) + ","
for i in investor_countries.keys(): head += c("from_" + rhclean(i)) + ','
for i in funding_round_types.keys(): head += c("from_" + rhclean(i)) + ","
for i in investor_names.keys(): head += c("label_" + rhclean(i)) + ","
for i in funding_round_types.keys(): head += c("label_" + rhclean(i)) + ","
fout.write(head[:-1] + "\n")
head = ""

#second pass
fin = open("../data/crunchbase_full.csv", "r+").read().replace("\r", "\n")
mycsv = csv.reader(fin.split("\n"), delimiter = ",", quotechar="\"")
ct = 0
for row in mycsv:
	ct += 1
	if ct <= 1 or len(row[3]) == 0 or len(row[0]) == 0: continue

	if not row[3] in nvcl or nvcl[row[3]] < nvcl_thresh: continue

	n = row[0] #name
	f = row[8] #raised_amount_usd
	if f == "": f = 0
	else: f = int(f.replace(",", ""))

	if not n in cmp:
		cmp[n] = {"company_category_code" : row[1], "company_country" : row[2], "birth_date" : row[7], "total_funds_raised_to_date" : 0, "investor_names" : {}, "investor_category_codes" : {}, "investor_countries" : {}, "funding_rounds" : {}}

	try: age = date_diff(row[7], cmp[n]["birth_date"])
	except: continue

	#binarize company_category_code and company_country
	tmp = ["0"] * len(company_category_codes.keys())
	if cmp[n]["company_category_code"] in company_category_codes: tmp[company_category_codes[cmp[n]["company_category_code"]]] = "1"
	bin_cmpcat = ",".join(tmp)
	tmp = ["0"] * len(company_countries.keys())
	if cmp[n]["company_country"] in company_countries: tmp[company_countries[cmp[n]["company_country"]]] = "1"
	bin_cmpreg = ",".join(tmp)

	out = c(n) + "," + c(age) + "," + c(cmp[n]["total_funds_raised_to_date"]) + "," + bin_cmpcat + "," + bin_cmpreg + ","
	outl = ""

	#binarize investor_name, investor_category_code, investor_countries, and funding_round...and label
	for i in investor_names.keys():
		if i in cmp[n]["investor_names"]: out += str(cmp[n]["investor_names"][i]) + ","
		else: out += "0,"

		if not row[0] in investor_names_hist[i]: outl += "0,"
		else: outl += str(amt_raised_after(investor_names_hist[i][row[0]], row[7])) + ","
	#for i in investor_category_codes.keys():
	#	if i in cmp[n]["investor_category_codes"]: out += str(cmp[n]["investor_category_codes"][i]) + ","
	#	else: out += "0,"
	for i in investor_countries.keys():
		if i in cmp[n]["investor_countries"]: out += str(cmp[n]["investor_countries"][i]) + ","
		else: out += "0,"
	for i in funding_round_types.keys():
		if i in cmp[n]["funding_rounds"]: out += str(cmp[n]["funding_rounds"][i]) + ","
		else: out += "0,"

		if not row[0] in funding_rounds_hist[i]: outl += "0,"
		else: outl += str(amt_raised_after(funding_rounds_hist[i][row[0]], row[7])) + ","

	fout.write(out + outl[:-1] + "\n")

	cmp[n]["total_funds_raised_to_date"] += f
	if not vcc[row[3]] in cmp[n]["investor_names"]: cmp[n]["investor_names"][vcc[row[3]]] = 0
	cmp[n]["investor_names"][vcc[row[3]]] += f
	#if not row[4] in cmp[n]["investor_category_codes"]: cmp[n]["investor_category_codes"][row[4]] = 0
	#cmp[n]["investor_category_codes"][row[4]] += f
	if not row[5] in cmp[n]["investor_countries"]: cmp[n]["investor_countries"][row[5]] = 0
	cmp[n]["investor_countries"][row[5]] += f
	if not row[6] in cmp[n]["funding_rounds"]: cmp[n]["funding_rounds"][row[6]] = 0
	cmp[n]["funding_rounds"][row[6]] += f

	#print ct

fout.close()

#print len([x for x in nvcl.keys() if nvcl[x] >= nvcl_thresh])
































