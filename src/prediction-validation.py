
from argparse import ArgumentParser
from itertools import zip_longest

parser = ArgumentParser()
parser.add_argument("filepaths", nargs="*", help="paths to files")

args = parser.parse_args()
filepaths = args.filepaths

window_fn = filepaths[0]  # "./input/window.txt"
actual_fn = filepaths[1]  # "./input/actual.txt"
predicted_fn = filepaths[2]  # "./input/predicted.txt"
output_fn = filepaths[3]  # "./output/comparison.txt"

DELIMITER = "|"
VALS_PER_LINE = 3


def split(line, delimiter=DELIMITER):
    """splist line at delimiter
    
    Args:
        line (str): string to split
        delimiter (str, optional): where to split string

    Returns:
        list of str: string split at N delimiters into N+1 strings
    
    Raises:
        ValueError: Exception if split fails for any reason
        ValueError: Exception if too many delimiters
    """
    try:
        line = line.split(delimiter)
    except:
        raise ValueError("Split failed for unknown reason, wrong delimiter?")

    if len(line) > VALS_PER_LINE:
        raise ValueError("line had too many delimiters")
    else:
        return line


def str_to_int(s):
    """get int value for s

    Args:
        s (str): str to convert to int
    
    Returns:
        int: s converted from str to int
    
    Raises:
        ValueError: Exception if s cannot be interpreted as integer
    """

    if s.isdigit():
        s = int(s)
        return s
    else:
        raise ValueError("Cannot interpret str as int")


def get_price(s):
    """get price value for s

    Assumes s is price in format $.cents

    Args:
        s (str): str to convert to float
    
    Returns:
        float: s converted from str to float
    
    Raises:
        ValueError: Description
    """
    sign = 1
    if s[0] == "-":
        sign = -1
        s = s[1:]
    if s.replace(".", "", 1).isdigit():
        s = sign * float(s)
        return s
    else:
        raise ValueError("Cannot interpret price as float")


def format_line(line):
    """formats line for processing

    Assumes line has format idsdf
        - i is int, d is delimiter, s is str, f is float
    
    Args:
        line (str): item to process
    
    Returns:
        [int, str, float]: formatted line
    """
    line = split(line)
    line[0] = str_to_int(line[0])
    line[2] = get_price(line[2])

    return line


def get_hour_error(actual, predicted, current_hour):
    """get error value for an hour

    Looks at the subdicts in actual and predicted which have the same keys (hour values)
    and computes the absolute error for each stock in predicted for the given current_hour.
    
    Args:
        actual (dict of dicts): keys are stocks, subkeys are hours
        predicted (dict of dicts): keys are stocks, subkeys are hours
        current_hour (int): hour to get error for
    
    Returns:
        tuple of floats: Total hour error, number of stocks for this error
    """
    errors = {}
    hour = current_hour

    for stock in predicted:
        if hour in predicted[stock]:
            if stock in actual:
                if hour in actual[stock]:
                    error = abs(predicted[stock][hour] - actual[stock][hour])
                    errors[stock] = error

    hour_errors = (sum(errors.values()), len(errors.keys()))

    return hour_errors


def del_hour_from_dict(d, hour):
    """deletes subdicts from d that have key = hour
    
    Note: deletes in place

    Args:
        d (dict of dicts): dicts to delete subdicts from
        hour (int): key to use for deletion
    """
    for stock in d:
        if hour in d[stock]:
            del d[stock][hour]


def process_input(fn_actual, fn_predicted):
    """loads files line by line into dicts of dicts, computes error hour by hour.
    Deletes subdicts as it goes to reduce memory footprint
    
    Assumes "predicted" file has less than or same number of lines as "actual" file.
    Assumes order of hours in increasing in both files.

    Args:
        fn_actual (str): name of "actual" file
        fn_predicted (str): name of "predicted" file
    
    Returns:
        dict: errors for each hour in "predicted" file
    """

    with open(fn_actual) as f_actual, open(fn_predicted) as f_predicted:

        current_hour = None

        actual = {}
        predicted = {}
        hour_errors = {}

        # itertools.zip_longest appends None to the shorter list until they are equal length

        for actual_line, predicted_line in zip_longest(f_actual, f_predicted):

            actual_line = actual_line.strip()

            if actual_line:

                actual_hour, actual_stock, actual_price = format_line(actual_line)

                # do not assume the starting hour is anything in particular
                if current_hour is None:
                    current_hour = actual_hour

                # add actual line to dict
                if actual_stock not in actual:
                    actual[actual_stock] = {actual_hour: actual_price}
                else:
                    actual[actual_stock][actual_hour] = actual_price

            # likely that f_predicted is shorter than f_actual so check for line before stripping
            predicted_line = predicted_line.strip() if predicted_line else None

            if predicted_line:

                predicted_hour, predicted_stock, predicted_price = format_line(
                    predicted_line
                )

                # add predicted line to dict
                if predicted_stock not in predicted:
                    predicted[predicted_stock] = {predicted_hour: predicted_price}
                else:
                    predicted[predicted_stock][predicted_hour] = predicted_price

            # process data on hour switch
            if actual_hour > current_hour:

                hour_errors[current_hour] = get_hour_error(
                    actual, predicted, current_hour
                )

                # remove processed hour from dicts to save on RAM
                # (for 200MB files this cuts RAM by >75% on my system)
                del_hour_from_dict(actual, current_hour)
                del_hour_from_dict(predicted, current_hour)

                current_hour = actual_hour

        # must process the last hour separately
        current_hour = actual_hour
        hour_errors[current_hour] = get_hour_error(actual, predicted, current_hour)

        del actual, predicted

    return hour_errors


def get_window_intervals(window, hour_errors):
    """get all the window intervals for a given window  size and range of hours
    
    Args:
        window (int): length of window interval
        min_hour (int): lower bound for intervals
        max_hour (int): upper bound for intervals
    
    Returns:
        list of range(): window intervals
    """
    hours = hour_errors.keys()
    max_hour = max(hours)
    min_hour = min(hours)

    if window <= (max_hour - min_hour + 1):
        all_hours = range(min_hour, max_hour + 1)
        window_hours = [
            range(hour, hour + window)
            for hour in all_hours
            if hour + window - 1 in all_hours
        ]
        return window_hours
    else:
        raise ValueError("Window is larger than data breadth")


def get_interval_errors(window_intervals, hour_errors):
    """get the error for each interval
    
    Args:
        hour_errors (dict):  errors for each hour in "predicted" file
        
    Returns:
        dict: keys are index of window_interval, values are interval errors
    """

    window_errors = {}

    for i, hours in enumerate(window_intervals):

        error = 0
        count = 0

        for hour in hours:
            if hour in hour_errors:
                error += hour_errors[hour][0]
                count += hour_errors[hour][1]

        if count == 0:
            window_errors[i] = "NA"
        else:
            window_errors[i] = round(error / count, 2)
    return window_errors


def format_interval_error(error, interval):
    """format interval error for writing
    
    Args:
        error (float or str): error for this interval
        interval (range()): interval for this error
    
    Returns:
        str: interval error formatted for writing
    """
    if isinstance(error, float):
        error_str = "{:.2f}".format(error)

    else:
        error_str = error

    line = (
        "{}".format(interval[0])
        + DELIMITER
        + "{}".format(interval[-1])
        + DELIMITER
        + error_str
        + "\n"
    )
    return line


def generate_output(window_intervals, window_errors, output_fn):
    """format comparison and write to file
    
    Args:
        window_intervals (TYPE): Description
        window_errors (TYPE): Description
        output_fn (TYPE): Description
    """
    with open(output_fn, mode="w") as f:

        for window in window_errors:

            error = window_errors[window]
            interval = window_intervals[window]

            line = format_interval_error(error, interval)

            f.write(line)


def get_window(window_fn):
    window = None
    with open(window_fn) as f:
        for line in f:
            line = line.strip()
            if line:
                window = str_to_int(line)
                break

    if window is not None:
        return window
    else:
        raise ValueError("Bad window")


window = get_window(window_fn)
hour_errors = process_input(actual_fn, predicted_fn)
window_intervals = get_window_intervals(window, hour_errors)
window_errors = get_interval_errors(window_intervals, hour_errors)
generate_output(window_intervals, window_errors, output_fn)

