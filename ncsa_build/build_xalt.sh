#! /bin/bash

module_name=xalt

if module is-loaded $module_name; then
        module --force unload $module_name
fi

orig_dir=$PWD

echo "Verifying Directory"
cd /sw/workload

dir=$PWD
process_xalt_dir="${dir}/delta/process_xalt"
xalt_dir="${dir}/xalt2"
config_file=Config/Delta_Config.py

## Cloning XALT
cd $xalt_dir
echo "Cloning XALT"
git clone https://github.com/ncsa/xalt/ xalt_src

rm xalt_src/Config/*

cp ${orig_dir}/Config.py xalt_src/Config/


## Creating Reverse Mapping of Modules
echo "Creating Reverse Mapping"
$LMOD_DIR/spider -o xalt_rmapT      $MODULEPATH > ${process_xalt_dir}/reverseMapD/xalt_rmapT.json

echo "Reverse Map Created"

## Configuring XALT
echo "Configuring XALT"

echo $PWD

cd ${xalt_dir}/xalt_src

./configure --prefix=$xalt_dir                  \
--with-config=$config_file                      \
--with-syshostConfig=nth_name:2                 \
--with-transmission=file                        \
--with-xaltFilePrefix=${dir}/delta/json/        \
--with-MySQL=no                                 \
--with-cmdlineRecord=no                         \
--with-functionTracking=yes                     \
--with-etcDir=$process_xalt_dir

echo "Configuration Complete. Beginning Install now"
make install

if [ $? -eq 0 ]; then
        echo "Installation Complete. Loading module now"
        export MODULEPATH=$MODULEPATH:/sw/workload/xalt2/module
        module load $module_name
        module list
else
    echo "Install Failed"
fi

cd $orig_dir

