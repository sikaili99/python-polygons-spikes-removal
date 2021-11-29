# Polygons spike removal application
A Python application to remove spike from polygons


## Description

This tool can be used to remove spikes from input geometries stored in
`geopackage` format. This is done by parsing the input geometry and evaluating
each set of three contigous vertices against an evaluating strategy and
removing from the output geometry the vertices that fail to pass the test.


## Example original gpkg file

![example original file](https://github.com/Mathewsmusukuma/python-polygons-spikes-removal/blob/main/images/spiky-original-gpkg.png?raw=true)



## Output of the gpkg file after running the tool

![example output file](https://github.com/Mathewsmusukuma/python-polygons-spikes-removal/blob/main/images/spiky-output-gpkg.png?raw=true)


## Installation

This tool single external dependency is [geopandas](https://geopandas.org/).

Installation of the `python-polygons-spike-removal` tool can be done by cloning this repository as follows:

```
$ git clone https://github.com/Mathewsmusukuma/python-polygons-spikes-removal.git
$ cd python-polygons-spikes-removal
$ pip install -r requirements.txt
```

## Usage

Simple example of using this tool to process a file:

```
$ python3  main.py -o data-file/spiky-output.gpkg data-file/spiky-polygons.gpkg
```
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

The tool accepts three diferent input arguments:

* `--angle`: The maximum angle, in degrees, that will be used to evaluate
triplets of vertices. If the triplet being evaluated forms an angle greater
than the value of `angle`, that triplet will never be marked as a spiked. The
value of `angle` defaults to 1.0º if not specified.

* `--distance`: The minimum distance, in meters, that one of the edges of the
triplet being evaluated must have for that triplet to be tested as a spike.
The value of `distance` defaults to 100 000 meters if not specified.

* `--output`: The output path where the processed geometry will be saved to.