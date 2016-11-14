library(dplyr)
library(tidyverse)
library(ggplot2)
library(data.table)
library(reshape2)

setwd("/Users/automagi/workspace/BanditsBook/python/classification/R")
ifname = "../../out.log"
ofname = "demo.png"

data <- fread(ifname, header = F)
names(data) <- c("Id", "Time", "Reward", "SegName", "ArmName")
segments <- list("age", "gender", "income", "marriage")

n = nrow(data)
caption = sprintf("%d Simulates of some segments classify with Bandit [Thompson Sampling]", n)

d0 <- data %>%
  dplyr::group_by(SegName, ArmName)%>%
  dplyr::summarise(Alpha=sum(Reward == 1), Beta=sum(Reward == 0), Value=Alpha/(Alpha+Beta))

j <- list()
for (s in segments) {
  dh <- d0 %>%
    dplyr::group_by(SegName, ArmName)%>%
    dplyr::filter(SegName == s) %>%
    tidyr::gather(D1, Value, c(Alpha, Beta, Value))

  d1 <- dh %>% dplyr::filter(D1 != "Value")
  a1 <- ggplot(d1, aes(x=ArmName, y=Value, fill=D1)) +
    geom_bar(width = 0.8, stat = "identity") +
    ylab("Counts") +
    xlab(sprintf("ArmName [%s]", s))

  a2 <- ggplot(d1, aes(x=ArmName, y=Value, fill=D1)) +
    geom_bar(width = 0.8, stat = "identity", position="fill") +
    ylab("Rate") +
    xlab(sprintf("ArmName [%s]", s))
  
  d2 <- dh %>% dplyr::filter(D1 == "Value")
  b <- ggplot(d2, aes(x=ArmName, y=Value, group=D1, color=D1)) +
    geom_line() +
    ylab("CTR") +
    xlab(sprintf("ArmName [%s]", s))

  j <- c(j, list(a1, a2, b))
}

# 連結表示
library(grid)
library(gridExtra)
j <- c(j, ncol=3, top=caption)
g <- do.call(arrangeGrob, j)
print(g)
grid.draw(g)
ggsave(file=ofname, g, dpi = 100, width = 14, height = 16)

