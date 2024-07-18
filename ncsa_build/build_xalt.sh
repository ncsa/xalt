#! /bin/bash

module_name=xalt

if module is-loaded $module_name; then
        module --force unload $module_name
fi

orig_dir=$PWD

echo "Changing directories"
cd /sw/workload

dir=$PWD
process_xalt_dir="${dir}/delta/process_xalt"
xalt_dir="${dir}/xalt2"
src_dir="${xalt_dir}/xalt_src"
git_src="https://github.com/ncsa/xalt"
rmap_dir=:"${process_xalt_dir}/reverseMapD/xalt_rmapT.json"
config_file="${src_dir}/Config/Delta_Config.py"

# TODO Automate versioning
init_modpath="${src_dir}/ncsa_build/3.0.2.lua"
final_modpath="${xalt_dir}/module/xalt/3.0.2.lua"

if [- d "$src_dir"]; then
        echo "Source exists. Updating now"
        cd $src_dir
        git pull
        cd ..
else
        echo "Source does not exist. Cloning now"
        git clone $src_dir 
fi


## Creating Reverse Mapping of Modules
echo "Creating Reverse Mapping"
$LMOD_DIR/spider -o xalt_rmapT      $MODULEPATH > ${rmap_dir}

echo "Reverse Map Created"

## Configuring XALT
echo "Configuring XALT"

echo $PWD

cd $src_dir

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
        cp $init_modpath $final_modpath
        export MODULEPATH=$MODULEPATH:/sw/workload/xalt2/module
        module load $module_name
        module list
else
    echo "Install Failed"
fi

cd $orig_dir

