#!/usr/bin/bash

orig_dir=$PWD
base_dir=/sw/workload

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

xalt_repo_dir=$(cd "$(dirname "$0")/.." && pwd)
config_file="$xalt_repo_dir/Config/Delta_Config.py"

git_repo=https://github.com/ncsa/xalt

git_branch=hung # Can change to main later after merge

module_name=xalt
module_ver=3.0.2

echo Unloading XALT module
module --force unload $module_name 2>/dev/null || true

if [ ${XALT_LOCAL_ONLY} ] ; then
    echo
    echo "XALT_LOCAL_ONLY set, using local (possibly modified) source and configurations"
    echo
else
    echo "Verifying Directory:$src_dir"
    if [ -d "$src_dir" ]; then
        echo "Directory exists. Updating now."
        cd $src_dir
        # git pull
        git fetch origin
        git checkout "$git_branch"
        git pull origin "$git_branch"
        cd $orig_dir
    else
        echo "source Directory does not exist; about to make build directory $build_dir"
        mkdir -p $build_dir
        cd $build_dir
        # git clone $git_repo $XALT_REPO_NAME
        git clone -b "$git_branch" "$git_repo" "$XALT_REPO_NAME"
        cd $orig_dir
    fi
fi

echo "Syncing Config and py_src from ${xalt_repo_dir}"
cp "$xalt_repo_dir/Config/Delta_Config.py" "$src_dir/Config/Delta_Config.py"
cp "$xalt_repo_dir/py_src/xalt_sitecustomize.py" "$src_dir/py_src/xalt_sitecustomize.py"

if [ ${XALT_SETUP_CHECK} ] ; then
    cd $src_dir
    ls -ld ./configure
    exit
fi

cd $src_dir
echo "Configuring XALT with config: $config_file"
./configure --prefix=$build_dir                 \
--with-config="$config_file"                  \
--with-syshostConfig=nth_name:2                 \
--with-transmission=file                        \
--with-xaltFilePrefix=$json_dir                 \
--with-MySQL=no                                 \
--with-cmdlineRecord=no                         \
--with-functionTracking=yes                     \
--with-etcDir=$rmap_dir

echo "Configuration Complete. Starting Install now"
make install

if [ $? -eq 0 ]; then
    echo "Installation Complete."
    chmod -R u+rwx,o+rx $build_dir/xalt
    mkdir -p $build_dir/module/xalt

    prefix_dir=$(dirname "$base_dir")
    xalt_install_base="$build_dir/xalt/xalt"
    log_repo_base="$prefix_dir/log_repo/delta"
    mkdir -p "$log_repo_base/json"

    module_template="$xalt_repo_dir/ncsa_build/${module_ver}.lua.in"
    if [ ! -f "$module_template" ]; then
        module_template="$xalt_repo_dir/ncsa_build/${module_ver}.lua"
    fi
    sed -e "s|@XALT_INSTALL_BASE@|${xalt_install_base}|g" \
        -e "s|@XALT_LOG_REPO@|${log_repo_base}|g" \
        "$module_template" > "$build_dir/module/xalt/$module_ver.lua"

    echo "Module written to: ${build_dir}/module/xalt/${module_ver}.lua"
    cp "$xalt_repo_dir/ncsa_build/build_xalt.sh" "$build_dir/build_xalt.sh"
else
    echo "Install Failed"
    echo "If you need to add include directories to make the build work, add them to CPATH"
fi

cd $orig_dir