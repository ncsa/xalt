-- XALT 3.0.2 Modfile

-- Setting as sticky to bypass module purge on OOD launch script
add_property("lmod","sticky")


-- Get MMYYYY for XALT 
local currentDate = os.date("*t")
local month = string.format("%02d", currentDate.month)
local year = currentDate.year
local formattedDate = year .. month

-- Filepath used for current configuration of XALT
-- LOC local base  = "/sw/workload/xalt2/xalt/xalt"  --> Change to match your site!!!
local base  = "/u/csteffen/xalt_base/xalt2/xalt/xalt"  --> Change to match your site!!!
local bin   = pathJoin(base,"bin")
local pythonpath   = pathJoin(base,"site_packages")
local lib_dir = "/lib64" -- this is referenced to the internals of a container; doesn't need to be updated per local paths

-- LOC local record_dir  = "/sw/workload/delta/json"
local record_dir_base = "/u/csteffen/xalt_base/records"
local record_dir  = pathJoin(record_dir_base,"json")

-- Comma seperated as specified by https://apptainer.org/docs/user/main/bind_paths_and_mounts.html
-- LOC local apptainer_bind_dir = "/sw/workload/xalt2/xalt/xalt, /sw/workload/delta"
local apptainer_bind_dir = base..", "..record_dir_base


-- Turn on Module Tracking
setenv("XALT_EXECUTABLE_TRACKING",       "yes")

-- Environment variables for XALT to run on a Compute Node
prepend_path{"PATH",          bin, priority="100"}
prepend_path("XALT_DIR",      base)
prepend_path("LD_PRELOAD",    pathJoin(base, "lib64/libxalt_init.so"))
prepend_path("COMPILER_PATH", bin)

-- XAlT_DATE_TIME creation
setenv("XALT_FILE_PREFIX", pathJoin(record_dir,formattedDate))

-- XAlT_DATE_TIME creation
setenv("XALT_ALWAYS_CREATE_START", pathJoin(record_dir,formattedDate))


-- Variable needed for Python tracking outside a container 
prepend_path("PYTHONPATH",  pythonpath)


-- Variables needed for XALT to get included into containers
prepend_path("APPTAINER_BINDPATH", apptainer_bind_dir)
setenv("APPTAINERENV_LD_PRELOAD", pathJoin(base, lib_dir, "libxalt_init.so"))
setenv("APPTAINERENV_PYTHONPATH", pythonpath)


------------------------------------------------------------
-- Only set this in production not for testing!!!
-- setenv("XALT_SAMPLING",  "yes")

-- Uncomment this to track GPU usage
-- setenv("XALT_GPU_TRACKING",              "yes")

