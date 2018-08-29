# jubilant-robot

## Description
[Insight Data Engineering Coding Challenge Fall 2018](https://github.com/InsightDataScience/prediction-validation)

Basically, compare two potentially-unequal lists of partially-ordered data,  compute the error between the two datasets for sliding windows and output the window errors with a particular format.

### Considerations
In writing the scipt for this challenge I decided to use pure python 3 with as few packages as possible. Since I have no way of knowing the size of the files to be read in I decided not to read the total files into memory before processing. 

### Method
Each file is simultaneously loaded line by line into memory; once a chunk of data representing one hour is loaded that chunk is processed. The data is discarded and file loading / processing continues until the end of the longest file is reached. In processing, the total error for each hour is computed as well as the number of stocks for that error.

When loading / processing is complete, the windows are determined and the average error is computed for each. When complete the window errors are written to disk.

#### Why load line by line?
I considered three alternatives: `numpy.genfromtxt`, `pandas.readcsv`, and using `open()` to read the whole file before processing.

Using Pandas seemed to be against the spirit of the "no database engines" stipulation.

Using `numpy.genfromtxt` turned out to be slower than using `open()`, I assume it is doing many checks and other things.

Using `open` to read the whole file before processing was considerably faster than my current method of processing during loading, but it required that the entire file be loaded into memory. 


## Requirements

Python 3 standard library, in particular these two packages are used:
```
itertools
unittest
```

## Running
To run the comparator navigate to `jubilant-robot/` and do:

`./run.sh`

## Testing
To run unittests navigate to `jubilant-robot/src` and do:

`python3 test_insight_processing.py`

Note:
- One of these tests will perform a full comparison on whatever files are in input, if these are long it may take some time.

To run the insight testsuite navigate to `jubilant-robot/insight_testsuite/` and do:

`run_tests.sh`

Note:
- due to rounding errors insight_testsuite tests may fail if off by 0.01, disregard these failures.
- these tests may take some time


