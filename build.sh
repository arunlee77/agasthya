#!/bin/bash -e

confprefix="qemux86_64"
build_dir="build"

help="
Environment Initialization options
USAGE: $0 [-c <qemux86_64|qemuarm64|rasp_pi|rock_pi>] [-b <build directory>]
OPTIONS:
-c    Config options <qemux86_64|qemuarm64|rasp_pi|rock_pi>
-b    Build directory
-M    Machine
-h    Help
"
if [[ $1 == "" ]]; then
    echo "$help" && exit 1
fi

while getopts ":c:b:M:" opt; do
    case $opt in
        c)
	    confprefix=${OPTARG}
            ;;
	b)
	    build_dir=${OPTARG}
	    ;;
	M)
	    machine=${OPTARG}
	    ;;
        h)
            echo "$help" && exit 0
            ;;
        *)
            echo -e "\nERROR: unknown option: "$opt && echo "$help" && exit 1
            ;;
    esac
done
cd yocto
source ag-init-build-env $confprefix $build_dir $machine && echo
