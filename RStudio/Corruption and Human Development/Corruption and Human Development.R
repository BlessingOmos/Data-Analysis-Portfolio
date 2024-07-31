#import ggplot2
library('ggplot2')

#use read to load csv file and save it in a dataframe called df
df <- read.csv('Economist_Assignment_Data.csv')

#check the first 6 lines
head(df)

#use ggplot() + geom_point() to create scatter plot 
pl <- ggplot(data=df,aes(x=CPI, y=HDI, color=Region))
pl + geom_point(shape=1, size=4)

#make changes to plot:
#add shape and size to geom_point

#add trend line with:
#geom_smooth(aes(group=1))
pl + geom_point(shape=1, size=4) + geom_smooth(aes(group=1), method='lm', formular=y~log(x), se=FALSE, color='red')

#assign to another variable (pl2) to make easier
pl2 <- pl + geom_point(shape=1, size=4) + geom_smooth(aes(group=1), method='lm', formular=y~log(x), se=FALSE, color='red')

#add text with geom_text
pl2 + geom_text(aes(label=Country))

#select countries we want to label
pointsToLabel <- c("Russia", "Venezuela", "Iraq", "Myanmar", "Sudan",
                   "Afghanistan", "Congo", "Greece", "Argentina", "Brazil",
                   "India", "Italy", "China", "South Africa", "Spane",
                   "Botswana", "Cape Verde", "Bhutan", "Rwanda", "France",
                   "United States", "Germany", "Britain", "Barbados", "Norway", "Japan",
                   "New Zealand", "Singapore")
pl3 <- pl2 + geom_text(aes(label = Country), color = "gray20", 
                       data = subset(df, Country %in% pointsToLabel),check_overlap = TRUE)

#add theme 
pl4 <- pl3 + theme_bw()

#add scale_x_continuous and scale_y_continuous with arguments
pl5 <- pl4 + scale_x_continuous(name='Corruption Perceptions Index, 2011 (10=least corrupt)',
                         limits = c(.9, 10.5), breaks=1:10)

pl6 <- pl5 + scale_y_continuous(name='Human Development Index, 2011 (1=Best)',
                         limits = c(.2, 1.0))
pl6 + ggtitle('Corruption and Human development')
