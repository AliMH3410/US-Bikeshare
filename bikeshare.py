import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['January', 'February', 'March', 'April', 'May', 'June']

days = ['Saturday','Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
city = "none"
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input("Which city would you like to get data for: chicago, new york city, or washington?\n").lower())
    
    while city not in list(CITY_DATA.keys()):
        city = str(input("Invalid city name! Please, insert a valid name for the city you want to analyze for choosing from the listed cities.\n").lower())                 
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month = str(input("Please, insert the name of the month you want to analyze for (choose from months between January to June), or \"all\" for no month filter.\n").title())
    while month not in months:
        if month == "All":
            break
        month = str(input("Invalid month name! Please, insert a valid name for the month you want to analyze for(choose from months between January to June).\n").title()) 
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input("Please, insert the day you want to analyze for, or \"all\" for no day filter.\n").title())
    while day not in days:
        if day == "All":
            break
        day = str(input("Invalid day name! Please, insert a valid name for the day you want to analyze for.\n").title())
                         
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
    df['hour'] = df['Start Time'].dt.hour
    if month != 'All':
       month = months.index(month) + 1
       df = df[df['month'] == month]
    
    if day != 'All':
       df = df[df['day_of_week'] == day]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
  
    start_time = time.time()


    # TO DO: display the most common month


    most_common_month = df['month'].mode()[0]

    # TO DO: display the most common day of week

    most_common_day = df['day_of_week'].mode()[0]

    # TO DO: display the most common start hour

    most_common_hour = df['hour'].mode()[0]

    print("The most common month is: {}".format(most_common_month), "\nThe most common day is: {}".format(most_common_day), "\nThe most common hour is: {}".format(most_common_hour)) 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode().loc[0]


    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode().loc[0]


    # TO DO: display most frequent combination of start station and end station trip
    most_common_compination = df[['Start Station', 'End Station']].mode().loc[0]

    print("The most common start station is: {}".format(most_common_start_station), "\nThe most common end station is: {}".format(most_common_end_station), "\nThe most frequent compination of start station and end station trip is: Start station: {}, End station: {}".format(most_common_compination[0], most_common_compination[1]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_travel_time = df['Trip Duration'].sum()

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    
    print("The total travel time is: {}".format(tot_travel_time), "\ntThe mean travel time is: {}".format(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print("The counts of user types is:\n{}".format(counts_of_user_types)) 
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        counts_of_gender = df['Gender'].value_counts()
        print("\nThe counts of gender is:\n{}".format(counts_of_gender)) 


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earlist_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth is: {}".format(earlist_birth_year), "\nThe most recent year of birth is: {}".format(most_recent_birth_year), "\nThe most common year of birth is: {}".format(most_common_birth_year))

    # Display raw bikeshare data and iterate from 0 to the number of rows in steps of 5
    row_length = df.shape[0]
    for i in range(0, row_length, 5):
        display = input('\nWould you like to examine the particular user trip data? Type \'yes\' or \'no\'\n> ')
        if display.lower() != 'yes':
            break
        # retrieve and convert data to json format
        # split each json row data 
        rows = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for single_row in rows:
            # pretty print each user data
            desired_row = json.loads(single_row)
            json_row = json.dumps(desired_row, indent=2)
            print(json_row)
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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
