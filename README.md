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
