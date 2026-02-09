# Data Foundry for Predictive Machine Learning

This repository contains scripts and code for curating datasets for benchmarking predictive machine learning.
The data foundry defines a common **schema for curating datasets and metadata** to enable their usage in 
benchmarking. Moreover, the foundry shares scripts that reproduce the exact steps of how we went from raw
data to curated benchmarking datasets and task.

The curation scripts and metadata stored in this repository are primarily intended for preparing datasets
and benchmark tasks. These datasets and task can then be ingested (if possible) by third party data registries,
such as [OpenML](https://www.openml.org/), or used offline as local tasks. 

The schema we propose is aligned as much as possible with OpenML's dataset and task schema, but we had to add several
new features that are not natively supported by OpenML so far. Furthermore, our schema and this repository extends 
the curation efforts of [TabArena-v0.1](https://github.com/TabArena/tabarena_dataset_curation) and aims to be the 
place-to-be for future data curation of TabArena and the tabular community. 

## Structure

* `datasets/`: Contains the curation scripts and metadata for each dataset and task. It aims to contain the curation 
  efforts from various collections (such as TabArena-v0.1 and newer benchmarking datasets).
* `local-data-warehouse/`: Functions a local space to store local copies of data. This is where curators can store raw
  data, intermediate data, and final curated artifacts.
* `src/data_foundry`: Contains the package that defines the schema definition for datasets and tasks. Moreover, it 
  contains utilities to help with the curation process.

## Install

To install the required dependencies, run:

```bash
uv pip install -e .
```

For all dev dependencies, run:

```bash
uv pip install -e ".[dev,tests]"
```
