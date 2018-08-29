
from argparse import ArgumentParser
from insight_processing import generate_output
from insight_processing import get_interval_errors
from insight_processing import get_window
from insight_processing import get_window_intervals
from insight_processing import process_input

parser = ArgumentParser()
parser.add_argument("filepaths", nargs="*", help="paths to files")

args = parser.parse_args()
filepaths = args.filepaths

window_fn = filepaths[0]  # "./input/window.txt"
actual_fn = filepaths[1]  # "./input/actual.txt"
predicted_fn = filepaths[2]  # "./input/predicted.txt"
output_fn = filepaths[3]  # "./output/comparison.txt"

window = get_window(window_fn)
hour_errors = process_input(actual_fn, predicted_fn)
window_intervals = get_window_intervals(window, hour_errors)
window_errors = get_interval_errors(window_intervals, hour_errors)
generate_output(window_intervals, window_errors, output_fn)
