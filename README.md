# Pytree

A containerized [Flask](http://flask.pocoo.org/) application serving potree to extract
height profile from [LiDAR](https://en.wikipedia.org/wiki/Lidar) data.

## Requirements

1. You will need [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) to run the application.

## Installation

First, clone [this repository](https://github.com/yverdon/pytree) on your machine.

```
git clone git@github.com:yverdon/pytree.git && cd pytree
```

If you need another version of [CPotree](https://github.com/potree/CPotree/releases/tag/0.2), extract its release files (namely `extract_profile` and `liblaszip.so`) into `./bin` and make the file `extract_profile` actually executable:

```
chmod +x extract_profile
```

Otherwise, you can simply directly use the `bin/` folder provided in this repos. Credit goes to [M. Schuetz](https://github.com/m-schuetz).

Then, create your `.env` file with a `DEPLOY_ENV` variable set to either `DEV`
or `PROD`, a `PORT` variable specify which port of your host machine you want to use,
and a `DATA_DIR` variable containing the absolute path to the directory containing
your `metadata.json` file for your Potree LiDAR tiles (generated using [PotreeConvert](https://github.com/potree/PotreeConverter) v2.x.x).  
Check `.env.sample` for inspiration.

Thirdly, copy `example_config.yml` to `pytree.yml` and make sure to adapt the variable to your environment.
Especially adapt the following four variables:

- log_folder
- cpotree_executable
- pointclouds
- default_point_cloud

Finally run the 2 following commands:

```
docker-compose down --remove-orphans -v
docker-compose up --build
```

## Usage

The application runs at http://localhost:6001/pytree

Please chek [https://github.com/potree/CPotree/blob/master/README.md](https://github.com/potree/CPotree/blob/master/README.md) for a comprehensive list of valid URL parameters to get a LiDAR profile.

You can also [start a shell](https://docs.docker.com/engine/reference/commandline/exec/) to further explore inside the running container and play around with the executable:

```
docker exec -it pytree_api_1 bash
```

Then execute `extract_profile`:

```
extract_profile data/processed/metadata.json -o "stdout" --coordinates "{2525528.12,1185781.87},{2525989.37,1185541.87}" --width 10 --min-level 0 --max-level 5 > data/output/test.las
```
