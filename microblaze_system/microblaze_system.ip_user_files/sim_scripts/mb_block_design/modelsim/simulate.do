onbreak {quit -f}
onerror {quit -f}

vsim -voptargs="+acc" -t 1ps -L xil_defaultlib -L xpm -L microblaze_v10_0_7 -L lmb_v10_v3_0_9 -L lmb_bram_if_cntlr_v4_0_15 -L unisims_ver -L unimacro_ver -L secureip -lib xil_defaultlib xil_defaultlib.mb_block_design xil_defaultlib.glbl

do {wave.do}

view wave
view structure
view signals

do {mb_block_design.udo}

run -all

quit -force
