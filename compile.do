#====================================================================================
# UVVM Light compile script
#
# Compiled to library uvvm_util
#
# Default output directory is /sim and can be changed by passing an existing 
# direcotry as argument to this script.
#
#====================================================================================




#-------------------------------------------------------
# Setup
#
#   This section will try to setup the script for 
#   running on Modelsim and Riviera Pro simulators.
#
#-------------------------------------------------------

#
# Define library name, UVVM Util path and BFM path.
#
quietly set library_name uvvm_util
quietly set util_path src_util
quietly set bfm_path src_bfm


#
# Overload quietly (Modelsim specific command) to let it work in Riviera-Pro
#
proc quietly { args } {
  if {[llength $args] == 0} {
    puts "quietly"
  } else {
    # this works since tcl prompt only prints the last command given. list prints "".
    uplevel $args; list;
  }
}


#
# Detect simulator
#
if {[catch {eval "vsim -version"} message] == 0} {
  quietly set simulator_version [eval "vsim -version"]

  if {[regexp -nocase {modelsim} $simulator_version]} {
    quietly set simulator "modelsim"
  } elseif {[regexp -nocase {aldec} $simulator_version]} {
    quietly set simulator "rivierapro"
  } else {
    puts "Unknown simulator. Attempting to use Modelsim commands."
    quietly set simulator "modelsim"
  }
} else {
    puts "vsim -version failed with the following message:\n $message"
    abort all
}


#
# Set compilation directives for Modelsim / Riviera Pro
#
if { [string equal -nocase $simulator "modelsim"] } {
  quietly set compdirectives "-quiet -suppress 1346,1236,1090 -2008 -work $library_name"
} elseif { [string equal -nocase $simulator "rivierapro"] } {
  set compdirectives "-2008 -nowarn COMP96_0564 -nowarn COMP96_0048 -dbg -work $library_name"
}


#
# Set compile directory: 
#   no argument - compile directory is set to /sim
#   user argument - compile directory is set to user argument 
#
if { $argc > 0 } {
  quietly set target "$1/$library_name"
} else {
  quietly set target "sim/$library_name"
}


#-------------------------------------------------------
# Compile UVVM Util
#
#    This section compiles UVVM Util to library uvvm_util.
#    Target directory (compile directory) is /sim or
#    user specified if script is called with argument.
#
#-------------------------------------------------------
echo "\n\n\n=== Compiling UVVM Util to directory: $target\n"

quietly vlib $target
quietly vmap $library_name $target


echo "eval vcom $compdirectives $util_path/types_pkg.vhd"
eval vcom $compdirectives $util_path/types_pkg.vhd

echo "eval vcom $compdirectives $util_path/adaptations_pkg.vhd"
eval vcom $compdirectives $util_path/adaptations_pkg.vhd

echo "eval vcom $compdirectives $util_path/string_methods_pkg.vhd"
eval vcom $compdirectives $util_path/string_methods_pkg.vhd

echo "eval vcom $compdirectives $util_path/protected_types_pkg.vhd"
eval vcom $compdirectives $util_path/protected_types_pkg.vhd

echo "eval vcom $compdirectives $util_path/global_signals_and_shared_variables_pkg.vhd"
eval vcom $compdirectives $util_path/global_signals_and_shared_variables_pkg.vhd

echo "eval vcom $compdirectives $util_path/hierarchy_linked_list_pkg.vhd"
eval vcom $compdirectives $util_path/hierarchy_linked_list_pkg.vhd

echo "eval vcom $compdirectives $util_path/alert_hierarchy_pkg.vhd"
eval vcom $compdirectives $util_path/alert_hierarchy_pkg.vhd

echo "eval vcom $compdirectives $util_path/license_pkg.vhd"
eval vcom $compdirectives $util_path/license_pkg.vhd

echo "eval vcom $compdirectives $util_path/methods_pkg.vhd"
eval vcom $compdirectives $util_path/methods_pkg.vhd

echo "eval vcom $compdirectives $util_path/bfm_common_pkg.vhd"
eval vcom $compdirectives $util_path/bfm_common_pkg.vhd

echo "eval vcom $compdirectives $util_path/uvvm_util_context.vhd"
eval vcom $compdirectives $util_path/uvvm_util_context.vhd



#-------------------------------------------------------
# Compile BFMs
#
#    This section compiles UVVM BFMs to library uvvm_util.
#    Target directory (compile directory) is /sim or
#    user specified if script is called with argument.
#
#-------------------------------------------------------
echo "\n\n\n=== Compiling UVVM BFMs to directory: $target\n"

#
# Search for all VHD files in /src_bfm folder.
#
quietly set vhd_files [glob -directory "$bfm_path/" -- "*.vhd"]


#
# Compile all VHD files found in the /src_bfm folder.
#
foreach vhd_file $vhd_files {
  echo "eval vcom $compdirectives  $vhd_file"
  eval vcom $compdirectives  $vhd_file
}
