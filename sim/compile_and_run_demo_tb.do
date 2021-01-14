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
# End the simulations if there's an error or when run from terminal.
#
if {[batch_mode]} {
  onerror {abort all; exit -f -code 1}
} else {
  onerror {abort all}
}

# Detect simulator
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
# Set compile directives based on previously detected simulator.
#
if { [string equal -nocase $simulator "modelsim"] } {
  quietly set compdirectives "-quiet -suppress 1346,1236,1090 -2008 -work uvvm_util"
} elseif { [string equal -nocase $simulator "rivierapro"] } {
  set compdirectives "-2008 -nowarn COMP96_0564 -nowarn COMP96_0048 -dbg -work uvvm_util"
}

#
# Compile UVVM Util library
#
do ../script/compile.do

#-----------------------------------------------------------------------
# Compile testbench files
#
#    This section will compile the DEMO testbench files in to the
#    uvvm_util library.
#
#-----------------------------------------------------------------------
vlib uvvm_util
echo "\nCompiling demo TB\n"


echo "eval vcom $compdirectives ../demo_tb/dut/irqc_pif_pkg.vhd"
eval vcom $compdirectives ../demo_tb/dut/irqc_pif_pkg.vhd

echo "eval vcom $compdirectives ../demo_tb/dut/irqc_pif.vhd"
eval vcom $compdirectives ../demo_tb/dut/irqc_pif.vhd

echo "eval vcom $compdirectives ../demo_tb/dut/irqc_core.vhd"
eval vcom $compdirectives ../demo_tb/dut/irqc_core.vhd

echo "eval vcom $compdirectives ../demo_tb/dut/irqc.vhd"
eval vcom $compdirectives ../demo_tb/dut/irqc.vhd

echo "eval vcom $compdirectives ../demo_tb/demo_tb.vhd"
eval vcom $compdirectives ../demo_tb/demo_tb.vhd



#-----------------------------------------------------------------------
# Run simulation
#
#    This section will run the DEMO testbench in batch mode.
#
#-----------------------------------------------------------------------
vsim -c uvvm_util.demo_tb
run -all
exit -f