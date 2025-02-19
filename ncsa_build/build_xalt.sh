#!/usr/bin/bash

# Variables for build. Change as needed
orig_dir=$PWD
base_dir=/sw/workload

# set environment variable XALT_SETUP_CHECK to check that the target
# directory is working right, which will create the build directory,
# checkout source into it, check that the "configure" does in fact
# exist, then halt.  

# use this environment variable to put code in a new location
# for testing and whatnot
if [ ${XALT_BASE_DIRECTORY} ] ; then
    echo "taking base directory >${XALT_BASE_DIRECTORY}< from environment"
    base_dir="${XALT_BASE_DIRECTORY}"
fi
echo "base directory is: ${base_dir}"

XALT_REPO_NAME="xalt_src"

build_dir=$base_dir/xalt2
src_dir=$build_dir/${XALT_REPO_NAME}
rmap_dir=$base_dir/delta/process_xalt
json_dir=$base_dir/delta/json
config_file=Config/Delta_Config.py
git_repo=https://github.com/ncsa/xalt
module_name=xalt
module_ver=3.0.2

# Unloading module
echo Unloading XALT module
module --force unload $module_name

# Getting Latest Source
echo "Verifying Directory:$src_dir"
if [ -d "$src_dir" ]; then
        echo "Directory exists. Updating now."
        cd $src_dir
        git pull
        cd $orig_dir

else
        echo "source Directory does not exist; about to make build directory $build_dir"
	mkdir -p $build_dir
	echo "Made (successfully?), testing existence:"
	ls -ld $build_dir
	echo "verified existence, now go there and \"git clone\""
	cd $build_dir
        git clone $git_repo $XALT_REPO_NAME
	echo "checking that the git clone actually did something.  Running find:"
	find $XALT_REPO_NAME | wc -l	
fi

# Setting Source to read and execute
# chmod -R u=rwx,o=rx $src_dir

if [ ${XALT_SETUP_CHECK} ] ; then
    echo "checking XALT configuration (XALT_SETUP_CHECK is set)"
    cd $src_dir
    echo "I'm now in src_dir.  Check for configure:"
    ls -ld ./configure
    echo "checked for configure; exiting for testing."
    exit
    echo "should not get here!!!"
fi

cd $src_dir
echo "Configuring XALT"
./configure --prefix=$build_dir                 \
--with-config=$config_file                      \
--with-syshostConfig=nth_name:2                 \
--with-transmission=file                        \
--with-xaltFilePrefix=$json_dir                 \
--with-MySQL=no                                 \
--with-cmdlineRecord=no                         \
--with-functionTracking=yes                     \
--with-etcDir=$rmap_dir

# Install
echo "Configuration Complete. Starting Install now"
make install

if [ $? -eq 0 ]; then
        echo "Installation Complete." 
        chmod -R u+rwx,o+rx $build_dir/xalt
        echo "Updating Modulefile from source"
	echo "about to verify module directory exists"
	mkdir -p $build_dir/module/xalt
        cp $src_dir/ncsa_build/$module_ver.lua $build_dir/module/xalt/$module_ver.lua
        echo "Add ${base_dir}/module to MODULEPATH to begin using ${module_name}"
        cp $src_dir/ncsa_build/build_xalt.sh $build_dir/build_xalt.sh

else
    echo "Install Failed"
fi

cd $orig_dir
