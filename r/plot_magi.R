library("plyr")
library("ggplot2")
library("data.table")

if (Sys.getenv("BASE_DIR") != "") {
  baseDir = Sys.getenv("BASE_DIR")
  bestArm = strtoi(Sys.getenv("BEST_ARM"))
  numOfArms = strtoi(Sys.getenv("N_ARMS"))
  num_sims = strtoi(Sys.getenv("NUM_SIMS"))
  horizon = strtoi(Sys.getenv("HORIZON"))
} else {
  baseDir = "magi_results/random"
  bestArm = 17
  numOfArms = 25
  num_sims = 5000
  horizon = 250
}

caption = sprintf("[horizon: %d / simulates: %d]", horizon, num_sims)
simsFormat = sprintf("%dx%d_%dx%d", numOfArms, bestArm, horizon, num_sims)
inputFileSims = sprintf("%s/%s.sims.tsv", baseDir, simsFormat)
inputFileArms = sprintf("%s/%s.means.tsv", baseDir, simsFormat)
inputFileResults = sprintf("%s/%s.results.tsv", baseDir, simsFormat)
outputFile = sprintf("%s/%s.png", baseDir, simsFormat)

# 腕の初期確率
means <- fread(inputFileArms, header = F)
#print(means)
x <- ggplot(means, aes(x = 0:(nrow(means)-1), y = means$V1)) + 
  geom_point() + 
  ylim(0, 1) +
  labs(x = "Arm", y = "Prob") + 
  ggtitle(sprintf("Means [%d arms (best arm: %d)]", numOfArms, bestArm))

sims <- fread(inputFileSims, header = F)
names(sims) <- c("Algorithm", "Sim", "T", "ChosenArm", "Reward", "CumulativeReward")
sims <- transform(sims, Algorithm = factor(Algorithm))

# Plot average reward as a function of time.
stats1 <- ddply(sims,
               c("Algorithm", "T"),
               function (df) {mean(df$Reward)})
a <- ggplot(stats1, aes(x = T, y = V1, group = Algorithm, color = Algorithm)) +
  geom_line() +
  ylim(0, 1) +
  labs(x="Time", y="Average Reward") +
  ggtitle("Performance")

# Plot frequency of selecting correct arm as a function of time.
# In this instance, 5 is the correct arm.
stats2 <- ddply(sims,
               c("Algorithm", "T"),
               function (df) {mean(df$ChosenArm == bestArm)})
b <- ggplot(stats2, aes(x = T, y = V1, group = Algorithm, color = Algorithm)) +
  geom_line() +
  ylim(0, 1) +
  labs(x="Time", y="Probability of Selecting Best Arm") +
  ggtitle("Accuracy")

# Plot variance of chosen arms as a function of time.
stats3 <- ddply(sims,
               c("Algorithm", "T"),
               function (df) {var(df$ChosenArm)})
c <- ggplot(stats3, aes(x = T, y = V1, group = Algorithm, color = Algorithm)) +
  geom_line() +
  labs(x="Time", y="Variance of Chosen Arm") +
  ggtitle("Variability")

# Plot cumulative reward as a function of time.
stats4 <- ddply(sims,
               c("Algorithm", "T"),
               function (df) {mean(df$CumulativeReward)})
d <- ggplot(stats4, aes(x = T, y = V1, group = Algorithm, color = Algorithm)) +
  geom_line() +
  labs(x="Time", y="Cumulative Reward of Chosen Arm") +
  ggtitle("Cumulative Reward")

# 連結表示
library(grid)
library(gridExtra)

g <- arrangeGrob(x, a, b, c, d,
                layout_matrix = rbind(
                    c(1, 1),
                    c(2, 3),
                    c(4, 5)
                ),
                top=caption)
print(g)
print(outputFile)
grid.draw(g)
ggsave(file=outputFile, g, dpi = 100, width = 14, height = 16)

