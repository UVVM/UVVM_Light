#====================================================================================
# UVVM Light compile script
#
# Compiled to library uvvm_util
#
# Default output directory is /sim and can be changed by passing an existing
# direcotry as argument to this script.
#
#====================================================================================

#
# Define library name, UVVM Util path and BFM path.
#
quietly set library_name uvvm_util
quietly set util_path src_util
quietly set bfm_path src_bfm



#-------------------------------------------------------
# Setup
#
#   This section will try to setup the script for
#   running on Modelsim and Riviera Pro simulators.
#
#-------------------------------------------------------

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




#-----------------------------------------------------------------------
# This file may be called with 0 to 2 arguments:
#
#   0 args: script is called from uvvm_light/sim folder.
#   1 args: directory for uvvm_light is specified,
#           target will be current directory.
#   2 args: directory for uvvm_light is specified
#           and target directory specified.
#-----------------------------------------------------------------------
if { [info exists 1] } {
  quietly set source_path "$1"

  if {$argc == 1} {
    echo "\nUser specified uvvm_light directory"
    quietly set target_path "."
    quietly set source_path "$1"
  } elseif {$argc >= 2} {
    echo "\nUser specified uvvm_light and target directory"
    quietly set source_path "$1"
    quietly set target_path "$2"
  }
  unset 1
} else {
  echo "\nDefault output directory"
  quietly set source_path ".."
  quietly set target_path "$source_path/sim"
}

quietly vlib $target_path/$library_name
quietly vmap $library_name $target_path/$library_name



#-------------------------------------------------------
# Compile UVVM Util
#
#    This section compiles UVVM Util to library uvvm_util.
#    Target directory (compile directory) is /sim or
#    user specified if script is called with argument.
#
#-------------------------------------------------------
echo "\n\n\n=== Compiling UVVM Util to directory: $target_path\n"

echo "eval vcom $compdirectives $source_path/$util_path/types_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/types_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/adaptations_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/adaptations_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/string_methods_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/string_methods_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/protected_types_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/protected_types_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/global_signals_and_shared_variables_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/global_signals_and_shared_variables_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/hierarchy_linked_list_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/hierarchy_linked_list_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/alert_hierarchy_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/alert_hierarchy_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/license_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/license_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/methods_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/methods_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/bfm_common_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/bfm_common_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/generic_queue_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/generic_queue_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/data_queue_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/data_queue_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/data_fifo_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/data_fifo_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/data_stack_pkg.vhd"
eval vcom $compdirectives $source_path/$util_path/data_stack_pkg.vhd

echo "eval vcom $compdirectives $source_path/$util_path/uvvm_util_context.vhd"
eval vcom $compdirectives $source_path/$util_path/uvvm_util_context.vhd



#-------------------------------------------------------
# Compile BFMs
#
#    This section compiles UVVM BFMs to library uvvm_util.
#    Target directory (compile directory) is /sim or
#    user specified if script is called with argument.
#
#-------------------------------------------------------
echo "\n\n\n=== Compiling UVVM BFMs to directory: $target_path\n"

#
# Search for all VHD files in /src_bfm folder.
#
quietly set vhd_files [glob -directory "$source_path/$bfm_path/" -- "*.vhd"]


#
# Compile all VHD files found in the /src_bfm folder.
#
foreach vhd_file $vhd_files {
  echo "eval vcom $compdirectives  $vhd_file"
  eval vcom $compdirectives  $vhd_file
}
