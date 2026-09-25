# Polygons spike removal application

A Python command-line tool to remove spikes from polygons.

## Description

This tool removes spikes from input geometries stored in `geopackage` format.
It parses the input geometry and evaluates each set of three contiguous
vertices against an evaluation strategy, removing from the output geometry the
vertices that fail the test.

## Example original gpkg file

![example original file](https://github.com/sikaili99/python-polygons-spikes-removal/blob/main/images/spiky-original-gpkg.png?raw=true)

## Output of the gpkg file after running the tool

![example output file](https://github.com/sikaili99/python-polygons-spikes-removal/blob/main/images/spiky-output-gpkg.png?raw=true)

## Installation

The main external dependency is [geopandas](https://geopandas.org/). Python
3.9 or newer is required.

Clone the repository and install into a virtual environment:

```
$ git clone https://github.com/sikaili99/python-polygons-spikes-removal.git
$ cd python-polygons-spikes-removal
$ python3 -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
```

## Usage

Simple example of using this tool to process a file:

```
$ python3  main.py -o data/spiky-output.gpkg data/spiky-polygons.gpkg

```

## Flowchart diagram for the algorithm for the spike removal application

![flowchart-spike-algorithm](https://user-images.githubusercontent.com/33897492/143893704-eaf3c378-e832-4eb2-b66b-f02a9d282a8b.png)


## To run tests

`pytest -v`


## Note

You can update the dataset in the data-file directory.

For more details run `python main.py --help`:

```
Usage: spike_removal [OPTIONS] FILENAME

  A command-line tool used to remove spikes from polygons stored in
  Geopackage format.

Options:
  --angle FLOAT      Maximum angle, in degrees, used to evaluate spikes.
                     Defaults to 1.0º.

  --distance FLOAT   Minimum distance, in meters, used to evaluate spikes.
                     Defaults to 100 000m

  -o, --output TEXT  Name of the output destination file  [required]
  --help             Show this message and exit.
```

The tool accepts three different input arguments:

* `--angle`: The maximum angle, in degrees, that will be used to evaluate
triplets of vertices. If the triplet being evaluated forms an angle greater
than the value of `angle`, that triplet will never be marked as a spiked. The
value of `angle` defaults to 1.0º if not specified.

* `--distance`: The minimum distance, in meters, that one of the edges of the
triplet being evaluated must have for that triplet to be tested as a spike.
The value of `distance` defaults to 100 000 meters if not specified.

* `--output`: The output path where the processed geometry will be saved to.
