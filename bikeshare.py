import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please specify a city from chicago, new york city, washington:')
    city = city.casefold()
    while city not in CITY_DATA:
        city = input('Invalid inputs! Please specify a city from chicago, new york city, washington:')
        city = city.casefold()


    # get user input for month (all, january, february, ... , june)
    months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    month = input('Please specify the month from january to june or Enter "all" for no month filter:')
    month = month.casefold()
    while month not in months:
        month = input('Invalid inputs! Please specify the month from january to june or Enter "all" for no month filter:')
        month = month.casefold()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    day = input('Please specify the day from monday to sunday or Enter "all" for no day filter:')
    day = day.casefold()
    while day not in days:
        day = input('Invalid inputs! Please specify the day from monday to sunday or Enter "all" for no day filter:')
        day = day.casefold()
    


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1    
        df = df[df['month'] == month]
                                      
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
                                      
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('The most common month is:', months[most_common_month-1])
    
    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    most_common_day = df['day_of_week'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print('The most common day of week is:', days[most_common_day])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is:', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station is: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['most_frequent combination'] = (df['Start Station'] + '-' + df['End Station'])
    print('Most frequent combination of start station and end station trip is', df['most_frequent combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Trip Time:', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean Trip Time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:    
        gender = df['Gender'].value_counts()
        print(gender,'\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth:', df['Birth Year'].min())
        print('Most Recent year of birth:', df['Birth Year'].max())
        print('Most Common year of birth:', df['Birth Year'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        x = ['yes', 'no']
        
        while view_data.lower() not in x:
            view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
            view_data = view_data.lower()
        start_loc = 0
        while True:
            if view_data.lower() == 'yes':
                print(df.iloc[start_loc:start_loc + 5])
                start_loc += 5
                view_data = input("Do you wish to continue?: ").lower()
            else:
                break
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thanks for using!")
            break


if __name__ == "__main__":
	main()
