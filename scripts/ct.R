library(reshape2)
library(NeatMap)
library(ggplot2)

dat = read.csv("crunchbase_full.csv", head=T)

dat$investor_name = factor(dat$investor_name)
dat$funding_round_type = factor(dat$funding_round_type)
dat$company_category_code = factor(dat$company_category_code)
dat$raised_amount_usd = as.numeric(gsub(",","", dat$raised_amount_usd))#as.numeric(dat$raised_amount_usd)
dat$investor_permalink = NULL

dat = na.omit(dat)

fct = levels(factor(dat$company_region))
#tmp = matrix(0, nrow=length(fct), ncol = 1)
#for (i in 1:length(fct)) {
#  tmp[i,1] = dim(dat[dat$company_region == fct[i],])[1]
#}
#rownames(tmp) = fct
for (i in 1:length(fct)) {
  test = dat[dat$company_region == "SF Bay",]#aggregate(dat[,c("raised_amount_usd")], by = list(Region = dat$company_region), FUN = mean)
  if (dim(test)[1] <= 500) next
  dtest = data.frame(region = test$company_region, rau = test$raised_amount_usd)
  lim = range(dtest$rau)[2] / 10
  bk = lim/50
  pdf(file=paste("company_region/", paste(fct[i], ".pdf", sep=""), sep=""), width=8, height=6)
  print(ggplot(dtest, aes(x=rau)) + geom_histogram(breaks=c(seq(0, lim, by=bk), max(dtest$rau)), position = "identity") +
    coord_cartesian(xlim=c(0,lim+bk), ylim=c(0, dim(dtest)[1])) + geom_density() + xlab("Average Total Funds Raised (USD)") + ylab("Frequency (# VCs)"))
  dev.off()
}
plot(density(dat[dat$investor_name == "Silver Lake Partners","raised_amount_usd"], bw=1000000))
lines(density(dat[dat$investor_name == "New Atlantic Ventures","raised_amount_usd"], bw=1000000), col="green")

ndat = dcast(dat, raised_amount_usd ~ company_region)
ndatt = dcast(dat, investor_name ~ company_category_code)
ndatt$Var.2 = NULL
for (i in 2:dim(ndatt)[2]) {
  ndatt[,i] = as.numeric(ndatt[,i])
}

ndat = dcast(dat, investor_name + raised_amount_usd ~ funding_round_type)

ndat = aggregate(ndat[,2:dim(ndat)[2]], by = list(Name = ndat$investor_name), FUN = sum)
ndatt = aggregate(ndatt[,2:dim(ndatt)[2]], by = list(Name = ndatt$investor_name), FUN = sum)

vcl = as.vector(read.csv("vc-list.csv"))

ndat = ndat[ndat$Name %in% vcl[,1],]
ndatt = ndatt[ndatt$Name %in% vcl[,1],]
ndatt$Name = NULL

num_rounds = dim(ndat)[2] - 1
num_cats = dim(ndatt)[2] - 1
ndat = cbind(ndat, ndatt)

###
cp = ndat
cp$Name = NULL
cp = sapply(cp, as.numeric)
rownames(cp) = ndat$Name

cp = data.frame(cp)
cp[,"total"] = rowSums(cp[,2:ncol(cp)])
for (i in 1:(dim(cp)[2]-1)) {
  cp[,i] = cp[,i] / cp[,"total"]
}

#impute.mean <- function(x) replace(x, is.na(x), mean(x, na.rm = TRUE))
rec = matrix(0, nrow=2, ncol=dim(cp)[2])
rownames(rec) = c("Means", "StdDevs")
for (i in 1:dim(cp)[2]) {
  #cp[,i] = impute.mean(cp[,i])
  rec["Means",i] = mean(cp[,i])
  rec["StdDevs",i] = sd(cp[,i])
  cp[,i] = (cp[,i] - rec["Means",i]) / rec["StdDevs", i]
}

ind = (dim(cp)[2])
#cp = cp[,c((num_rounds+1):ind)]#c(1:num_rounds, dim(cp)[2])]#
cp = cp[,2:ncol(cp)]
fit = kmeans(cp, 3)

ctr = fit$centers
for (i in 1:dim(ctr)[2]) {
  ctr[,i] = rec["Means",i+1] + (ctr[,i] * rec["StdDevs", i+1])
}

aggregate(cp,by=list(fit$cluster),FUN=mean)
mydata = data.frame(cp, fit$cluster)
mydata$Name = rownames(cp)#ndat$Name

test = data.frame(cp)
test$Name = rownames(cp)

pairs(mydata[,1:20], col=mydata$fit.cluster)
###
tmp = seq(1, 20, 1)
for (i in 1:20) {
  fit = kmeans(cp, i)
  tmp[i] = fit$betweenss
}
plot(tmp)

###
ann = read.csv("../Ranks.csv", head=T)
ann$cluster = seq(1, dim(ann)[1], 1)
for (i in 1:dim(ann)[1]) {
  tmp = mydata[mydata$Name == toString(ann[i,"Name"]), "fit.cluster"]
  if (length(tmp) == 0) tmp = -1
  ann[i,"cluster"] = tmp
}
write.csv(file="../Ranks (Clustered).csv", ann)

#####

d = dist(cp)
fitt <- cmdscale(d,eig=TRUE, k=2) # k is the number of dim
fitt # view results

# plot solution 
x <- fitt$points[,1]
y <- fitt$points[,2]
pdf(file="mds.pdf", width=13, height=10)
plot(x, y, xlab="Coordinate 1", ylab="Coordinate 2", 
     main="Metric  MDS", type="n", ylim=c(-3,2))
text(x, y, labels = row.names(cp), cex=.2, col = mydata$fit.cluster)
dev.off()

###
heatmap(as.matrix(cor(t(cp))), cexRow = 0.1, cexCol = 0.1)
heatmap(as.matrix(cp), cexRow = 0.1)

make.heatmap1(t(cp),row.method="PCA",column.method="average.linkage",
              row.labels=rownames(t(cp)),column.labels=colnames(t(cp)), column.label.size=3, row.label.size=0.1) +
  theme(axis.line=element_blank(),
        axis.text.x=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks=element_blank(),
        axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        panel.background=element_blank(),
        panel.border=element_blank(),
        panel.grid.major=element_blank(),
        panel.grid.minor=element_blank(),
        plot.background=element_blank())
        #legend.position="none")

multiplot <- function(..., plotlist=NULL, cols) {
  require(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # Make the panel
  plotCols = cols                          # Number of columns of plots
  plotRows = ceiling(numPlots/plotCols) # Number of rows needed, calculated from # of cols
  
  # Set up the page
  grid.newpage()
  pushViewport(viewport(layout = grid.layout(plotRows, plotCols)))
  vplayout <- function(x, y)
    viewport(layout.pos.row = x, layout.pos.col = y)
  
  # Make each plot, in the correct location
  for (i in 1:numPlots) {
    curRow = ceiling(i/plotCols)
    curCol = (i-1) %% plotCols + 1
    print(plots[[i]], vp = vplayout(curRow, curCol ))
  }
  
}

pointSize=1.5
alpha=99

p = list()

for (i in 1:3) {
datf = data.frame(field = colnames(fit$centers), val = fit$centers[i,])
p[[i]] = ggplot(datf, aes(x=field, y=val, fill="red")) + geom_bar(stat="identity") + ylim(range(fit$centers)) + labs(title = paste("Cluster ", i, sep=""), x = "", y = "") + 
  theme(legend.position="none",
        axis.text.y = element_text(size=9),
        strip.text = element_text(size=16),
        plot.title = element_text(size=16)
  )
}

pdf(file="test6.pdf", width=12, height=6)
multiplot(p[[1]], p[[2]], p[[3]], cols=1)
dev.off()


####

dat = read.csv("crunchbase_munged_t2.csv", head=T)
ndat = dat[,c(1:2, grep("from_", colnames(dat)))]
ndat$company_name = NULL
ndat = sapply(ndat, as.numeric)

p = princomp(ndat)
summary(p)
biplot(p, col = c("gray", "red"), cex=0.7)




