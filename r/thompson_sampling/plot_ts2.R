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
  baseDir = "ts2_results/random"
  num_sims = 1000
  horizon = 1000
}

caption = sprintf("Thompson Sampling [horizon: %d / simulates: %d]", horizon, num_sims)
simsFormat = sprintf("%dx%d", horizon, num_sims)
inputFileSims = sprintf("%s/%s.sims.tsv", baseDir, simsFormat)
inputFileArms = sprintf("%s/%s.means.tsv", baseDir, simsFormat)
inputFileResults = sprintf("%s/%s.results.tsv", baseDir, simsFormat)
outputFile = sprintf("%s/%s.png", baseDir, simsFormat)

# 腕の尤度
means <- fread(inputFileArms, header = F)
names(means) <- c("Means", "Value")
means <- transform(means, Means = factor(Means))
#print(means)
x <- ggplot(means, aes(x = Means, y = Value, group = Means, color = Means)) +
  geom_boxplot() + 
  ylim(0, 1) +
  labs(x = "Arm", y = "Value") + 
  ggtitle("Means")

# シミュレート結果
sims <- fread(inputFileSims, header = F)
names(sims) <- c("Means", "Sim", "T", "ChosenArm", "BesArm", "Reward", "CumulativeReward")
sims <- transform(sims, Means = factor(Means))

# Plot average reward as a function of time.
stats1 <- ddply(sims,
                c("Means", "T"),
                function (df) {mean(df$Reward)})
a <- ggplot(stats1, aes(x = T, y = V1, group = Means, color = Means)) +
  geom_line() +
  ylim(0, 1) +
  labs(x="Time", y="Average Reward") +
  ggtitle("Performance")

# Plot frequency of selecting correct arm as a function of time.
# In this instance, 5 is the correct arm.
stats2 <- ddply(sims,
                c("Means", "T"),
                function (df) {mean(df$ChosenArm == df$BesArm)})
b <- ggplot(stats2, aes(x = T, y = V1, group = Means, color = Means)) +
  geom_line() +
  ylim(0, 1) +
  labs(x="Time", y="Probability of Selecting Best Arm") +
  ggtitle("Accuracy")

# Plot variance of chosen arms as a function of time.
stats3 <- ddply(sims,
                c("Means", "T"),
                function (df) {var(df$ChosenArm)})
c <- ggplot(stats3, aes(x = T, y = V1, group = Means, color = Means)) +
  geom_line() +
  labs(x="Time", y="Variance of Chosen Arm") +
  ggtitle("Variability")

# Plot cumulative reward as a function of time.
stats4 <- ddply(sims,
                c("Means", "T"),
                function (df) {mean(df$CumulativeReward)})
d <- ggplot(stats4, aes(x = T, y = V1, group = Means, color = Means)) +
  geom_line() +
  labs(x="Time", y="Cumulative Reward of Chosen Arm") +
  ggtitle("Cumulative Reward")


# シミュレート結果
results <- fread(inputFileResults, header = F)
names(results) <- c("Means", "Arm", "Value", "Alpha", "Beta")
results <- transform(results, Means = factor(Means))

result_a <- ddply(results,
                 c("Means", "Arm"),
                 function (df) {mean(df$Alpha)})
m <- ggplot(result_a, aes(x = Means, y = V1, group = Means, color = Means)) +
  geom_boxplot() + 
  ylim(0, horizon) +
  labs(x="Arm", y="Alpha") +
  ggtitle("Result Alpha Counts")

result_b <- ddply(results,
                 c("Means", "Arm"),
                 function (df) {mean(df$Beta)})
n <- ggplot(result_b, aes(x = Means, y = V1, group = Means, color = Means)) +
  geom_boxplot() + 
  ylim(0, horizon) +
  labs(x="Arm", y="Beta") +
  ggtitle("Result Beta Counts")

result_value <- ddply(results,
                 c("Means", "Arm"),
                 function (df) {mean(df$Value)})
o <- ggplot(result_value, aes(x = Means , y = V1, group = Means, color = Means)) +
  geom_boxplot() + 
  ylim(0, 1) +
  labs(x="Arm", y="Value") +
  ggtitle("Result Values")


# 連結表示
library(grid)
library(gridExtra)

g <- arrangeGrob(x, a, b, c, d, o, m, n,
                 layout_matrix = rbind(
                   c(1, 1),
                   c(2, 3),
                   c(4, 5),
                   c(6, 6),
                   c(7, 8)
                 ),
                 top=caption)
print(g)
print(outputFile)
grid.draw(g)
ggsave(file=outputFile, g, dpi = 100, width = 14, height = 16)

