vlib work
vlib riviera

vlib riviera/xil_defaultlib
vlib riviera/xpm
vlib riviera/microblaze_v10_0_7
vlib riviera/lmb_v10_v3_0_9
vlib riviera/lmb_bram_if_cntlr_v4_0_15

vmap xil_defaultlib riviera/xil_defaultlib
vmap xpm riviera/xpm
vmap microblaze_v10_0_7 riviera/microblaze_v10_0_7
vmap lmb_v10_v3_0_9 riviera/lmb_v10_v3_0_9
vmap lmb_bram_if_cntlr_v4_0_15 riviera/lmb_bram_if_cntlr_v4_0_15

vlog -work xil_defaultlib  -sv2k12 \
"/opt/york/cs/net/xilinx_vivado-2018.2_ise-14.7_x86-64-1/Vivado/2018.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -93 \
"/opt/york/cs/net/xilinx_vivado-2018.2_ise-14.7_x86-64-1/Vivado/2018.2/data/ip/xpm/xpm_VCOMP.vhd" \

vcom -work microblaze_v10_0_7 -93 \
"../../../../microblaze_system.srcs/sources_1/bd/mb_block_design/ipshared/b649/hdl/microblaze_v10_0_vh_rfs.vhd" \

vcom -work xil_defaultlib -93 \
"../../../bd/mb_block_design/ip/mb_block_design_microblaze_0_0/sim/mb_block_design_microblaze_0_0.vhd" \

vcom -work lmb_v10_v3_0_9 -93 \
"../../../../microblaze_system.srcs/sources_1/bd/mb_block_design/ipshared/78eb/hdl/lmb_v10_v3_0_vh_rfs.vhd" \

vcom -work xil_defaultlib -93 \
"../../../bd/mb_block_design/ip/mb_block_design_lmb_v10_0_0/sim/mb_block_design_lmb_v10_0_0.vhd" \
"../../../bd/mb_block_design/ip/mb_block_design_lmb_v10_1_0/sim/mb_block_design_lmb_v10_1_0.vhd" \

vcom -work lmb_bram_if_cntlr_v4_0_15 -93 \
"../../../../microblaze_system.srcs/sources_1/bd/mb_block_design/ipshared/92fd/hdl/lmb_bram_if_cntlr_v4_0_vh_rfs.vhd" \

vcom -work xil_defaultlib -93 \
"../../../bd/mb_block_design/ip/mb_block_design_lmb_bram_if_cntlr_0_0/sim/mb_block_design_lmb_bram_if_cntlr_0_0.vhd" \
"../../../bd/mb_block_design/ip/mb_block_design_lmb_v10_2_0/sim/mb_block_design_lmb_v10_2_0.vhd" \
"../../../bd/mb_block_design/ip/mb_block_design_lmb_bram_if_cntlr_1_0/sim/mb_block_design_lmb_bram_if_cntlr_1_0.vhd" \
"../../../bd/mb_block_design/sim/mb_block_design.vhd" \

vlog -work xil_defaultlib \
"glbl.v"

