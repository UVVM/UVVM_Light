action = "simulation"
sim_tool = "ghdl"
sim_top = "demo_tb"
ghdl_opt = "--std=08 -frelaxed-rules"

modules = {'local': ['..',
                     '../demo_tb']}
