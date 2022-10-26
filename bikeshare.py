import time
import pandas as pd
import numpy as np
from pathlib import Path  # tip to import csv files faster and better
import calendar  # for access to month, day names etc
import sys
from termcolor import colored, cprint  # for some color


class bcolors:  # also for some color
    FAIL = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ['C', 'N', 'W']
    cprint('Hello! Let\'s explore some US bikeshare data!', 'yellow', attrs=['bold'])
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('What city? C for Chicago, N for New York City or W for Washington \n').upper()
            #if city == 'C' or city == 'N' or city == 'W':
            if city in cities:
                break
            elif city.isdigit():
                cprint('Enter the letter C, N or W not a number', 'magenta')
            else:
                print(bcolors.FAIL + 'Only the first letter')
        except ValueError:
            print(bcolors.FAIL + 'Somethings gone wrong here')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input(
                'What month? enter the number for the month, eg 1 for January, 6 for June. Or \'all\' for no filter. \n').lower()
            if month in ['1','2', '3', '4', '5','6', 'all']:
                   # == '1' or month == '2' or month == '3' or month == '4' or month == '5' or month == '6':
                break
            else:
                print(
                    bcolors.FAIL + 'You can only type numbers 1-6 or all. This statistic can not show data for July to December')
        except ValueError:
            print(bcolors.FAIL + 'This input only accept 1-6 or the word all')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input(
                'What day of week? enter the number for the weekday where Monday is 1 and Sunday 7. Or \'all\' for no filter. \n')
            if day in ['1', '2', '3', '4', '5', '6', '7', 'all']:
                break
            elif day.lower() == 'all':
                break
            else:
                print(bcolors.FAIL + 'You can only type numbers 1-7 or all.')
        except ValueError:
            print(bcolors.FAIL + 'This input only accept 1-7 or the word all')

    print('-' * 40)
    return city.upper(), month, day


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
    filepath = Path(__file__)  # this not part of course, got tip from friend
    data = {
        "W": Path(f"{filepath.parent}/washington.csv"),
        "C": Path(f"{filepath.parent}/chicago.csv"),
        "N": Path(f"{filepath.parent}/new_york_city.csv"),
    }

    df = pd.read_csv(data[city].as_posix())

    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d')

    if month != "all":
        month_filter = df["Start Time"].dt.month == int(month)
        df = df.loc[month_filter]
    if day != "all":
        day_filter = df["Start Time"].dt.weekday + 1 == int(day)
        df = df.loc[day_filter]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    cprint('\nCalculating The Most Frequent Times of Travel...\n', 'blue', attrs=['bold'])
    start_time = time.time()

    # display the most common month
    # using calendar that has built in functionality for names. using f for easier string composing instead of format
    most_common_month = calendar.month_name[int(df["Start Time"].dt.month.mode())]
    print(bcolors.BOLD + f'The most common month was: ' + bcolors.ENDC + f'{most_common_month}')

    # display the most common day of week
    most_common_day = calendar.day_name[int(df["Start Time"].dt.day_of_week.mode())]
    print(bcolors.BOLD + f'The most common day of the week was: ' + bcolors.ENDC + f'{most_common_day}')

    # display the most common start hour
    most_common_hour = f'{df["Start Time"].dt.hour.mode().to_string(index=False)}:00'  # this to string index false removes first column
    print(bcolors.BOLD + f'The most common start hour was: ' + bcolors.ENDC + f'{most_common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    cprint('\nCalculating The Most Popular Stations and Trip...\n', 'blue', attrs=['bold'])
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df["Start Station"].mode().to_string(index=False)
    print(bcolors.BOLD + f'Most common station was: ' + bcolors.ENDC + f'{most_common_start}')

    # display most commonly used end station
    most_common_end = df["End Station"].mode().to_string(index=False)
    print(bcolors.BOLD + f'Most common end station was: ' + bcolors.ENDC + f'{most_common_end}')

    # display most frequent combination of start station and end station trip
    start, end = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print(
        bcolors.BOLD + f'Most frequent combination of start and end station was: ' + bcolors.ENDC + f'{start} - {end}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    cprint('\nCalculating Trip Duration...\n', 'blue', attrs=['bold'])
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')

    total = (df['End Time'] - df['Start Time']).sum()
    print(bcolors.BOLD + f'Total travel time was: ' + bcolors.ENDC + f'{total}')

    # display mean travel time
    mean = (df['End Time'] - df['Start Time']).mean()
    print(bcolors.BOLD + f'Mean travel time was: ' + bcolors.ENDC + f'{mean}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    cprint('\nCalculating User Stats...\n', 'blue', attrs=['bold'])
    start_time = time.time()

    try:
        # Display counts of user types
        count_usertypes = df['User Type'].value_counts()
        print(bcolors.BOLD + 'User Types' + bcolors.ENDC)
        print(count_usertypes.to_string())
    except KeyError:
        print("No user type data to display.")

    print("\n")

    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()
        print(bcolors.BOLD + 'Gender' + bcolors.ENDC)
        print(count_gender.to_string())
    except KeyError:
        print("No gender data to display.")

    print("\n")

    try:
        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df["Birth Year"].min())
        most_recent_year = int(df["Birth Year"].max())
        most_common_year = int(df["Birth Year"].mode())
        print(
            bcolors.BOLD + 'Earliest Birth Year: ' + bcolors.ENDC + f'{earliest_year}\n' + bcolors.BOLD + 'Most recent Birth Year: ' + bcolors.ENDC + f'{most_recent_year}\n' + bcolors.BOLD + 'Most common birth year:' + bcolors.ENDC + f'{most_common_year}')
    except KeyError:
        print("No Birth Year Data to display.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    global view_display
    view_data = input(colored('\nDo you also want to see some raw data? Type yes, or just hit enter for no\n', 'blue',
                              attrs=['bold']))
    index = 0
    while view_data:
        try:
            if view_data == 'yes' or view_data == 'y':
                print(df.iloc[index:index + 5])
                index += 5
                view_display = input("Do you wish to continue?: ").lower()
            if view_display == 'no':
                break
        except:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        cprint('This is the result', 'yellow', attrs=['bold'])

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input(
            colored('\nThat\'s it, type yes for restart, or no to end the programme\n', 'blue', attrs=['bold']))
        if restart.lower() != 'yes':
            print('\n Welcome back at anytime')
            break


if __name__ == "__main__":
    main()