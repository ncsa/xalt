![XALT Logo](https://github.com/xalt/xalt/raw/main/logos/XALT_Sticker.png)

[![Documentation Status](https://readthedocs.org/projects/xalt/badge/?version=latest)](https://xalt.readthedocs.io/en/latest/?badge=latest)
## Synopsis

XALT is a lightweight software tool for any Linux cluster,
workstation, or high-end supercomputer to track executable information
and linkage of static shared and dynamically linked libraries. When
the code is executed, wrappers intercept both GNU linker (ld) to capture
linkage information and environmental variables.

## Creators

Dr. Mark Fahey  
Dr. Robert McLay

## Motivation

We wanted to be able to answer the questions: what software do
researchers actually use on high-end computers, and how successful are
they in their efforts to use it?  With the information that xalt
collects, high-end computer administrators can answer our questions by
tracking continuous job-level information to learn what products
researchers do and do not need.  Drilling down to data driven usage
statistics helps stakeholders conduct business in a more efficient,
effective, and systematic way.


## Original Documentation

Installation and Use of XALT is provided at https://xalt.readthedocs.io website.


## NCSA SPIN Summer 2024 Documentation
This is a fork of XALT for the NCSA. This was developed as a project in the SPIN Summer 2024 cohort by Prakhar Gupta.

### Current Configuration on Delta

XALT is currently located in `/sw/workload/` on Delta. The source (this repository) is in `/sw/workload/xalt2/xalt_src` and the executables are in `/sw/workload/xalt2/xalt`.

Each build of XALT requires a configuration file. The configuration file is [Delta_config.py](https://github.com/ScreamingPigeon/xalt/blob/main/Config/Delta_Config.py).

Relevant information on configuring XALT can be found 
- [Downloading XALT and Configuring it for your site](https://xalt.readthedocs.io/en/latest/020_site_configuration.html)
- [Running Configure and building XALT for your site](https://xalt.readthedocs.io/en/latest/050_install_and_test.html) 
- [XALT's Environment Variables](https://xalt.readthedocs.io/en/latest/095_xalt_env_vars.html)

The script used to build xalt on Delta can be found at [`ncsa_build/build_xalt.sh`](https://github.com/ScreamingPigeon/xalt/blob/main/ncsa_build/build_xalt.sh).
The important bit is that XALT is configured to dump files into `/sw/workload/delta/json`. The LMOD reverse map it uses to match paths to modules is in `/sw/workload/delta/process_xalt`.

This configuration of XALT is further supplemented by the modulefile in use. 



#### Currently Implemented 
   

### Python CLI Tool


### How does XALT work


### Major Changes













