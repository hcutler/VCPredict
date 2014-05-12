library("class")
library("e1071")
library("glmnet")
library("pROC")
library("reshape2")
library("rpart")

#load data
dat = read.csv("crunchbase_munged_t1.csv", head=T)
dat$company_name = NULL
dat = sapply(dat, as.numeric)

#specify features, labels
feature_cols = c(1:2,grep("is_", colnames(dat)), grep("from_", colnames(dat)))
slab = "label_2"
label_cols = grep(slab, colnames(dat))

#1) Remove outliers in real-valued features
for (i in 1:2) { #real-valued features
  m = mean(dat[,i])
  s = sd(dat[,i])
  dat = dat[abs(dat[,i] - m) <= 3 * s,]
}

#1.5) Combine correlated features using PCA
p = princomp(dat[,feature_cols])
#biplot(p, col = c("gray", "red"), cex=0.7) #useful for visualizing p$loadings
dat = cbind(p$scores, dat[,label_cols])
colnames(dat) = c(colnames(dat)[1:(ncol(dat)-1)], slab)
label_cols = grep(slab, colnames(dat))

#2) Split data into training, validation, and test sets
k = 0.7 * nrow(dat) #70% -> training + validation
kv = 0.5 * nrow(dat) #50% -> training
rows = sample(1:nrow(dat), nrow(dat), replace=FALSE)
train_rows = rows[1:kv]
val_rows = rows[(kv+1):k]
test_rows = rows[(k+1):length(rows)]

train_set = dat[train_rows, feature_cols]
val_set = dat[val_rows, feature_cols]
test_set = dat[test_rows, feature_cols]
train_labels = dat[train_rows, label_cols]
val_labels = dat[val_rows, label_cols]
test_labels = dat[test_rows, label_cols]

#3) Run logistic regression
cb = cbind(train_set, as.numeric(train_labels))
colnames(cb) = c(colnames(train_set), colnames(dat)[label_cols])
frm = as.formula(paste(paste(colnames(cb)[ncol(cb)], " ~ ", sep=""), paste(colnames(cb)[1:(ncol(cb)-1)], collapse= "+")))

fit = glm(frm, data = data.frame(cb), family = "binomial")
pred = predict(fit, data.frame(test_set))
pred = 1 / (1 + exp(-1 * pred))#plogis(pred)

#4) Tune threshold to produce ROC curve
roc = matrix(0,nrow=1000,ncol=4)
for (t in 1:1000) {
  th = 0.001 * t
  thresh = matrix(th, nrow=length(test_labels), ncol=1)
  p = (pred > thresh) + 0
  tab = table(p, test_labels)
  acc = sum(p == test_labels) / length(test_labels)
  if (nrow(tab) < 2) next
  tpr = tab[2,2] / sum(tab[,2])
  fpr = tab[2,1] / sum(tab[2,])
  roc[t,1] = tpr
  roc[t,2] = fpr
  roc[t,3] = acc
  roc[t,4] = th
}
colnames(roc) = c("TPR", "FPR", "Accuracy", "Threshold")
rat = na.omit(data.frame(roc, roc[,1] / roc[,2]))
colnames(rat) = c(colnames(roc), "TPR/FPR")

#4.25) Regression tree for implicit feature selection
# grow tree 
cb = cbind(train_set, as.factor(train_labels))
colnames(cb) = c(colnames(train_set), colnames(dat)[label_cols])
frm = as.formula(paste(paste(colnames(cb)[ncol(cb)], " ~ ", sep=""), paste(colnames(cb)[1:(ncol(cb)-1)], collapse= "+")))
fit <- rpart(frm, data=data.frame(cb))

printcp(fit) # display the results 
plotcp(fit) # visualize cross-validation results 
summary(fit) # detailed summary of splits

# plot tree 
plot(fit, uniform=TRUE, 
     main="Classification Tree for Training Set")
text(fit, use.n=TRUE, all=TRUE, cex=.8)

#4.5) Neural net for modeling nonlinearities
cb = cbind(train_set, as.factor(train_labels))
colnames(cb) = c(colnames(train_set), colnames(dat)[label_cols])
frm = as.formula(paste(paste(colnames(cb)[ncol(cb)], " ~ ", sep=""), paste(colnames(cb)[1:(ncol(cb)-1)], collapse= "+")))
fit = nnet(frm, data = data.frame(cb), size = 2, rang = 0.1, decay = 5e-4, maxit = 200)
pred = predict( object = fit, newdata = test_set)

roc = matrix(0,nrow=1000,ncol=4)
for (t in 1:1000) {
  th = 0.001 * t
  thresh = matrix(th, nrow=length(test_labels), ncol=1)
  p = (pred > thresh) + 0
  tab = table(p, test_labels)
  acc = sum(p == test_labels) / length(test_labels)
  if (nrow(tab) < 2) next
  tpr = tab[2,2] / sum(tab[,2])
  fpr = tab[2,1] / sum(tab[2,])
  roc[t,1] = tpr
  roc[t,2] = fpr
  roc[t,3] = acc
  roc[t,4] = th
}
colnames(roc) = c("TPR", "FPR", "Accuracy", "Threshold")
rat = na.omit(data.frame(roc, roc[,1] / roc[,2]))
colnames(rat) = c(colnames(roc), "TPR/FPR")

#5) Run clustering on VCs
pdat = read.csv("crunchbase_full.csv", head=T)

#basic cleaning
pdat$investor_name = factor(pdat$investor_name)
pdat$funding_round_type = factor(pdat$funding_round_type)
pdat$company_category_code = factor(pdat$company_category_code)
pdat$raised_amount_usd = as.numeric(gsub(",","", pdat$raised_amount_usd))#as.numeric(dat$raised_amount_usd)
pdat$investor_permalink = NULL
pdat = na.omit(pdat)

#aggregation into appropriate features -- see summary(ndat) after running the 2 lines below
ndat = dcast(pdat, investor_name + raised_amount_usd ~ funding_round_type)
ndat = aggregate(ndat[,2:dim(ndat)[2]], by = list(Name = ndat$investor_name), FUN = sum)

#make copy of data for clustering
cp = ndat
cp$Name = NULL
cp = sapply(cp, as.numeric)
rownames(cp) = ndat$Name

#add total # investments column
cp = data.frame(cp)
cp[,"total"] = rowSums(cp[,2:ncol(cp)])
for (i in 1:(dim(cp)[2]-1)) {
  cp[,i] = cp[,i] / cp[,"total"]
}

#normalize features
rec = matrix(0, nrow=2, ncol=dim(cp)[2])
rownames(rec) = c("Means", "StdDevs")
for (i in 1:dim(cp)[2]) {
  rec["Means",i] = mean(cp[,i])
  rec["StdDevs",i] = sd(cp[,i])
  cp[,i] = (cp[,i] - rec["Means",i]) / rec["StdDevs", i]
}

k = 3
fit = kmeans(cp, k)

#undo normalization for cluster centers
ctr = fit$centers
for (i in 1:dim(ctr)[2]) {
  ctr[,i] = rec["Means",i+1] + (ctr[,i] * rec["StdDevs", i+1])
}



