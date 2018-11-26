##---------------------------------
## STATS 506 Group Project
## Group 9: Cubic Spline Regression
## Author: Xiaotong Yang
## 11 / 18 / 2018
## -----------------------------

# Load data and package-----------------------------
library(splines)
library(faraway)
library(dplyr)
library(ggplot2)
data(uswages)

# Visualizing data-----------------------------
head(uswages)
summary(uswages)
ggplot(uswages, aes(exper, wage))+geom_point()

# Remove outliers-----------------------------
uswages = filter(uswages, wage<4000)

#fit OLS and Polynomial regression models-----------------------------
fit1 = lm(wage~exper, data = uswages)
plot(uswages$exper, uswages$wage, xlab = "Weekly wage", 
     ylab = "Experience", main = "OLS model", col = "slategrey")
abline(fit1, col = "red")

g2 = lm(wage~poly(exper, 2), data = uswages)
g4 = lm(wage~poly(exper, 4), data = uswages)
uswages = mutate(uswages, degree2 = fitted(g2), degree4 = fitted(g4))

ggplot(uswages, aes(exper, wage)) +
  geom_point( col = "slategrey") + 
  geom_line(aes(exper, degree2,color = "2"))+
  geom_line(aes(exper, degree4,color = "4")) +
  scale_color_manual(values = c(
    '2' = 'darkblue',
    '4' = 'red')) +
  labs(color = 'Polynomial degree')+
  ggtitle("Polynomial regression models")

## Regression splines-----------------------------
cubic_spline = lm(wage~bs(exper, knots = c(0, 20, 40, 50, 60)), data = uswages)
uswages = mutate(uswages, smooth = fitted(cubic_spline))

ggplot(uswages, aes(exper, wage)) + 
  geom_point(col = "slategrey") +
  geom_line(aes(exper, smooth), col = "red") + 
  ggtitle("Cubic regression spline model")
