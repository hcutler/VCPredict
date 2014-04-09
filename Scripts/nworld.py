def c(s):
	return "\"" + str(s).replace("\"", "\'").strip() + "\""

fin = open("../Data/NetworkWorld/backend/Workbook10.csv", "r").read().split("\r")
fout = open("../Data/NetworkWorld/NetworkWorld.csv", "w")

fout.write("Company,City,Industry,Amount raised,Investors,Type of Financing,Quarter,What the co. does\n")

for i in range(0, len(fin) - 1):
	if i % 2 == 1: continue
	fout.write(fin[i].replace(":,", ",") + "," + c(fin[i+1].split(",,")[1]) + "\n")

fout.close()