DELIMITER = "|"

window = None
with open("../input/example_window.txt") as f:
    for line in f:
        line = line.strip()
        if window is None and line[0].isdigit():
            window = int(line[0])
            break

actual = []
with open("../input/example_actual.txt") as f:
    for i, line in enumerate(f):
        line = line.strip()
        if line:
            actual.append(line)

predicted = []
with open("../input/example_predicted.txt") as f:
    for i, line in enumerate(f):
        line = line.strip()
        if line:
            predicted.append(line)

def is_positive_float(s):
    return s.replace('.','',1).isdigit()



actual_stock_dict = {}
for line in actual:
    line = line.split(DELIMITER)

    stock = line[1]
    if line[0].isdigit() and is_positive_float(line[2]):
        if stock not in actual_stock_dict:
            actual_stock_dict[stock] = {int(line[0]): float(line[2])}
        else:
            actual_stock_dict[stock][int(line[0])] = float(line[2])

predicted_stock_dict = {}
for line in predicted:
    line = line.split(DELIMITER)

    stock = line[1]
    if line[0].isdigit() and is_positive_float(line[2]):
        if stock not in predicted_stock_dict:
            predicted_stock_dict[stock] = {int(line[0]): float(line[2])}
        else:
            predicted_stock_dict[stock][int(line[0])] = float(line[2])

error_dict = {}
for stock in predicted_stock_dict:
    for hour in predicted_stock_dict[stock]:
        if stock in actual_stock_dict:
            if hour in actual_stock_dict[stock]:
                error = abs(
                    actual_stock_dict[stock][hour] - predicted_stock_dict[stock][hour]
                )
                if stock not in error_dict:
                    error_dict[stock] = {hour: error}
                else:
                    error_dict[stock][hour] = error

hour_errors = {}
for stock in error_dict:
    for hour in error_dict[stock]:
        if hour not in hour_errors:
            hour_errors[hour] = error_dict[stock][hour], 1
        else:
            previous_error = hour_errors[hour]
            hour_errors[hour] = (
                previous_error[0] + error_dict[stock][hour],
                previous_error[1] + 1,
            )

unique_hours = {hour for hour in hour_errors}

window_hours = [
    range(hour, hour + window)
    for hour in unique_hours
    if hour + window - 1 in unique_hours
]

window_errors = {}

for i, hours in enumerate(window_hours):
    
    error = None
    count = None
    
    for hour in hours:
        
        if error is None and count is None:
            
            error = hour_errors[hour][0]
            count = hour_errors[hour][1]
            
        else:
            
            error += hour_errors[hour][0]
            count += hour_errors[hour][1]
            
    window_errors[i] = round(error / count, 2)

with open("../output/example_comparison.txt", mode="w") as f:
    for window in window_errors:
        line = "{}".format(window_hours[window][0]) + DELIMITER\
               + "{}".format(window_hours[window][-1]) + DELIMITER\
               + "{}".format(window_errors[window]) + "\n"
        f.write(line)