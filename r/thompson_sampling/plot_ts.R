library(plyr)
library(ggplot2)
library(data.table)

if (Sys.getenv("BASE_DIR") != "") {
  base_dir = Sys.getenv("BASE_DIR")
  file_format = Sys.getenv("SAVE_FORMAT")
  num_sims = strtoi(Sys.getenv("NUM_SIMS"))
  horizon = strtoi(Sys.getenv("HORIZON"))
} else {
  base_dir = "ts_results"
  num_sims = 100
  horizon = 10000
  mean_type = "random"
  datetime = "20161109_155317"
  file_format = sprintf("%s.%dx%d.%s", mean_type, horizon, num_sims, datetime)
}

caption = sprintf("Thompson Sampling (%d[horizon] x %d[simulates])", horizon, num_sims)
inputFileArms = sprintf("%s/%s.arms.tsv", base_dir, file_format)
inputFileSims = sprintf("%s/%s.sims.tsv", base_dir, file_format)
outputFile = sprintf("%s/%s.png", base_dir, file_format)

arms <- fread(inputFileArms, header = F)
names(arms) <- c("ArmNum", "BestArm", "Arm", "Mean", "Value", "Alpha", "Beta")
arms <- transform(arms, Name = factor(sprintf("%d arms[best:%d]", ArmNum, BestArm)))

sims <- fread(inputFileSims, header = F)
names(sims) <- c("ArmNum", "BestArm", "Sim", "T", "ChosenArm", "Reward", "CumulativeReward")
sims <- transform(sims, Name = factor(sprintf("%d arms[best:%d]", ArmNum, BestArm)))

# フィルタ
#arms <- subset(arms, ArmNum >= 50)
#sims <- subset(sims, ArmNum >= 50)

#-------------------------------
# 腕の尤度/結果
gr1 <- ggplot(arms, aes(x = Arm, y = Mean, group = Name, color = Name)) +
  geom_point() + 
  ylim(0, 1) +
  labs(x = "Arm", y = "Value") + 
  ggtitle("Means")

ra <- ddply(arms,
            c("Name", "Arm"),
            function (df) {mean(df$Alpha)})
gr2 <- ggplot(ra, aes(x = Arm, y = V1, group = Name, color = Name)) +
  geom_line() + 
  ylim(0, horizon) +
  labs(x="Arm", y="Alpha") +
  ggtitle("Result Alpha Counts")

rb <- ddply(arms,
            c("Name", "Arm"),
            function (df) {mean(df$Beta)})
gr3 <- ggplot(rb, aes(x = Arm, y = V1, group = Name, color = Name)) +
  geom_line() + 
  ylim(0, horizon) +
  labs(x="Arm", y="Beta") +
  ggtitle("Result Beta Counts")

rv <- ddply(arms,
            c("Name", "Arm"),
            function (df) {mean(df$Value)})
gr4 <- ggplot(rv, aes(x = Arm, y = V1, group = Name, color = Name)) +
  geom_line() + 
  ylim(0, 1) +
  labs(x="Arm", y="Value") +
  ggtitle("Result Values")

#-------------------------------
# シミュレート結果
# Plot average reward as a function of time.
stats1 <- ddply(sims,
                c("Name", "T"),
                function (df) {mean(df$Reward)})
gs1 <- ggplot(stats1, aes(x = T, y = V1, group = Name, color = Name)) +
  geom_line() +
  ylim(0, 1) +
  labs(x="Time", y="Average Reward") +
  ggtitle("Performance")

# Plot frequency of selecting correct arm as a function of time.
# In this instance, 5 is the correct arm.
stats2 <- ddply(sims,
                c("Name", "T"),
                function (df) {mean(df$ChosenArm == df$BestArm)})
gs2 <- ggplot(stats2, aes(x = T, y = V1, group = Name, color = Name)) +
  geom_line() +
  ylim(0, 1) +
  labs(x="Time", y="Probability of Selecting Best Arm") +
  ggtitle("Accuracy")

# Plot variance of chosen arms as a function of time.
stats3 <- ddply(sims,
                c("Name", "T"),
                function (df) {var(df$ChosenArm)})
gs3 <- ggplot(stats3, aes(x = T, y = V1, group = Name, color = Name)) +
  geom_line() +
  labs(x="Time", y="Variance of Chosen Arm") +
  ggtitle("Variability")

# Plot cumulative reward as a function of time.
stats4 <- ddply(sims,
                c("Name", "T"),
                function (df) {mean(df$CumulativeReward)})
gs4 <- ggplot(stats4, aes(x = T, y = V1, group = Name, color = Name)) +
  geom_line() +
  labs(x="Time", y="Cumulative Reward of Chosen Arm") +
  ggtitle("Cumulative Reward")


# 連結表示
library(grid)
library(gridExtra)

g <- arrangeGrob(gr1, gs1, gs2, gs3, gs4, gr4, gr2, gr3,
                 layout_matrix = rbind(
                   c(1, 1),
                   c(2, 3),
                   c(4, 5),
                   c(6, 6),
                   c(7, 7),
                   c(8, 8)
                 ),
                 top=caption)
grid.draw(g)
ggsave(file=outputFile, g, dpi = 100, width = 14, height = 16)
print(outputFile)
