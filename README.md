#  UVVM Light
UVVM (Universal VHDL Verification Methodology) is a free and Open Source Methodology and Library for making very structured VHDL-based testbenches.

Overview, Readability, Maintainability, Extensibility and Reuse are all vital for FPGA development efficiency and quality.
UVVM VVC (VHDL Verification Component) Framework was released in 2016 to handle exactly these aspects.

UVVM Light is a low threshold version of UVVM and is intended for developers who want to start using UVVM Utilty library and BFMs (Bus Functional Models).

UVVM Light consists currently of the following elements:
- Utility Library
- BFMs (Bus Functional Models)


## Issues and pull requests
UVVM Light is a subset of UVVM, thus any issues and pull requests has to be performed on the [UVVM repository] (https://github.com/UVVM/UVVM). 


## Compilation
Compiling UVVM Light can be done by using the compile.do script, located in the repository root folder. 


# Demo
A simple demonstration testbench is provided along with UVVM Light and is located in the /sim folder. Note that libray uvvm_util has to be compiled to the /sim folder prior to running the testbench (see Compilation section above).

Steps to run demo:
1. Run compile.do in repository root folder
2. Run compile_and_run_demo.do / run_demo.bat / run_demo.sh in /sim folder


# Directory structure
- compile.do
- README.md
- /src
- /doc
    - Simple_TB_step_by_step.pps
    - UVVM_Utilty_Library_Concepts_and_Usage.pps
    - util_quick_ref.pdf
    - avalon_mm_bfm_QuickRef.pdf
    - axilite_bfm_QuickRef.pdf
    - gpio_bfm_QuickRef.pdf
    - i2c_bfm_QuickRef.pdf
    - sbi_bfm_QuickRef.pdf
    - spi_bfm_QuickRef.pdf
    - uart_bfm_QuickRef.pdf
- /sim
    - compile_and_run_demo_tb.do
- /src_bfm
    - avalon_mm_bfm_pkg.vhd
    - axilite_bmf_pkg.vhd
    - axistream_bfm_pkg.vhd
    - gpio_bfm_pkg.vhd
    - i2c_bfm_pkg.vhd
    - sbi_bfm_pkg.vhd
    - spi_bfm_pkg.vhd
    - uart_bfm_pkg
- /src_util
    - adaptations_pkg.vhd
    - alert_hierarchy_pkg.vhd
    - bfm_common_pkg.vhd
    - global_signals_and_shared_variables_pkg.vhd
    - hierarchy_linked_list_pkg.vhd
    - license_pkg.vhd
    - methods_pkg.vhd
    - protected_types_pkg.vhd
    - string_methods_pkg.vhd
    - types_pkg.vhd
    - uvvm_util_context.vhd
- /demo_tb 
    - demo_tb.vhd
    - /dut
        - irqc_core.vhd
        - irqc_pif_pkg.vhd
        - irqc_pif.vhd
        - irqc.vhd

