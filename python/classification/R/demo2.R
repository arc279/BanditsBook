library(dplyr)
library(tidyverse)
library(ggplot2)
library(data.table)
library(reshape2)

setwd("/Users/automagi/workspace/BanditsBook/python/classification/R")
#data <- fread("../../out.oneline.log", header = F)
#names(data) <- c("Id", "Time", "Reward", "gender", "marriage", "income", "age")
#d0 = melt(data, measure.var = c("gender", "marriage", "income", "age"))
#d1 = dcast(d0, Id + Time + Reward ~ variable)

data2 <- fread("../../out.log", header = F)
names(data2) <- c("Id", "Time", "Reward", "SegName", "ArmName")
d2 = dcast(data2, Id + Time + Reward ~ SegName, value.var = "ArmName")

b = names(d2)
c = b[!b %in% c("Id", "Time", "Reward")]
c2 = combn(c, 2)
print(c2)

# table 用メソッド追加
fortify.table <- function(model, ...) {
  data <- reshape2::melt(model)
  return(data)
}

# draw
library(grid)
library(gridExtra)
j <- list()
for(i in 1:ncol(c2)) {
  x <- c2[1, i]
  y <- c2[2, i]
  f <- sprintf("Reward~%s+%s", x, y)
  t <- xtabs(as.formula(f), data=d2, subset = Reward == 1)
  print(t)
  p <- ggplot(data=t) + 
        geom_bar(aes_string(x, y="value", fill=y), stat="identity") + 
#        coord_flip() +
        ggtitle(sprintf("%s + %s", x, y))
  j <- c(j, list(p))
}

caption = "Crosstab Segments"
j <- c(j, ncol=2, top=caption)
g <- do.call(arrangeGrob, j)
grid.draw(g)
ggsave(file="demo2.png", g, dpi = 100, width = 14, height = 16)


###
# t2 = as.data.frame.matrix(t)
# pairs.panels(t2,hist.col="white",rug=F,ellipses=F,lm=T)
