import unittest

import insight_processing as ip


#           _ _ _
#           | (_) |
#  ___ _ __ | |_| |_
# / __| '_ \| | | __|
# \__ \ |_) | | | |_
# |___/ .__/|_|_|\__|
#     | |
#     |_|
class test_split(unittest.TestCase):
    def test_delimiter_is_pipe(self):

        line = "1,NASDAQ,1234.56"
        self.assertRaises(ValueError, ip.split, line, "|")

    def test_makes_three_strs(self):

        line = "1|NAS|DAQ|1234.56"
        self.assertRaises(ValueError, ip.split, line, "|")

    def test_makes_correct_output(self):

        line = "1|NASDAQ|1234.56"
        split_line = ["1", "NASDAQ", "1234.56"]
        self.assertEqual(split_line, ip.split(line, "|"))


#      _        _         _       _
#     | |      | |       (_)     | |
#  ___| |_ _ __| |_ ___   _ _ __ | |_
# / __| __| '__| __/ _ \ | | '_ \| __|
# \__ \ |_| |  | || (_) || | | | | |_
# |___/\__|_|   \__\___/ |_|_| |_|\__|
#         ______     ______
#        |______|   |______|
class test_str_to_int(unittest.TestCase):
    def test_with_str_float(self):

        s = "1."
        self.assertRaises(ValueError, ip.str_to_int, s)

    def test_with_str_str(self):

        s = "one"
        self.assertRaises(ValueError, ip.str_to_int, s)

    def test_with_str_Nan(self):

        s = "nan"
        self.assertRaises(ValueError, ip.str_to_int, s)

    def test_with_str_None(self):

        s = "None"
        self.assertRaises(ValueError, ip.str_to_int, s)

    def test_with_str_bool(self):

        s = "True"
        self.assertRaises(ValueError, ip.str_to_int, s)

    def test_str_int_makes_correct_output(self):

        s = "100_000_000_000_000"
        self.assertEqual(100_000_000_000_000, ip.str_to_int(s))


#             _                  _
#            | |                (_)
#   __ _  ___| |_     _ __  _ __ _  ___ ___
#  / _` |/ _ \ __|   | '_ \| '__| |/ __/ _ \
# | (_| |  __/ |_    | |_) | |  | | (_|  __/
#  \__, |\___|\__|   | .__/|_|  |_|\___\___|
#   __/ |      ______| |
#  |___/      |______|_|
class test_get_price(unittest.TestCase):
    def test_with_str_str(self):

        s = "one"
        self.assertRaises(ValueError, ip.get_price, s)

    def test_with_str_Nan(self):

        s = "nan"
        self.assertRaises(ValueError, ip.get_price, s)

    def test_with_str_None(self):

        s = "None"
        self.assertRaises(ValueError, ip.get_price, s)

    def test_with_str_bool(self):

        s = "True"
        self.assertRaises(ValueError, ip.get_price, s)

    def test_str_negative_float_makes_correct_input(self):
        s = "-100_000_000_000_000.00"
        self.assertEqual(-100_000_000_000_000.00, ip.get_price(s))

    def test_str_float_makes_correct_output(self):

        s = "100_000_000_000_000.00"
        self.assertEqual(100_000_000_000_000.00, ip.get_price(s))


#   __                           _     _ _
#  / _|                         | |   | (_)
# | |_ ___  _ __ _ __ ___   __ _| |_  | |_ _ __   ___
# |  _/ _ \| '__| '_ ` _ \ / _` | __| | | | '_ \ / _ \
# | || (_) | |  | | | | | | (_| | |_  | | | | | |  __/
# |_| \___/|_|  |_| |_| |_|\__,_|\__| |_|_|_| |_|\___|
#                                 ______
#                                |______|
class test_format_line(unittest.TestCase):
    def test_makes_correct_output(self):

        line = "1|NASDAQ|-1234.56"
        self.assertEqual([1, "NASDAQ", -1234.56], ip.format_line(line))


#            _     _       _             _    _ _
#           | |   | |     | |           | |  | (_)
#   __ _  __| | __| |  ___| |_ ___   ___| | _| |_ _ __   ___
#  / _` |/ _` |/ _` | / __| __/ _ \ / __| |/ / | | '_ \ / _ \
# | (_| | (_| | (_| | \__ \ || (_) | (__|   <| | | | | |  __/
#  \__,_|\__,_|\__,_| |___/\__\___/ \___|_|\_\_|_|_| |_|\___|
#                 ______
#                |______|
class test_add_stockline_to_dict(unittest.TestCase):
    def test_add_to_empty_dict(self):

        d = {}
        line = "1|NASDAQ|-1234.56"
        hour, stock, price = ip.format_line(line)
        ip.add_stockline_to_dict(d, hour, stock, price)
        d_true = {stock: {hour: price}}
        self.assertEqual(d, d_true)

    def test_add_multiple_to_dict(self):

        d = {}
        line_1 = "1|NASDAQ|-1234.56"
        hour, stock, price = ip.format_line(line_1)
        ip.add_stockline_to_dict(d, hour, stock, price)
        d_true = {stock: {hour: price}}

        line_2 = "2|ABCDEF|789.10"
        hour, stock, price = ip.format_line(line_2)
        ip.add_stockline_to_dict(d, hour, stock, price)
        d_true[stock] = {hour: price}

        self.assertEqual(d, d_true)


#             _     _
#            | |   | |
#   __ _  ___| |_  | |__   ___  _   _ _ __ ___ _ __ _ __ ___  _ __
#  / _` |/ _ \ __| | '_ \ / _ \| | | | '__/ _ \ '__| '__/ _ \| '__|
# | (_| |  __/ |_  | | | | (_) | |_| | | |  __/ |  | | | (_) | |
#  \__, |\___|\__| |_| |_|\___/ \__,_|_|  \___|_|  |_|  \___/|_|
#   __/ |      ______                ______
#  |___/      |______|              |______|
#
class test_get_hour_error(unittest.TestCase):
    def test_makes_correct_output(self):

        example_actual = [
            "1|SLKWVA|94.51",
            "1|CMWTQH|81.27",
            "1|ATAYJP|25.74",
            "1|HVIWZR|22.81",
            "2|ATAYJP|29.62",
            "2|SLKWVA|81.87",
            "2|CMWTQH|116.11",
            "2|HVIWZR|22.15",
            "3|ATAYJP|21.93",
            "3|HVIWZR|22.24",
            "3|SLKWVA|78.01",
            "3|CMWTQH|113.63",
        ]

        example_predicted = [
            "1|ATAYJP|25.71",
            "1|HVIWZR|22.80",
            "1|SLKWVA|94.49",
            "1|CMWTQH|81.22",
            "2|ATAYJP|29.92",
            "2|HVIWZR|22.06",
            "3|ATAYJP|21.84",
            "3|HVIWZR|22.36",
            "3|SLKWVA|79.49",
        ]

        actual = [ip.format_line(line) for line in example_actual]
        acutal_dict = {}
        for line in actual:
            hour, stock, price = line[0], line[1], line[2]
            ip.add_stockline_to_dict(acutal_dict, hour, stock, price)

        predicted = [ip.format_line(line) for line in example_predicted]
        predicted_dict = {}
        for line in predicted:
            hour, stock, price = line[0], line[1], line[2]
            ip.add_stockline_to_dict(predicted_dict, hour, stock, price)

        current_hour = 1
        hour_1_error = ip.get_hour_error(acutal_dict, predicted_dict, current_hour)
        hour_1_error_true = (0.11, 4)

        self.assertAlmostEqual(hour_1_error[0], hour_1_error_true[0])
        self.assertEqual(hour_1_error[1], hour_1_error_true[1])


#      _      _   _
#     | |    | | | |
#   __| | ___| | | |__   ___  _   _ _ __
#  / _` |/ _ \ | | '_ \ / _ \| | | | '__|
# | (_| |  __/ | | | | | (_) | |_| | |
#  \__,_|\___|_| |_| |_|\___/ \__,_|_|
#            ______
#           |______|
class test_del_hour_from_dict(unittest.TestCase):
    def test_deletes_in_place(self):

        d = {}
        line = "1|NASDAQ|-1234.56"
        hour, stock, price = ip.format_line(line)
        ip.add_stockline_to_dict(d, hour, stock, price)
        ip.del_hour_from_dict(d, hour)
        d_true = {stock: {}}
        self.assertEqual(d, d_true)


#                                      _                   _
#                                     (_)                 | |
#  _ __  _ __ ___   ___ ___  ___ ___   _ _ __  _ __  _   _| |_
# | '_ \| '__/ _ \ / __/ _ \/ __/ __| | | '_ \| '_ \| | | | __|
# | |_) | | | (_) | (_|  __/\__ \__ \ | | | | | |_) | |_| | |_
# | .__/|_|  \___/ \___\___||___/___/ |_|_| |_| .__/ \__,_|\__|
# | |                             ______      | |
# |_|                            |______|     |_|
#
class test_process_input(unittest.TestCase):
    def test_operates_without_failure(self):
        """better testing using insight testtuite"""
        try:
            hour_errors = ip.process_input(
                "../input/actual.txt", "../input/predicted.txt"
            )
        except ExceptionType:
            self.fail("process_input raised ExceptionType unexpectedly!")


#             _            _           _
#            | |          (_)         | |
#   __ _  ___| |___      ___ _ __   __| | _____      __
#  / _` |/ _ \ __\ \ /\ / / | '_ \ / _` |/ _ \ \ /\ / /
# | (_| |  __/ |_ \ V  V /| | | | | (_| | (_) \ V  V /
#  \__, |\___|\__| \_/\_/ |_|_| |_|\__,_|\___/ \_/\_/
#   __/ |      ______
#  |___/      |______|
class test_get_window(unittest.TestCase):
    def test_operates_without_failure(self):
        try:
            hour_errors = ip.get_window("../input/window.txt")
        except ExceptionType:
            self.fail("get_window raised ExceptionType unexpectedly!")


#           _           _               _       _                       _
#          (_)         | |             (_)     | |                     | |
# __      ___ _ __   __| | _____      ___ _ __ | |_ ___ _ ____   ____ _| |___
# \ \ /\ / / | '_ \ / _` |/ _ \ \ /\ / / | '_ \| __/ _ \ '__\ \ / / _` | / __|
#  \ V  V /| | | | | (_| | (_) \ V  V /| | | | | ||  __/ |   \ V / (_| | \__ \
#   \_/\_/ |_|_| |_|\__,_|\___/ \_/\_/ |_|_| |_|\__\___|_|    \_/ \__,_|_|___/
#                                  ______
#                                 |______|
class test_get_window_intervals(unittest.TestCase):
    def test_with_zero(self):

        hour_errors = {1: (0.5, 2), 2: {0.1, 5}}
        window = 0
        self.assertRaises(ValueError, ip.get_window_intervals, window, hour_errors)

    def test_with_window_larger_than_data_breadth(self):

        hour_errors = {1: (0.5, 2), 2: {0.1, 5}}
        window = 3

        self.assertRaises(ValueError, ip.get_window_intervals, window, hour_errors)

    def test_makes_correct_output(self):

        hour_errors = {1: (0.5, 2), 100: {0.1, 5}}
        window = 98
        window_intervals = ip.get_window_intervals(window, hour_errors)
        window_intervals_true = [range(1, 99), range(2, 100), range(3, 101)]

        self.assertEqual(window_intervals, window_intervals_true)


#  _       _                       _
# (_)     | |                     | |
#  _ _ __ | |_ ___ _ ____   ____ _| |  ___ _ __ _ __ ___  _ __ ___
# | | '_ \| __/ _ \ '__\ \ / / _` | | / _ \ '__| '__/ _ \| '__/ __|
# | | | | | ||  __/ |   \ V / (_| | ||  __/ |  | | | (_) | |  \__ \
# |_|_| |_|\__\___|_|    \_/ \__,_|_| \___|_|  |_|  \___/|_|  |___/
#                                 ______
#                                |______|
class test_get_interval_errors(unittest.TestCase):
    def test_makes_correct_output(self):

        hour_errors = {1: (0.5, 2), 5: (0.1, 5)}

        window = 2
        window_intervals = ip.get_window_intervals(window, hour_errors)
        interval_errors = ip.get_interval_errors(window_intervals, hour_errors)
        interval_errors_true = {0: 0.5 / 2, 1: "NA", 2: "NA", 3: 0.1 / 5}

        self.assertEqual(interval_errors, interval_errors_true)


#   __                           _
#  / _|                         | |
# | |_ ___  _ __ _ __ ___   __ _| |_   ___ _ __ _ __ ___  _ __
# |  _/ _ \| '__| '_ ` _ \ / _` | __| / _ \ '__| '__/ _ \| '__|
# | || (_) | |  | | | | | | (_| | |_ |  __/ |  | | | (_) | |
# |_| \___/|_|  |_| |_| |_|\__,_|\__| \___|_|  |_|  \___/|_|
#                                 ______
#                                |______|
class test_format_interval_error(unittest.TestCase):
    def test_makes_correct_output(self):

        interval = range(1, 100)
        error = 2
        formatted_interval_error = ip.format_interval_error(error, interval)
        formatted_interval_error_true = "1|99|2.00\n"

        self.assertEqual(formatted_interval_error, formatted_interval_error_true)

        interval = range(1, 2)
        error = 3.14
        formatted_interval_error = ip.format_interval_error(error, interval)
        formatted_interval_error_true = "1|1|3.14\n"

        self.assertEqual(formatted_interval_error, formatted_interval_error_true)

        interval = range(1, 3)
        error = "NA"
        formatted_interval_error = ip.format_interval_error(error, interval)
        formatted_interval_error_true = "1|2|NA\n"

        self.assertEqual(formatted_interval_error, formatted_interval_error_true)


#                                  _                    _               _
#                                 | |                  | |             | |
#   __ _  ___ _ __   ___ _ __ __ _| |_ ___   ___  _   _| |_ _ __  _   _| |_
#  / _` |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \ / _ \| | | | __| '_ \| | | | __|
# | (_| |  __/ | | |  __/ | | (_| | ||  __/| (_) | |_| | |_| |_) | |_| | |_
#  \__, |\___|_| |_|\___|_|  \__,_|\__\___| \___/ \__,_|\__| .__/ \__,_|\__|
#   __/ |                               ______             | |
#  |___/                               |______|            |_|
#
class test_generate_output(unittest.TestCase):
    def test_operates_without_failuer(self):

        hour_errors = {1: (0.5, 2), 5: (0.1, 5)}

        window = 2

        window_intervals = ip.get_window_intervals(window, hour_errors)
        interval_errors = ip.get_interval_errors(window_intervals, hour_errors)

        try:
            ip.generate_output(
                window_intervals, interval_errors, "../output/comparison.txt"
            )
        except:
            self.fail("generate_output failed unexpectely")


if __name__ == "__main__":
    unittest.main()
