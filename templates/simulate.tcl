open_project ../../../microblaze_system/microblaze_system.xpr

add_files -fileset sim_1 testbench.vhd
add_files -fileset sources_1 memory_sim.vhd
add_files -fileset sources_1 controller.vhd
%%ADD_STATEMACHINES%%

set_property top testbench_%%TESTNAME%% [get_filesets "sim_1"]

launch_simulation -simset sim_1

open_saif %%SAIF%%
log_saif [get_objects -r *]

run 5 ms

close_saif

remove_files -fileset sim_1 testbench.vhd
add_files -fileset sources_1 testbench_synth.vhd

remove_files -fileset sources_1 memory_sim.vhd
add_files -fileset sources_1 memory_synth.vhd

set_property top testbench_%%TESTNAME%% [get_filesets "sources_1"]

create_run -flow {Vivado Synthesis 2013} synth_%%TESTNAME%%
launch_runs synth_%%TESTNAME%%
wait_on_run synth_%%TESTNAME%%
open_run synth_%%TESTNAME%%

read_saif %%SAIF%%
report_power -file %%POWER%%
report_utilization -file %%UTIL%%
close_saif

remove_files -fileset sources_1 testbench_synth.vhd
remove_files -fileset sources_1 memory_synth.vhd
remove_files -fileset sources_1 controller.vhd
%%REMOVE_STATEMACHINES%%
