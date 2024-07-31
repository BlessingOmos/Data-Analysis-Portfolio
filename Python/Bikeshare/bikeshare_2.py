import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Ask user to specify a city, month, and day to analyze.

    Return:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
     
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()

        if city in cities:
            break
        else:
            print('Invalid input! Please type one of the following cities: Chicago, New York City or Washington.\n')

   
    # get user input for month (all, january, february, ... , june)
    while True:
       months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
       month = input('Would you like to see data for the month January, February, March, April, May, June or all?\n').lower()
      
       if month in months:
        break
       else:
        print('Invalid input! Please type one of the following months: January, February, March, April, May, June or all.\n')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        day = input('Would you like to see the data for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?\n').lower()

        if day in days:
            break
        else:
            print('Invalid input! Please type one of the following days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all.\n')

    print('-'*40)
    return city, month, day


def load_data(city, month, day): 
    """
    Load data for the specified city and filters by month and day if applicable.

    Arg:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Return:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
   
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def raw_data(df):
    """Displays 5 lines by request of user"""

    response = input('Would you like to see the first 5 lines of individual data? Yes or no?\n').lower()
    counter = 0

    while response == 'yes':
        counter += 5
        print(df.iloc[counter - 5: counter, :])
        response = input('Do you want to see the next 5 lines? Yes or no?\n').lower()


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        popular_month = df['month'].value_counts().idxmax()
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        print('Most frequent month is:', popular_month)
    
   
    # display the most common day of week
    if day == 'all':  
        popular_day_of_week = df['day_of_week'].value_counts().idxmax()
        print('Most frequent day is:', popular_day_of_week)


    # display the most common start hour
    popular_hour = df['hour'].value_counts().idxmax() 
    print('Most frequent start hour is:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('The most frequent start station is:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('The most frequent end hour is:', popular_end_station)


    # display most frequent combination of start station and end station trip
    frequent_station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most frequent start and end station:', frequent_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is:', total_travel_time)
    
    # display mean travel time
    trip_duration_stats = df['Trip Duration'].mean()
    print('The average travel time is:', trip_duration_stats)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user types are:\n',user_types)


    # Display counts of gender
    if 'Gender' in df.columns:
        print('The gender count is:\n{}'.format(df['Gender'].value_counts()))
    

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        popular_birth_year = int(df['Birth Year'].value_counts().idxmax())
        print('The earliest birth year is {}\nwhile the most recent birth year is {}\nand the most frequent birth year is {}.'.format(earliest_birth_year, most_recent_birth_year, popular_birth_year))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters() 
        
        df = load_data(city, month, day) 
        raw_data(df)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
