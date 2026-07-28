#!/usr/bin/bash
# Load the local XALT test module (not the system /sw/workload install).
# Usage: source PREFIX_DIR/xalt/ncsa_build/load_local_xalt.sh PREFIX_DIR

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
xalt_repo_dir=$(cd "$script_dir/.." && pwd)

if [ $# -ge 1 ]; then
  prefix_dir=$(cd "$1" && pwd)
else
  prefix_dir=$(cd "$xalt_repo_dir/.." && pwd)
fi

module_dir="$prefix_dir/target/xalt2/module"

if [ ! -f "$module_dir/xalt/3.0.2.lua" ]; then
  echo "ERROR: local modulefile not found: $module_dir/xalt/3.0.2.lua" >&2
  return 1 2>/dev/null || exit 1
fi

module --force unload xalt 2>/dev/null || true
unset LD_PRELOAD PYTHONPATH XALT_DIR XALT_FILE_PREFIX XALT_ALWAYS_CREATE_START 2>/dev/null || true

export MODULEPATH="$module_dir${MODULEPATH:+:$MODULEPATH}"

module load util-linux-uuid
module load xalt

export LD_PRELOAD="$prefix_dir/target/xalt2/xalt/xalt/lib64/libxalt_init.so"

echo "Loaded local XALT from: $module_dir"
echo "  XALT_DIR=$XALT_DIR"
echo "  LD_PRELOAD=$LD_PRELOAD"
echo "  XALT_FILE_PREFIX=$XALT_FILE_PREFIX"