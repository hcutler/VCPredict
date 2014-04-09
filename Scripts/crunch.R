# Installing required packages
if (!require(ggplot2)){                                                                                                                           
  install.packages("ggplot2")
}
if (!require(gridExtra)){
 install.packages("gridExtra")
}
if (!require(stargazer)){
 install.packages("stargazer")
}

# Loading installed libraries
require("ggplot2")
require("gridExtra")
require("stargazer")


# Reading in data
dat = read.table("Investments.csv", sep=",", head=T, fill=T)
dat[,"funding_round_type"] = factor(dat[,"funding_round_type"])
dat[,"raised_amount_usd"] = as.numeric(dat[,"raised_amount_usd"])

hist(as.numeric(dat[,"raised_amount_usd"]))
