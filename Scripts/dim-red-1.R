library(NeatMap)

dat = read.table("dim-red-1.csv", sep=",", head=T)
dat$Name = NULL
dat <- sapply( dat, as.numeric )
heatmap(dat,na.rm = T, row.method="PCA",column.method="average.linkage",
              row.labels=rownames(dat),column.labels=colnames(dat), column.label.size=3) + scale_x_continuous(lim=c(-1,26))+scale_y_continuous(lim=c(-5,150)) +
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
        plot.background=element_blank(),
        legend.title = element_text(size=2))