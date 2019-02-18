-makelib ies_lib/xil_defaultlib -sv \
  "/opt/york/cs/net/xilinx_vivado-2018.2_ise-14.7_x86-64-1/Vivado/2018.2/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \
-endlib
-makelib ies_lib/xpm \
  "/opt/york/cs/net/xilinx_vivado-2018.2_ise-14.7_x86-64-1/Vivado/2018.2/data/ip/xpm/xpm_VCOMP.vhd" \
-endlib
-makelib ies_lib/microblaze_v10_0_7 \
  "../../../../microblaze_system.srcs/sources_1/bd/mb_block_design/ipshared/b649/hdl/microblaze_v10_0_vh_rfs.vhd" \
-endlib
-makelib ies_lib/xil_defaultlib \
  "../../../bd/mb_block_design/ip/mb_block_design_microblaze_0_0/sim/mb_block_design_microblaze_0_0.vhd" \
-endlib
-makelib ies_lib/lmb_v10_v3_0_9 \
  "../../../../microblaze_system.srcs/sources_1/bd/mb_block_design/ipshared/78eb/hdl/lmb_v10_v3_0_vh_rfs.vhd" \
-endlib
-makelib ies_lib/xil_defaultlib \
  "../../../bd/mb_block_design/ip/mb_block_design_lmb_v10_0_0/sim/mb_block_design_lmb_v10_0_0.vhd" \
  "../../../bd/mb_block_design/ip/mb_block_design_lmb_v10_1_0/sim/mb_block_design_lmb_v10_1_0.vhd" \
-endlib
-makelib ies_lib/lmb_bram_if_cntlr_v4_0_15 \
  "../../../../microblaze_system.srcs/sources_1/bd/mb_block_design/ipshared/92fd/hdl/lmb_bram_if_cntlr_v4_0_vh_rfs.vhd" \
-endlib
-makelib ies_lib/xil_defaultlib \
  "../../../bd/mb_block_design/ip/mb_block_design_lmb_bram_if_cntlr_0_0/sim/mb_block_design_lmb_bram_if_cntlr_0_0.vhd" \
  "../../../bd/mb_block_design/ip/mb_block_design_lmb_v10_2_0/sim/mb_block_design_lmb_v10_2_0.vhd" \
  "../../../bd/mb_block_design/ip/mb_block_design_lmb_bram_if_cntlr_1_0/sim/mb_block_design_lmb_bram_if_cntlr_1_0.vhd" \
  "../../../bd/mb_block_design/sim/mb_block_design.vhd" \
-endlib
-makelib ies_lib/xil_defaultlib \
  glbl.v
-endlib

