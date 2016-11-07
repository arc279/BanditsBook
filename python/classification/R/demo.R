library(dplyr)
library(tidyverse)
library(ggplot2)
library(data.table)
library(reshape2)

ifname = "demo/out.log"
ofname = "demo/out.png"

data <- fread(ifname, header = F)
names(data) <- c("Id", "Time", "SegName", "ArmName", "Reward")
segments <- list("age", "gender", "income", "marriage")

n = nrow(data)
caption = sprintf("%d Simulates of some segments classify with bandit [Thompson Sampling]", n)

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
  a <- ggplot(d1, aes(x=ArmName, y=Value, fill=D1)) + 
    geom_bar(width = 0.7, stat = "identity") + 
    ylab(sprintf("Counts [%s]", s))
  
  d2 <- dh %>% dplyr::filter(D1 == "Value")
  b <- ggplot(d2, aes(x=ArmName, y=Value, group=D1, color=D1)) + 
    geom_line() + 
    ylab(sprintf("CVR [%s]", s))

  j <- c(j, list(a, b))
}

# 連結表示
library(grid)
library(gridExtra)
j <- c(j, ncol=2, top=caption)
g <- do.call(arrangeGrob, j)
print(g)
grid.draw(g)
ggsave(file=ofname, g, dpi = 100, width = 14, height = 16)

