"""bikeshare.py module"""

import time
from typing import List
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def check_input_validity(choice: str,
                         valid_list: List[str]
                         ) -> str:
    """
    This function checks if the input choice is in valid_list or not.
    If it's not in the valid_list it will continue asking user to enter the correct choice.

    Args:
        choice: The first choice of user
        valid_list: The valid list of different choices

    Returns:
        The valid input choice

    """
    while input_choice not in valid_list:
        input_choice = input('Invalid input. Please try another time: ').strip().casefold()
    return input_choice


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike-share data!')

    # City Info
    city = input('Would you like to get information for chicago, new york city,'
                 ' or washington\'s bike-shares?').strip().casefold()
    city = check_input_validity(city, list(CITY_DATA.keys()))

    # Month Info
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Enter the month ("January" to "June")'
                  ' or enter "all" if you need all information for all months: ').strip().casefold()
    month = check_input_validity(month, valid_months)

    # Day Info
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
                  'sunday']
    day = input('Enter the day ("monday" to "sunday")'
                ' or enter "all" if you need all information for all days: ').strip().casefold()
    day = check_input_validity(day, valid_days)

    print('-' * 40)
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

    # load data file into a dataframe
    data_df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    data_df['Start Time'] = pd.to_datetime(data_df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    data_df['month'] = data_df['Start Time'].dt.month
    data_df['day_of_week'] = data_df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        data_df = data_df[data_df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        data_df = data_df[data_df['day_of_week'] == day.title()]

    return data_df


def time_stats(data_df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # ################# Display the most common month#################
    # Creating a column named as month from the 'Start Time' column
    data_df['month'] = data_df['Start Time'].dt.month
    # Finding the most common month of the year from 1 to 12
    popular_month = data_df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    # printing the converted indexed month to the named month
    print(f"Most Popular Month:\n{months[popular_month - 1]}")

    # ################# Display the most common day of week#################
    # Creating a column named as dayofweek from the 'Start Time' column
    data_df['day_of_week'] = data_df['Start Time'].dt.dayofweek
    # Finding the most common day of the week from 0 to 6
    popular_day = data_df['day_of_week'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # printing the converted indexed day to the named day
    print(f"Most Popular Day:\n{days[popular_day]}")

    # ################# Display the most common start hour#################
    # Creating a column named as hour from the 'Start Time' column
    data_df['hour'] = data_df['Start Time'].dt.hour
    # Finding the most common hour from 0 to 23
    popular_hour = data_df['hour'].mode()[0]
    print(f"Most Popular Start Hour:\n{popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(data_df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"\nMost commonly used start station:\n{data_df['Start Station'].mode()[0]}")

    # display most commonly used end station
    print(f"\nMost commonly used end station:\n{data_df['End Station'].mode()[0]}")

    # display most frequent combination of start station and end station trip
    start_end_station = data_df['Start Station'] + ' TO ' + data_df['End Station']
    print(f"\nMost frequent combination of start and end station trips:\n"
          f"{start_end_station.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(data_df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displaying total travel time
    print(f"\nTotal travel time:\n{data_df['Trip Duration'].sum()}")

    # Displaying mean travel time
    print(f"\nMean travel time:\n{data_df['Trip Duration'].mean()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(data_df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying counts of user types
    print(f"\nCounts of user types:\n{data_df['User Type'].value_counts()}")

    # Displaying counts of gender
    if 'Gender' in data_df.columns:
        print(f"\nThe counts of gender:\n{data_df['Gender'].value_counts()}")
    else:
        print("\nThe dataset does not have Gender as a column. OOPS!!!")

    # Displaying earliest, most recent, and most common year of birth
    if 'Birth Year' in data_df.columns:
        print(f"\nEarliest year of Birth:\n{data_df['Birth Year'].min()}")
        print(f"\nMost Recent year of Birth:\n{data_df['Birth Year'].max()}")
        print(f"\nMost Common year of Birth:\n{data_df['Birth Year'].mode()[0]}")
    else:
        print("\nThe dataset does not have Birth Year as a column. OOPS!!!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        data = load_data(city, month, day)

        time_stats(data)
        station_stats(data)
        trip_duration_stats(data)
        user_stats(data)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
