#!/bin/bash


# Check for UVVM Light installation path
if [ "$1" != "" ]; then
    SRC_PATH=$1
else
    SRC_PATH=".."
fi


echo "======================================================================="
echo "This script will compile UVVM Light using GHDL."
echo "Check if GHDL is set in the PATH variable if script is failing."
echo ""
echo "USAGE:"
echo "  compile.sh [src_path]"
echo ""
echo "NOTE:"
echo "  #1 Set the UVVM Light source path argument when calling"
echo "     the script from outside the uvvm_light/sim directory."
echo "  #2 Target path is always current working directory."
echo ""
echo "  Source path is: $SRC_PATH"
echo "  Target path is: $PWD"
echo ""
echo "======================================================================="
echo ""

compile_file()
{
echo "Running: $TARGT_PATH ghdl -a -frelaxed-rules --std=08 -Wno-hide -Wno-shared --work=uvvm_util $SRC_PATH/$part_path/$file_name"
ghdl -a -frelaxed-rules --std=08 -Wno-hide -Wno-shared --work=$COMPILE_LIB $SRC_PATH/$part_path/$file_name
}




# Compile UVVM Util
util_file_list='types_pkg.vhd
        adaptations_pkg.vhd
        string_methods_pkg.vhd 
        protected_types_pkg.vhd
        global_signals_and_shared_variables_pkg.vhd
        hierarchy_linked_list_pkg.vhd
        alert_hierarchy_pkg.vhd
        license_pkg.vhd
        methods_pkg.vhd
        bfm_common_pkg.vhd
        uvvm_util_context.vhd'

COMPILE_LIB="uvvm_util"

echo ""
echo "Compiling UVVM Utility Library..."

part_path="src_util"
for file_name in $util_file_list; do
    compile_file
done


# Compile UVVM BFMs

echo ""
echo "Compiling UVVM BFMs..."
bfm_file_list='avalon_mm_bfm_pkg.vhd
	      avalon_st_bfm_pkg.vhd
	      axilite_bfm_pkg.vhd
	      axistream_bfm_pkg.vhd
	      gmii_bfm_pkg.vhd
	      gpio_bfm_pkg.vhd
	      i2c_bfm_pkg.vhd
	      rgmii_bfm_pkg.vhd
	      sbi_bfm_pkg.vhd
	      spi_bfm_pkg.vhd
	      uart_bfm_pkg.vhd'

part_path="src_bfm"
for file_name in $bfm_file_list; do
    compile_file
done
