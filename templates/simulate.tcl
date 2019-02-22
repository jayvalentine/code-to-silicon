open_project microblaze_system/microblaze_system.xpr

add_files -fileset sim_1 testbench_test.vhd

set_property top testbench_test [get_filesets "sim_1"]

launch_simulation -simset sim_1

remove_files -fileset sim_1 testbench_test.vhd
