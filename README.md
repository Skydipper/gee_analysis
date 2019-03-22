# GEE Analysis endpoints

## Getting started

### Requirements

You need to install Docker in your machine if you haven't already [Docker](https://www.docker.com/)

### Development

Follow the next steps to set up the development environment in your machine.

1. Clone the repo and go to the folder

```ssh
git clone https://github.com/skydipper/gee-analysis.git
cd analysis-gee
```

2. Run the geeanalysis.sh shell script in development mode.

```ssh
./geeanalysis.sh develop
```

If this is the first time you run it, it may take a few minutes.

### Code structure

The API has been packed in a Python module (geeanalysis). It creates and exposes a WSGI application. The core functionality
has been divided in three different layers or submodules (Routes, Services and Models).

There are also some generic submodules that manage the request validations, HTTP errors and the background tasks manager.


### 
This microservice queries several GEE collections (i.e. Sentinel 2 and Landsat 8 collections), and returns every image in the collection for a given lat&lon pair, sorted by cloud coverage. These images can be used in png format; and they are scaled for visualization in RGB. The motivation for this is to provide samples from satellite imagery to a model training process, in a predefined grid (i.e. slippy tiles).

The main mode of functioning is to provide a natural color visualization of the bands (i.e., images constructed from the red, green, and blue channels), but any combination of three bands can be used. Use 
`https://api.skydipper.com/recent-tiles?lat=12&lon=27&start=2018-12-21&end=2019-03-22&bands=[B8,B11,B2]` for natural color tiles, and `https://api.skydipper.com/recent-tiles?lat=12&lon=27&start=2018-12-21&end=2019-03-22&bands=[B8,B11,B2]` for specifying the desired bands (bands are named B<number>, following the (Sentinel 2 band definition)[https://earth.esa.int/web/sentinel/user-guides/sentinel-2-msi/resolutions/spatial]).

This microservice is meant to be run in the context of the Skydipper API: please refer to developer.skydipper.com for more information on how to set up a local development environment. You'll need to provide your own credentials for Google Cloud Storage (which acts as the storage backend for any process) and to Google Earth Engine.
