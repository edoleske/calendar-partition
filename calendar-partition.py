from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from statistics import median

''' TEST PARAMETERS '''
start_date = date(2016, 1, 4)
day_increments = [6,7,8,9,10]
years_to_test = 2

''' OUTPUT OPTIONS '''
range_detailed = False

def get_partition_data(start_date, day_increment, months_to_test=12):
    """
    Get partitions, length in days of date span, unnecessary days of each month given a start date and increment of n days
    :param start_date: datetime date where iteration starts
    :param day_increment: number of days date is incremented by
    :param months_to_test: numbers of months to test
    """
    partition_points = list()
    partition_data = list()
    end_date = start_date + relativedelta(months=+(months_to_test+2))

    # Propogate list with partition points
    i_date = start_date
    while i_date <= end_date:
        partition_points.append(i_date)
        i_date += timedelta(days=day_increment)

    target_month = (start_date + relativedelta(months=+1)).month
    range_begin = date(start_date.year, target_month, 1)
    range_end = range_begin + relativedelta(months=+1)

    encapsulating_begin = date.min
    encapsulating_end = date.max

    for month in range(months_to_test):
        # Inefficient
        for i in range(len(partition_points)):
            if partition_points[i] >= range_begin:
                encapsulating_begin = partition_points[i-1]
                break
        for i in range(len(partition_points)):
            if partition_points[i] >= range_end:
                encapsulating_end = partition_points[i]
                break

        partition_data.append({
            'range_begin': range_begin,
            'range_end': range_end,
            'front_partition_point': encapsulating_begin,
            'back_partition_point': encapsulating_end,
            'partition_count': (encapsulating_end - encapsulating_begin).days // day_increment,
            'day_length': (encapsulating_end - encapsulating_begin).days,
            'unnecessary_days': (range_begin - encapsulating_begin).days +
                                (encapsulating_end - range_end).days
        })

        # Increment month
        range_begin = range_end
        range_end = range_begin + relativedelta(months=+1)

    return partition_data

def get_averages(data):
    partition_nums = list()
    day_lengths = list()
    unnecessary_lengths = list()

    for entry in data:
        partition_nums.append(entry['partition_count'])
        day_lengths.append(entry['day_length'])
        unnecessary_lengths.append(entry['unnecessary_days'])

    return {
        'partition_average': sum(partition_nums) / len(partition_nums),
        'partition_min': min(partition_nums),
        'partition_max': max(partition_nums),
        'day_average': sum(day_lengths) / len(day_lengths),
        'unnecessary_average': sum(unnecessary_lengths) / len(unnecessary_lengths)
    }

''' FILE OUTPUT '''
with open('output-calendar-partition.txt', 'w') as f:
    for n in day_increments:
        data = get_partition_data(start_date, n, months_to_test=years_to_test*12)
        averages = get_averages(data)
        f.write(
            f'DAY INCREMENT {n}\n'
            f'Average partitions in pull: {averages["partition_average"]}\n'
            f'Partition Min\Max: {averages["partition_min"]} | {averages["partition_max"]}\n'
            f'Average day length of pull: {averages["day_average"]}\n'
            f'Average unnecessary days in pull: {averages["unnecessary_average"]}\n\n'
        )

        # More detailed analytics
        if range_detailed:
            for entry in data:
                f.write(
                    f'\tRANGE {entry["range_begin"]} - {entry["range_end"]}:\n'
                    f'\tPartition range: {entry["front_partition_point"]} - {entry["back_partition_point"]}\n'
                    f'\tPartitions, Days, Unnecessary Days: {entry["partition_count"]} | {entry["day_length"]} | {entry["unnecessary_days"]}\n\n'
                )
