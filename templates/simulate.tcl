open_project ../../../microblaze_system/microblaze_system.xpr

add_files -fileset sim_1 testbench.vhd
add_files -fileset sources_1 memory.vhd
add_files -fileset sources_1 controller.vhd
%%ADD_STATEMACHINES%%

set_property top testbench_%%TESTNAME%% [get_filesets "sim_1"]

launch_simulation -simset sim_1
run 5 ms

remove_files -fileset sim_1 testbench.vhd
remove_files -fileset sources_1 memory.vhd
remove_files -fileset sources_1 controller.vhd
%%REMOVE_STATEMACHINES%%
