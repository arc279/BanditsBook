library(dplyr)
library(tidyverse)
library(ggplot2)
library(data.table)
library(reshape2)

data <- fread("demo/out.log", header = F)
names(data) <- c("Id", "Time", "SegName", "ArmName", "Reward")
segments <- list("age", "gender", "income", "marriage")

data[, Time:=NULL]

d0 <- data %>%
  dplyr::group_by(SegName, ArmName) %>%
  dplyr::summarise(Alpha=sum(Reward == 1), Beta=sum(Reward == 0), Value=Alpha/(Alpha+Beta))
library(grid)
library(gridExtra)
c1 <- subset(d0, SegName == "age")
c2 <- subset(d0, SegName == "gender")
g1 <- ggplot(c1, aes(x=ArmName, y=Value, group = 1)) + geom_line()
g2 <- ggplot(c2, aes(x=ArmName, y=Value, group = 1)) + geom_line()
g <- arrangeGrob(g1, g2)
grid.draw(g)


v1 <- acast(data, SegName + ArmName ~ Reward, value.var = "Reward", length)
v2 <- acast(data, ArmName ~ Reward ~ SegName, value.var = "Reward", length)
#print(v2[,1,])
#print(v2[,2,])
v3 <- dcast(data, SegName + ArmName ~ Reward, value.var = "Reward", length)
v4 <- dcast(data, Id ~ SegName + ArmName, value.var = "Reward")


c3 <- subset(data, SegName %in% c("age"))
c4 <- subset(data, SegName %in% c("gender"))
c5 <- inner_join(c3, c4, by="Id")
#print(c5)

c6 <- acast(c5, ArmName.x + ArmName.y ~ Reward.x + Reward.y, length)

c7 <- cbind(c6, CrossSegment = rownames(c6))
rownames(c7) <- NULL
