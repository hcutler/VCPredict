library("class")
library("e1071")
library("randomForest")
library("ada")
library("glmnet")
library("pROC")
pdat = read.csv("crunchbase_munged_t1.csv", head=T)

pdat$company_name = NULL
pdat = sapply(pdat, as.numeric)

feature_cols = c(1:2,grep("is_", colnames(pdat)), grep("from_", colnames(pdat)))
label_colss = grep("label_", colnames(pdat))#sample(grep("label_1", colnames(dat)), 1)
#for (label_cols in label_colss) {
label_cols = grep("label_1", colnames(pdat))
  
dat = pdat#[pdat[,label_cols] > 0,]

#1
for (i in 1:2) { #real-valued features
  m = mean(dat[,i])
  s = sd(dat[,i])
  dat = dat[abs(dat[,i] - m) <= 3 * s,]
}

k = 0.7 * nrow(dat)
kv = 0.5 * nrow(dat)
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

cb = cbind(train_set, as.numeric(train_labels))
colnames(cb) = c(colnames(train_set), colnames(dat)[label_cols])
frm = as.formula(paste(paste(colnames(cb)[ncol(cb)], " ~ ", sep=""), paste(colnames(cb)[1:(ncol(cb)-1)], collapse= "+")))
#fit = lm(frm, data=data.frame(cb))
#print(colnames(pdat)[label_cols])
#print(summary(fit)$r.squared)

#}

#K = 5
#knn_model = knn(train=train_set, test=test_set, cl=as.factor(labels), k=K)

classifier = naiveBayes(train_set, train_labels)
classifier = ada(train_set, train_labels)
classifier = randomForest(train_set, train_labels)

pred = predict(classifier, test_set)
table(pred, test_labels, dnn=list('predicted', 'actual'))

###

library(DAAG)
cv.lm(df=data.frame(cb), fit, m=3) # 3 fold cross-validation

library(MASS)
step <- stepAIC(fit, direction="both")
step$anova # display results

###

fit = glm(frm, data = data.frame(cb), family = "multinomial")
pred = predict(fit, data.frame(test_set))
pred = plogis(pred)

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

###

# Classification Tree with rpart
library(rpart)

# grow tree 
fit <- rpart(frm,
             method="class", data=data.frame(cb))

fit = prune(fit, cp=fit$cptable[which.min(fit$cptable[,"xerror"]),"CP"])

printcp(fit) # display the results 
plotcp(fit) # visualize cross-validation results 
summary(fit) # detailed summary of splits

# plot tree 
plot(fit, uniform=TRUE, 
     main="Classification Tree for Kyphosis")
text(fit, use.n=TRUE, all=TRUE, cex=.8)

# create attractive postscript plot of tree 
post(fit, file = "tree.ps", 
     title = "Classification Tree for Kyphosis")









