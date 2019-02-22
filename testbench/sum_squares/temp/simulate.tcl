open_project ../../../microblaze_system/microblaze_system.xpr

add_files -fileset sim_1 testbench.vhd

set_property top testbench [get_filesets "sim_1"]

launch_simulation -simset sim_1

remove_files -fileset sim_1 testbench.vhd
