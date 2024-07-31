#import packages 
library(ggplot2)
library(dplyr)
library(plotly)
library(viridisLite)
library(viridis)
library(writexl)
library(forcats)
library(gridExtra)

#import csv file 
salary <- read.csv('salary_data.csv')

#overview of data 
head(salary)
glimpse(salary)
str(salary)
summary(salary)

#check for null values
any(is.na(salary))

# Histogram of highest salary 
p1 <- ggplot(salary, aes(x = highest_salary)) +
  geom_histogram(binwidth = 1000, fill = "maroon", color = "black") +
  theme_minimal() +
  labs(title = "Distribution of Highest Salaries", x = "Highest Salary", y = "Frequency")

# Histogram of average salary
p2 <- ggplot(salary, aes(x = average_salary)) +
  geom_histogram(binwidth = 500, fill = "maroon", color = "black") +
  theme_minimal() +
  labs(title = "Distribution of Average Salaries", x = "Average Salary", y = "Frequency")

#Histogram of lowest salary 
p3 <- ggplot(salary, aes(x = lowest_salary)) +
  geom_histogram(binwidth = 200, fill = 'maroon', color = 'black') +
  theme_minimal() +
  labs(title = "Distribution of Lowest Salaries", x = "Lowest Salary", y = "Frequency")

#Histogram of median salary
p4 <- ggplot(salary, aes(x = median_salary)) +
  geom_histogram(binwidth = 1000, fill = 'maroon', color = 'black') +
  theme_minimal() + 
  labs(title = "Distribution of Median Salaries", x = "Median Salary", y = "Frequency")

# Arrange the plots
grid.arrange(p1, p2, p3, p4, ncol = 2)


#Highest & least paid countries 
least_paid <- salary %>% 
  arrange(lowest_salary) %>%
  mutate(country_name = fct_reorder(country_name, desc(lowest_salary))) %>%
  slice(1:10)

pl1 <- ggplot(least_paid, mapping = aes(x = country_name, y = lowest_salary, fill = continent_name)) +
  geom_col() +
  geom_text(aes(label = scales::dollar(round(lowest_salary, 1))), nudge_y = 3) +
  scale_y_continuous(labels = scales::dollar_format(), limits = c(0, 50)) +
  xlab("Country") + ylab("Lowest Salary") +
  labs(title = "Top 10 Least Paid Countries", fill = "Continent") +
  guides(x = guide_axis(angle = 45)) +
  scale_fill_manual(values = c("Asia" = "yellow3", "South America" = "skyblue3", "Africa" = "darkgreen"))

#Highest paid salary countries 
highest_paid <- salary %>% 
  arrange(desc(highest_salary)) %>%
  mutate(country_name = fct_reorder(country_name, highest_salary)) %>%
  slice(1:10)

pl2 <- ggplot(highest_paid, mapping = aes(x = country_name, y = highest_salary, fill = continent_name)) +
  geom_col() +
  geom_text(aes(label = scales::dollar(round(highest_salary, 0))), nudge_y = 5000) +
  scale_y_continuous(labels = scales::dollar_format()) +
  xlab("Country") + ylab("Highest Salary") +
  labs(title = "Top 10 Highest Paid Countries", fill = "Continent") +
  guides(x = guide_axis(angle = 45)) +
  scale_fill_manual(values = c("Asia" = "yellow3", "Europe" = "darkblue", "Northern America" = "red2"))

grid.arrange(pl1, pl2, ncol = 1)



#Salary Standard Deviation NOT SURE
#Calculate deviation from the continent's average salary for each country
salary <- salary %>% 
  group_by(continent_name) %>%
  mutate(average_salary_mean = mean(average_salary),
         salary_standard_deviation_from_continent = average_salary - average_salary_mean,
         continent_salary_std = sd(average_salary)) %>%
  ungroup()

#Define thresholds as 2 standard deviation from the mean 
low_threshold <- -2 * mean(salary$continent_salary_std)
high_threshold <- 2 * mean(salary$continent_salary_std)

#Countries with salaries significantly lower than continent's average
low_salary_countries <- salary %>%
  filter(salary_standard_deviation_from_continent < low_threshold)

#Countries with salaries significantly higher than their continent's average 
high_salary_countries <- salary %>%
  filter(salary_standard_deviation_from_continent > high_threshold)
#Scatter plot of salary deviation from continent's average 
sd <- ggplot(salary, mapping = aes(x = salary_standard_deviation_from_continent, y = average_salary, color = continent_name)) +
  geom_point(size = 3) +
  geom_vline(xintercept = low_threshold, linetype = "dashed", color = "red") +
  geom_vline(xintercept = high_threshold, linetype = "dashed", color = "green") +
  labs(title = "Salary Deviation from Continent's Average", x = "Deviation from Continent's Average Salary", y = "Average Salary") +
  theme_minimal() +
  theme(legend.title = element_blank())

sd #NOT SURE

#Scatterplot 
sd2 <- plot_ly(
  data = salary,
  x = ~average_salary,
  y = ~country_name,
  type = 'scatter',
  mode = 'markers',
  marker = list(color = ~salary_standard_deviation_from_continent, colorscale = 'RdBu', showscale = TRUE),
  text = ~paste("Country:", country_name, "<br>Average Salary:", average_salary, "<br>Deviation:", salary_standard_deviation_from_continent),
  hoverinfo = 'text'
)

# Customize the appearance of the plot
sd2 <- sd2 %>%
  layout(
    title = 'Salary Standard Deviation by Country',
    xaxis = list(title = 'Average Salary'),
    yaxis = list(title = 'Country'),
    coloraxis = list(colorbar = list(title = 'Salary Deviation'))
  )

# Show the interactive plot
sd2

#Median salaries by continent 
ms_con <- ggplot(salary, mapping = aes(x = continent_name, y = median_salary, fill = continent_name)) +
  geom_boxplot() +
  labs(title = "Distribution of Median Salaries by Continent", x = "Continent", y = "Median Salary", fill = "Continent name") +
  guides(x = guide_axis(angle = 45))
  theme_minimal()
  
#Average salaries by continent
av_con<- ggplot(salary, mapping = aes(x = continent_name, y = average_salary, fill = continent_name)) +
  geom_boxplot() +
  labs(title = "Distribution of Average Salaries by Continent", x = "Continent", y = "Average Salary", fill = "Continent name") +
  guides(x = guide_axis(angle = 45))
theme_minimal()

#Highest salaries by continent 
hs_con<- ggplot(salary, mapping = aes(x = continent_name, y = highest_salary, fill = continent_name)) +
  geom_boxplot() +
  labs(title = "Distribution of Highest Salaries by Continent", x = "Continent", y = "Highest Salary", fill = "Continent name") +
  guides(x = guide_axis(angle = 45))
theme_minimal()

#Lowest salaries by continent 
ls_con<- ggplot(salary, mapping = aes(x = continent_name, y = lowest_salary, fill = continent_name)) +
  geom_boxplot() +
  labs(title = "Distribution of Lowest Salaries by Continent", x = "Continent", y = "Lowest Salary", fill = "Continent name") +
  guides(x = guide_axis(angle = 45))
theme_minimal()

grid.arrange(ms_con, av_con, hs_con, ls_con, ncol = 2)



