library("plyr")
library("ggplot2")
library("data.table")

bestArm = strtoi(Sys.getenv("BEST_ARM"))
numOfArms = strtoi(Sys.getenv("N_ARMS"))
sims = strtoi(Sys.getenv("NUM_SIMS"))
horizon = strtoi(Sys.getenv("HORIZON"))

simsFormat = sprintf("%dx%d_%dx%d", numOfArms, bestArm, horizon, sims)
inputFile = sprintf("hedge_results/%s.tsv", simsFormat)
outputFile = sprintf("hedge_results/%s.png", simsFormat)
caption = sprintf("Hedge %d arms (best arm: %d) sims: %d/hirozon: %d", numOfArms, bestArm, sims, horizon)

results <- fread(inputFile, header = F)
names(results) <- c("Eta", "Sim", "T", "ChosenArm", "Reward", "CumulativeReward")
results <- transform(results, Eta = factor(Eta))

# Plot average reward as a function of time.
stats1 <- ddply(results,
               c("Eta", "T"),
               function (df) {mean(df$Reward)})
a <- ggplot(stats1, aes(x = T, y = V1, group = Eta, color = Eta)) +
 geom_line() +
 ylim(0, 1) +
 xlab("Time") +
 ylab("Average Reward") +
 ggtitle("Performance")

# Plot frequency of selecting correct arm as a function of time.
# In this instance, 5 is the correct arm.
stats2 <- ddply(results,
               c("Eta", "T"),
               function (df) {mean(df$ChosenArm == bestArm)})
b <- ggplot(stats2, aes(x = T, y = V1, group = Eta, color = Eta)) +
 geom_line() +
 ylim(0, 1) +
 xlab("Time") +
 ylab("Probability of Selecting Best Arm") +
 ggtitle("Accuracy")

# Plot variance of chosen arms as a function of time.
stats3 <- ddply(results,
               c("Eta", "T"),
               function (df) {var(df$ChosenArm)})
c <- ggplot(stats3, aes(x = T, y = V1, group = Eta, color = Eta)) +
 geom_line() +
 xlab("Time") +
 ylab("Variance of Chosen Arm") +
 ggtitle("Variability")

# Plot cumulative reward as a function of time.
stats4 <- ddply(results,
c("Eta", "T"),
function (df) {mean(df$CumulativeReward)})
d <- ggplot(stats4, aes(x = T, y = V1, group = Eta, color = Eta)) +
 geom_line() +
 xlab("Time") +
 ylab("Cumulative Reward of Chosen Arm") +
 ggtitle("Cumulative Reward")


# 連結表示
library(grid)
library(gridExtra)

g <- arrangeGrob(a, b, c, d, ncol=2, top=caption)
grid.draw(g)
print(g)
ggsave(file=outputFile, g)

