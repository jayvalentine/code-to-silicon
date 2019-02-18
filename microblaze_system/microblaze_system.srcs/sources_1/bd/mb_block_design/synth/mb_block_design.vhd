--Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2018.2.1 (lin64) Build 2288692 Thu Jul 26 18:23:50 MDT 2018
--Date        : Mon Feb 18 15:07:56 2019
--Host        : cse069pc-44 running 64-bit Ubuntu 18.04.2 LTS
--Command     : generate_target mb_block_design.bd
--Design      : mb_block_design
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity mb_block_design is
  port (
    LMB_M_0_abus : in STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_M_0_addrstrobe : in STD_LOGIC;
    LMB_M_0_be : in STD_LOGIC_VECTOR ( 0 to 3 );
    LMB_M_0_ce : out STD_LOGIC;
    LMB_M_0_readdbus : out STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_M_0_readstrobe : in STD_LOGIC;
    LMB_M_0_ready : out STD_LOGIC;
    LMB_M_0_rst : out STD_LOGIC;
    LMB_M_0_ue : out STD_LOGIC;
    LMB_M_0_wait : out STD_LOGIC;
    LMB_M_0_writedbus : in STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_M_0_writestrobe : in STD_LOGIC;
    M_AXI_DP_0_araddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M_AXI_DP_0_arprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M_AXI_DP_0_arready : in STD_LOGIC;
    M_AXI_DP_0_arvalid : out STD_LOGIC;
    M_AXI_DP_0_awaddr : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M_AXI_DP_0_awprot : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M_AXI_DP_0_awready : in STD_LOGIC;
    M_AXI_DP_0_awvalid : out STD_LOGIC;
    M_AXI_DP_0_bready : out STD_LOGIC;
    M_AXI_DP_0_bresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
    M_AXI_DP_0_bvalid : in STD_LOGIC;
    M_AXI_DP_0_rdata : in STD_LOGIC_VECTOR ( 31 downto 0 );
    M_AXI_DP_0_rready : out STD_LOGIC;
    M_AXI_DP_0_rresp : in STD_LOGIC_VECTOR ( 1 downto 0 );
    M_AXI_DP_0_rvalid : in STD_LOGIC;
    M_AXI_DP_0_wdata : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M_AXI_DP_0_wready : in STD_LOGIC;
    M_AXI_DP_0_wstrb : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M_AXI_DP_0_wvalid : out STD_LOGIC;
    clk_100MHz : in STD_LOGIC;
    rst : in STD_LOGIC
  );
  attribute CORE_GENERATION_INFO : string;
  attribute CORE_GENERATION_INFO of mb_block_design : entity is "mb_block_design,IP_Integrator,{x_ipVendor=xilinx.com,x_ipLibrary=BlockDiagram,x_ipName=mb_block_design,x_ipVersion=1.00.a,x_ipLanguage=VHDL,numBlks=7,numReposBlks=7,numNonXlnxBlks=0,numHierBlks=0,maxHierDepth=0,numSysgenBlks=0,numHlsBlks=0,numHdlrefBlks=0,numPkgbdBlks=0,bdsource=USER,da_board_cnt=4,da_clkrst_cnt=2,da_mb_cnt=1,synth_mode=OOC_per_IP}";
  attribute HW_HANDOFF : string;
  attribute HW_HANDOFF of mb_block_design : entity is "mb_block_design.hwdef";
end mb_block_design;

architecture STRUCTURE of mb_block_design is
  component mb_block_design_microblaze_0_0 is
  port (
    Clk : in STD_LOGIC;
    Reset : in STD_LOGIC;
    Interrupt : in STD_LOGIC;
    Interrupt_Address : in STD_LOGIC_VECTOR ( 0 to 31 );
    Interrupt_Ack : out STD_LOGIC_VECTOR ( 0 to 1 );
    Instr_Addr : out STD_LOGIC_VECTOR ( 0 to 31 );
    Instr : in STD_LOGIC_VECTOR ( 0 to 31 );
    IFetch : out STD_LOGIC;
    I_AS : out STD_LOGIC;
    IReady : in STD_LOGIC;
    IWAIT : in STD_LOGIC;
    ICE : in STD_LOGIC;
    IUE : in STD_LOGIC;
    Data_Addr : out STD_LOGIC_VECTOR ( 0 to 31 );
    Data_Read : in STD_LOGIC_VECTOR ( 0 to 31 );
    Data_Write : out STD_LOGIC_VECTOR ( 0 to 31 );
    D_AS : out STD_LOGIC;
    Read_Strobe : out STD_LOGIC;
    Write_Strobe : out STD_LOGIC;
    DReady : in STD_LOGIC;
    DWait : in STD_LOGIC;
    DCE : in STD_LOGIC;
    DUE : in STD_LOGIC;
    Byte_Enable : out STD_LOGIC_VECTOR ( 0 to 3 );
    M_AXI_DP_AWADDR : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M_AXI_DP_AWPROT : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M_AXI_DP_AWVALID : out STD_LOGIC;
    M_AXI_DP_AWREADY : in STD_LOGIC;
    M_AXI_DP_WDATA : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M_AXI_DP_WSTRB : out STD_LOGIC_VECTOR ( 3 downto 0 );
    M_AXI_DP_WVALID : out STD_LOGIC;
    M_AXI_DP_WREADY : in STD_LOGIC;
    M_AXI_DP_BRESP : in STD_LOGIC_VECTOR ( 1 downto 0 );
    M_AXI_DP_BVALID : in STD_LOGIC;
    M_AXI_DP_BREADY : out STD_LOGIC;
    M_AXI_DP_ARADDR : out STD_LOGIC_VECTOR ( 31 downto 0 );
    M_AXI_DP_ARPROT : out STD_LOGIC_VECTOR ( 2 downto 0 );
    M_AXI_DP_ARVALID : out STD_LOGIC;
    M_AXI_DP_ARREADY : in STD_LOGIC;
    M_AXI_DP_RDATA : in STD_LOGIC_VECTOR ( 31 downto 0 );
    M_AXI_DP_RRESP : in STD_LOGIC_VECTOR ( 1 downto 0 );
    M_AXI_DP_RVALID : in STD_LOGIC;
    M_AXI_DP_RREADY : out STD_LOGIC
  );
  end component mb_block_design_microblaze_0_0;
  component mb_block_design_lmb_v10_0_0 is
  port (
    LMB_Clk : in STD_LOGIC;
    SYS_Rst : in STD_LOGIC;
    LMB_Rst : out STD_LOGIC;
    M_ABus : in STD_LOGIC_VECTOR ( 0 to 31 );
    M_ReadStrobe : in STD_LOGIC;
    M_WriteStrobe : in STD_LOGIC;
    M_AddrStrobe : in STD_LOGIC;
    M_DBus : in STD_LOGIC_VECTOR ( 0 to 31 );
    M_BE : in STD_LOGIC_VECTOR ( 0 to 3 );
    Sl_DBus : in STD_LOGIC_VECTOR ( 0 to 31 );
    Sl_Ready : in STD_LOGIC_VECTOR ( 0 to 0 );
    Sl_Wait : in STD_LOGIC_VECTOR ( 0 to 0 );
    Sl_UE : in STD_LOGIC_VECTOR ( 0 to 0 );
    Sl_CE : in STD_LOGIC_VECTOR ( 0 to 0 );
    LMB_ABus : out STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_ReadStrobe : out STD_LOGIC;
    LMB_WriteStrobe : out STD_LOGIC;
    LMB_AddrStrobe : out STD_LOGIC;
    LMB_ReadDBus : out STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_WriteDBus : out STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_Ready : out STD_LOGIC;
    LMB_Wait : out STD_LOGIC;
    LMB_UE : out STD_LOGIC;
    LMB_CE : out STD_LOGIC;
    LMB_BE : out STD_LOGIC_VECTOR ( 0 to 3 )
  );
  end component mb_block_design_lmb_v10_0_0;
  component mb_block_design_lmb_v10_1_0 is
  port (
    LMB_Clk : in STD_LOGIC;
    SYS_Rst : in STD_LOGIC;
    LMB_Rst : out STD_LOGIC;
    M_ABus : in STD_LOGIC_VECTOR ( 0 to 31 );
    M_ReadStrobe : in STD_LOGIC;
    M_WriteStrobe : in STD_LOGIC;
    M_AddrStrobe : in STD_LOGIC;
    M_DBus : in STD_LOGIC_VECTOR ( 0 to 31 );
    M_BE : in STD_LOGIC_VECTOR ( 0 to 3 );
    Sl_DBus : in STD_LOGIC_VECTOR ( 0 to 31 );
    Sl_Ready : in STD_LOGIC_VECTOR ( 0 to 0 );
    Sl_Wait : in STD_LOGIC_VECTOR ( 0 to 0 );
    Sl_UE : in STD_LOGIC_VECTOR ( 0 to 0 );
    Sl_CE : in STD_LOGIC_VECTOR ( 0 to 0 );
    LMB_ABus : out STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_ReadStrobe : out STD_LOGIC;
    LMB_WriteStrobe : out STD_LOGIC;
    LMB_AddrStrobe : out STD_LOGIC;
    LMB_ReadDBus : out STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_WriteDBus : out STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_Ready : out STD_LOGIC;
    LMB_Wait : out STD_LOGIC;
    LMB_UE : out STD_LOGIC;
    LMB_CE : out STD_LOGIC;
    LMB_BE : out STD_LOGIC_VECTOR ( 0 to 3 )
  );
  end component mb_block_design_lmb_v10_1_0;
  component mb_block_design_lmb_bram_if_cntlr_0_0 is
  port (
    LMB_Clk : in STD_LOGIC;
    LMB_Rst : in STD_LOGIC;
    LMB_ABus : in STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_WriteDBus : in STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_AddrStrobe : in STD_LOGIC;
    LMB_ReadStrobe : in STD_LOGIC;
    LMB_WriteStrobe : in STD_LOGIC;
    LMB_BE : in STD_LOGIC_VECTOR ( 0 to 3 );
    Sl_DBus : out STD_LOGIC_VECTOR ( 0 to 31 );
    Sl_Ready : out STD_LOGIC;
    Sl_Wait : out STD_LOGIC;
    Sl_UE : out STD_LOGIC;
    Sl_CE : out STD_LOGIC;
    LMB1_ABus : in STD_LOGIC_VECTOR ( 0 to 31 );
    LMB1_WriteDBus : in STD_LOGIC_VECTOR ( 0 to 31 );
    LMB1_AddrStrobe : in STD_LOGIC;
    LMB1_ReadStrobe : in STD_LOGIC;
    LMB1_WriteStrobe : in STD_LOGIC;
    LMB1_BE : in STD_LOGIC_VECTOR ( 0 to 3 );
    Sl1_DBus : out STD_LOGIC_VECTOR ( 0 to 31 );
    Sl1_Ready : out STD_LOGIC;
    Sl1_Wait : out STD_LOGIC;
    Sl1_UE : out STD_LOGIC;
    Sl1_CE : out STD_LOGIC;
    BRAM_Rst_A : out STD_LOGIC;
    BRAM_Clk_A : out STD_LOGIC;
    BRAM_Addr_A : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_EN_A : out STD_LOGIC;
    BRAM_WEN_A : out STD_LOGIC_VECTOR ( 0 to 3 );
    BRAM_Dout_A : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_Din_A : in STD_LOGIC_VECTOR ( 0 to 31 )
  );
  end component mb_block_design_lmb_bram_if_cntlr_0_0;
  component mb_block_design_lmb_v10_2_0 is
  port (
    LMB_Clk : in STD_LOGIC;
    SYS_Rst : in STD_LOGIC;
    LMB_Rst : out STD_LOGIC;
    M_ABus : in STD_LOGIC_VECTOR ( 0 to 31 );
    M_ReadStrobe : in STD_LOGIC;
    M_WriteStrobe : in STD_LOGIC;
    M_AddrStrobe : in STD_LOGIC;
    M_DBus : in STD_LOGIC_VECTOR ( 0 to 31 );
    M_BE : in STD_LOGIC_VECTOR ( 0 to 3 );
    Sl_DBus : in STD_LOGIC_VECTOR ( 0 to 31 );
    Sl_Ready : in STD_LOGIC_VECTOR ( 0 to 0 );
    Sl_Wait : in STD_LOGIC_VECTOR ( 0 to 0 );
    Sl_UE : in STD_LOGIC_VECTOR ( 0 to 0 );
    Sl_CE : in STD_LOGIC_VECTOR ( 0 to 0 );
    LMB_ABus : out STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_ReadStrobe : out STD_LOGIC;
    LMB_WriteStrobe : out STD_LOGIC;
    LMB_AddrStrobe : out STD_LOGIC;
    LMB_ReadDBus : out STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_WriteDBus : out STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_Ready : out STD_LOGIC;
    LMB_Wait : out STD_LOGIC;
    LMB_UE : out STD_LOGIC;
    LMB_CE : out STD_LOGIC;
    LMB_BE : out STD_LOGIC_VECTOR ( 0 to 3 )
  );
  end component mb_block_design_lmb_v10_2_0;
  component mb_block_design_lmb_bram_if_cntlr_1_0 is
  port (
    LMB_Clk : in STD_LOGIC;
    LMB_Rst : in STD_LOGIC;
    LMB_ABus : in STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_WriteDBus : in STD_LOGIC_VECTOR ( 0 to 31 );
    LMB_AddrStrobe : in STD_LOGIC;
    LMB_ReadStrobe : in STD_LOGIC;
    LMB_WriteStrobe : in STD_LOGIC;
    LMB_BE : in STD_LOGIC_VECTOR ( 0 to 3 );
    Sl_DBus : out STD_LOGIC_VECTOR ( 0 to 31 );
    Sl_Ready : out STD_LOGIC;
    Sl_Wait : out STD_LOGIC;
    Sl_UE : out STD_LOGIC;
    Sl_CE : out STD_LOGIC;
    BRAM_Rst_A : out STD_LOGIC;
    BRAM_Clk_A : out STD_LOGIC;
    BRAM_Addr_A : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_EN_A : out STD_LOGIC;
    BRAM_WEN_A : out STD_LOGIC_VECTOR ( 0 to 3 );
    BRAM_Dout_A : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_Din_A : in STD_LOGIC_VECTOR ( 0 to 31 )
  );
  end component mb_block_design_lmb_bram_if_cntlr_1_0;
  component mb_block_design_blk_mem_gen_0_0 is
  port (
    clka : in STD_LOGIC;
    rsta : in STD_LOGIC;
    ena : in STD_LOGIC;
    addra : in STD_LOGIC_VECTOR ( 31 downto 0 );
    douta : out STD_LOGIC_VECTOR ( 31 downto 0 );
    clkb : in STD_LOGIC;
    rstb : in STD_LOGIC;
    enb : in STD_LOGIC;
    addrb : in STD_LOGIC_VECTOR ( 31 downto 0 );
    doutb : out STD_LOGIC_VECTOR ( 31 downto 0 );
    rsta_busy : out STD_LOGIC;
    rstb_busy : out STD_LOGIC
  );
  end component mb_block_design_blk_mem_gen_0_0;
  signal Conn1_ABUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn1_ADDRSTROBE : STD_LOGIC;
  signal Conn1_BE : STD_LOGIC_VECTOR ( 0 to 3 );
  signal Conn1_CE : STD_LOGIC;
  signal Conn1_READDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn1_READSTROBE : STD_LOGIC;
  signal Conn1_READY : STD_LOGIC;
  signal Conn1_UE : STD_LOGIC;
  signal Conn1_WAIT : STD_LOGIC;
  signal Conn1_WRITEDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn1_WRITESTROBE : STD_LOGIC;
  signal Conn2_ABUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn2_ADDRSTROBE : STD_LOGIC;
  signal Conn2_BE : STD_LOGIC_VECTOR ( 0 to 3 );
  signal Conn2_CE : STD_LOGIC;
  signal Conn2_READDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn2_READSTROBE : STD_LOGIC;
  signal Conn2_READY : STD_LOGIC;
  signal Conn2_UE : STD_LOGIC;
  signal Conn2_WAIT : STD_LOGIC;
  signal Conn2_WRITEDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn2_WRITESTROBE : STD_LOGIC;
  signal Conn3_ABUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn3_ADDRSTROBE : STD_LOGIC;
  signal Conn3_BE : STD_LOGIC_VECTOR ( 0 to 3 );
  signal Conn3_CE : STD_LOGIC;
  signal Conn3_READDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn3_READSTROBE : STD_LOGIC;
  signal Conn3_READY : STD_LOGIC;
  signal Conn3_RST : STD_LOGIC;
  signal Conn3_UE : STD_LOGIC;
  signal Conn3_WAIT : STD_LOGIC;
  signal Conn3_WRITEDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn3_WRITESTROBE : STD_LOGIC;
  signal Conn_ABUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn_ADDRSTROBE : STD_LOGIC;
  signal Conn_BE : STD_LOGIC_VECTOR ( 0 to 3 );
  signal Conn_CE : STD_LOGIC;
  signal Conn_READDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn_READSTROBE : STD_LOGIC;
  signal Conn_READY : STD_LOGIC;
  signal Conn_UE : STD_LOGIC;
  signal Conn_WAIT : STD_LOGIC;
  signal Conn_WRITEDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal Conn_WRITESTROBE : STD_LOGIC;
  signal clk_100MHz_1 : STD_LOGIC;
  signal lmb_bram_if_cntlr_0_BRAM_PORT_ADDR : STD_LOGIC_VECTOR ( 0 to 31 );
  signal lmb_bram_if_cntlr_0_BRAM_PORT_CLK : STD_LOGIC;
  signal lmb_bram_if_cntlr_0_BRAM_PORT_DOUT : STD_LOGIC_VECTOR ( 31 downto 0 );
  signal lmb_bram_if_cntlr_0_BRAM_PORT_EN : STD_LOGIC;
  signal lmb_bram_if_cntlr_0_BRAM_PORT_RST : STD_LOGIC;
  signal lmb_bram_if_cntlr_1_BRAM_PORT_ADDR : STD_LOGIC_VECTOR ( 0 to 31 );
  signal lmb_bram_if_cntlr_1_BRAM_PORT_CLK : STD_LOGIC;
  signal lmb_bram_if_cntlr_1_BRAM_PORT_DOUT : STD_LOGIC_VECTOR ( 31 downto 0 );
  signal lmb_bram_if_cntlr_1_BRAM_PORT_EN : STD_LOGIC;
  signal lmb_bram_if_cntlr_1_BRAM_PORT_RST : STD_LOGIC;
  signal microblaze_0_DLMB_ABUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal microblaze_0_DLMB_ADDRSTROBE : STD_LOGIC;
  signal microblaze_0_DLMB_BE : STD_LOGIC_VECTOR ( 0 to 3 );
  signal microblaze_0_DLMB_CE : STD_LOGIC;
  signal microblaze_0_DLMB_READDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal microblaze_0_DLMB_READSTROBE : STD_LOGIC;
  signal microblaze_0_DLMB_READY : STD_LOGIC;
  signal microblaze_0_DLMB_UE : STD_LOGIC;
  signal microblaze_0_DLMB_WAIT : STD_LOGIC;
  signal microblaze_0_DLMB_WRITEDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal microblaze_0_DLMB_WRITESTROBE : STD_LOGIC;
  signal microblaze_0_ILMB_ABUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal microblaze_0_ILMB_ADDRSTROBE : STD_LOGIC;
  signal microblaze_0_ILMB_CE : STD_LOGIC;
  signal microblaze_0_ILMB_READDBUS : STD_LOGIC_VECTOR ( 0 to 31 );
  signal microblaze_0_ILMB_READSTROBE : STD_LOGIC;
  signal microblaze_0_ILMB_READY : STD_LOGIC;
  signal microblaze_0_ILMB_UE : STD_LOGIC;
  signal microblaze_0_ILMB_WAIT : STD_LOGIC;
  signal microblaze_0_M_AXI_DP_ARADDR : STD_LOGIC_VECTOR ( 31 downto 0 );
  signal microblaze_0_M_AXI_DP_ARPROT : STD_LOGIC_VECTOR ( 2 downto 0 );
  signal microblaze_0_M_AXI_DP_ARREADY : STD_LOGIC;
  signal microblaze_0_M_AXI_DP_ARVALID : STD_LOGIC;
  signal microblaze_0_M_AXI_DP_AWADDR : STD_LOGIC_VECTOR ( 31 downto 0 );
  signal microblaze_0_M_AXI_DP_AWPROT : STD_LOGIC_VECTOR ( 2 downto 0 );
  signal microblaze_0_M_AXI_DP_AWREADY : STD_LOGIC;
  signal microblaze_0_M_AXI_DP_AWVALID : STD_LOGIC;
  signal microblaze_0_M_AXI_DP_BREADY : STD_LOGIC;
  signal microblaze_0_M_AXI_DP_BRESP : STD_LOGIC_VECTOR ( 1 downto 0 );
  signal microblaze_0_M_AXI_DP_BVALID : STD_LOGIC;
  signal microblaze_0_M_AXI_DP_RDATA : STD_LOGIC_VECTOR ( 31 downto 0 );
  signal microblaze_0_M_AXI_DP_RREADY : STD_LOGIC;
  signal microblaze_0_M_AXI_DP_RRESP : STD_LOGIC_VECTOR ( 1 downto 0 );
  signal microblaze_0_M_AXI_DP_RVALID : STD_LOGIC;
  signal microblaze_0_M_AXI_DP_WDATA : STD_LOGIC_VECTOR ( 31 downto 0 );
  signal microblaze_0_M_AXI_DP_WREADY : STD_LOGIC;
  signal microblaze_0_M_AXI_DP_WSTRB : STD_LOGIC_VECTOR ( 3 downto 0 );
  signal microblaze_0_M_AXI_DP_WVALID : STD_LOGIC;
  signal rst_1 : STD_LOGIC;
  signal NLW_blk_mem_gen_0_rsta_busy_UNCONNECTED : STD_LOGIC;
  signal NLW_blk_mem_gen_0_rstb_busy_UNCONNECTED : STD_LOGIC;
  signal NLW_lmb_bram_if_cntlr_0_BRAM_Dout_A_UNCONNECTED : STD_LOGIC_VECTOR ( 0 to 31 );
  signal NLW_lmb_bram_if_cntlr_0_BRAM_WEN_A_UNCONNECTED : STD_LOGIC_VECTOR ( 0 to 3 );
  signal NLW_lmb_bram_if_cntlr_1_BRAM_Dout_A_UNCONNECTED : STD_LOGIC_VECTOR ( 0 to 31 );
  signal NLW_lmb_bram_if_cntlr_1_BRAM_WEN_A_UNCONNECTED : STD_LOGIC_VECTOR ( 0 to 3 );
  signal NLW_lmb_v10_0_LMB_Rst_UNCONNECTED : STD_LOGIC;
  signal NLW_lmb_v10_2_LMB_Rst_UNCONNECTED : STD_LOGIC;
  signal NLW_microblaze_0_Interrupt_Ack_UNCONNECTED : STD_LOGIC_VECTOR ( 0 to 1 );
  attribute BMM_INFO_ADDRESS_SPACE : string;
  attribute BMM_INFO_ADDRESS_SPACE of lmb_bram_if_cntlr_0 : label is "byte  0x00000000 32 > mb_block_design blk_mem_gen_0";
  attribute KEEP_HIERARCHY : string;
  attribute KEEP_HIERARCHY of lmb_bram_if_cntlr_0 : label is "yes";
  attribute BMM_INFO_PROCESSOR : string;
  attribute BMM_INFO_PROCESSOR of microblaze_0 : label is "microblaze-le > mb_block_design lmb_bram_if_cntlr_0";
  attribute KEEP_HIERARCHY of microblaze_0 : label is "yes";
  attribute X_INTERFACE_INFO : string;
  attribute X_INTERFACE_INFO of LMB_M_0_addrstrobe : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 ADDRSTROBE";
  attribute X_INTERFACE_INFO of LMB_M_0_ce : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 CE";
  attribute X_INTERFACE_INFO of LMB_M_0_readstrobe : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 READSTROBE";
  attribute X_INTERFACE_INFO of LMB_M_0_ready : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 READY";
  attribute X_INTERFACE_INFO of LMB_M_0_rst : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 RST";
  attribute X_INTERFACE_INFO of LMB_M_0_ue : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 UE";
  attribute X_INTERFACE_INFO of LMB_M_0_wait : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 WAIT";
  attribute X_INTERFACE_INFO of LMB_M_0_writestrobe : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 WRITESTROBE";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_arready : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 ARREADY";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_arvalid : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 ARVALID";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_awready : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 AWREADY";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_awvalid : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 AWVALID";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_bready : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 BREADY";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_bvalid : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 BVALID";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_rready : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 RREADY";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_rvalid : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 RVALID";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_wready : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 WREADY";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_wvalid : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 WVALID";
  attribute X_INTERFACE_INFO of clk_100MHz : signal is "xilinx.com:signal:clock:1.0 CLK.CLK_100MHZ CLK";
  attribute X_INTERFACE_PARAMETER : string;
  attribute X_INTERFACE_PARAMETER of clk_100MHz : signal is "XIL_INTERFACENAME CLK.CLK_100MHZ, ASSOCIATED_BUSIF M_AXI_DP_0, ASSOCIATED_RESET rst, CLK_DOMAIN mb_block_design_clk_100MHz, FREQ_HZ 100000000, PHASE 0.000";
  attribute X_INTERFACE_INFO of rst : signal is "xilinx.com:signal:reset:1.0 RST.RST RST";
  attribute X_INTERFACE_PARAMETER of rst : signal is "XIL_INTERFACENAME RST.RST, POLARITY ACTIVE_HIGH";
  attribute X_INTERFACE_INFO of LMB_M_0_abus : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 ABUS";
  attribute X_INTERFACE_PARAMETER of LMB_M_0_abus : signal is "XIL_INTERFACENAME LMB_M_0, ADDR_WIDTH 32, DATA_WIDTH 32, READ_WRITE_MODE READ_WRITE";
  attribute X_INTERFACE_INFO of LMB_M_0_be : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 BE";
  attribute X_INTERFACE_INFO of LMB_M_0_readdbus : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 READDBUS";
  attribute X_INTERFACE_INFO of LMB_M_0_writedbus : signal is "xilinx.com:interface:lmb:1.0 LMB_M_0 WRITEDBUS";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_araddr : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 ARADDR";
  attribute X_INTERFACE_PARAMETER of M_AXI_DP_0_araddr : signal is "XIL_INTERFACENAME M_AXI_DP_0, ADDR_WIDTH 32, ARUSER_WIDTH 0, AWUSER_WIDTH 0, BUSER_WIDTH 0, CLK_DOMAIN mb_block_design_clk_100MHz, DATA_WIDTH 32, FREQ_HZ 100000000, HAS_BRESP 1, HAS_BURST 0, HAS_CACHE 0, HAS_LOCK 0, HAS_PROT 1, HAS_QOS 0, HAS_REGION 0, HAS_RRESP 1, HAS_WSTRB 1, ID_WIDTH 0, MAX_BURST_LENGTH 1, NUM_READ_OUTSTANDING 1, NUM_READ_THREADS 1, NUM_WRITE_OUTSTANDING 1, NUM_WRITE_THREADS 1, PHASE 0.000, PROTOCOL AXI4LITE, READ_WRITE_MODE READ_WRITE, RUSER_BITS_PER_BYTE 0, RUSER_WIDTH 0, SUPPORTS_NARROW_BURST 0, WUSER_BITS_PER_BYTE 0, WUSER_WIDTH 0";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_arprot : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 ARPROT";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_awaddr : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 AWADDR";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_awprot : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 AWPROT";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_bresp : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 BRESP";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_rdata : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 RDATA";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_rresp : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 RRESP";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_wdata : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 WDATA";
  attribute X_INTERFACE_INFO of M_AXI_DP_0_wstrb : signal is "xilinx.com:interface:aximm:1.0 M_AXI_DP_0 WSTRB";
begin
  Conn3_ABUS(0 to 31) <= LMB_M_0_abus(0 to 31);
  Conn3_ADDRSTROBE <= LMB_M_0_addrstrobe;
  Conn3_BE(0 to 3) <= LMB_M_0_be(0 to 3);
  Conn3_READSTROBE <= LMB_M_0_readstrobe;
  Conn3_WRITEDBUS(0 to 31) <= LMB_M_0_writedbus(0 to 31);
  Conn3_WRITESTROBE <= LMB_M_0_writestrobe;
  LMB_M_0_ce <= Conn3_CE;
  LMB_M_0_readdbus(0 to 31) <= Conn3_READDBUS(0 to 31);
  LMB_M_0_ready <= Conn3_READY;
  LMB_M_0_rst <= Conn3_RST;
  LMB_M_0_ue <= Conn3_UE;
  LMB_M_0_wait <= Conn3_WAIT;
  M_AXI_DP_0_araddr(31 downto 0) <= microblaze_0_M_AXI_DP_ARADDR(31 downto 0);
  M_AXI_DP_0_arprot(2 downto 0) <= microblaze_0_M_AXI_DP_ARPROT(2 downto 0);
  M_AXI_DP_0_arvalid <= microblaze_0_M_AXI_DP_ARVALID;
  M_AXI_DP_0_awaddr(31 downto 0) <= microblaze_0_M_AXI_DP_AWADDR(31 downto 0);
  M_AXI_DP_0_awprot(2 downto 0) <= microblaze_0_M_AXI_DP_AWPROT(2 downto 0);
  M_AXI_DP_0_awvalid <= microblaze_0_M_AXI_DP_AWVALID;
  M_AXI_DP_0_bready <= microblaze_0_M_AXI_DP_BREADY;
  M_AXI_DP_0_rready <= microblaze_0_M_AXI_DP_RREADY;
  M_AXI_DP_0_wdata(31 downto 0) <= microblaze_0_M_AXI_DP_WDATA(31 downto 0);
  M_AXI_DP_0_wstrb(3 downto 0) <= microblaze_0_M_AXI_DP_WSTRB(3 downto 0);
  M_AXI_DP_0_wvalid <= microblaze_0_M_AXI_DP_WVALID;
  clk_100MHz_1 <= clk_100MHz;
  microblaze_0_M_AXI_DP_ARREADY <= M_AXI_DP_0_arready;
  microblaze_0_M_AXI_DP_AWREADY <= M_AXI_DP_0_awready;
  microblaze_0_M_AXI_DP_BRESP(1 downto 0) <= M_AXI_DP_0_bresp(1 downto 0);
  microblaze_0_M_AXI_DP_BVALID <= M_AXI_DP_0_bvalid;
  microblaze_0_M_AXI_DP_RDATA(31 downto 0) <= M_AXI_DP_0_rdata(31 downto 0);
  microblaze_0_M_AXI_DP_RRESP(1 downto 0) <= M_AXI_DP_0_rresp(1 downto 0);
  microblaze_0_M_AXI_DP_RVALID <= M_AXI_DP_0_rvalid;
  microblaze_0_M_AXI_DP_WREADY <= M_AXI_DP_0_wready;
  rst_1 <= rst;
blk_mem_gen_0: component mb_block_design_blk_mem_gen_0_0
     port map (
      addra(31) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(0),
      addra(30) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(1),
      addra(29) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(2),
      addra(28) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(3),
      addra(27) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(4),
      addra(26) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(5),
      addra(25) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(6),
      addra(24) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(7),
      addra(23) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(8),
      addra(22) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(9),
      addra(21) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(10),
      addra(20) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(11),
      addra(19) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(12),
      addra(18) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(13),
      addra(17) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(14),
      addra(16) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(15),
      addra(15) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(16),
      addra(14) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(17),
      addra(13) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(18),
      addra(12) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(19),
      addra(11) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(20),
      addra(10) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(21),
      addra(9) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(22),
      addra(8) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(23),
      addra(7) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(24),
      addra(6) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(25),
      addra(5) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(26),
      addra(4) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(27),
      addra(3) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(28),
      addra(2) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(29),
      addra(1) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(30),
      addra(0) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(31),
      addrb(31) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(0),
      addrb(30) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(1),
      addrb(29) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(2),
      addrb(28) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(3),
      addrb(27) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(4),
      addrb(26) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(5),
      addrb(25) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(6),
      addrb(24) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(7),
      addrb(23) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(8),
      addrb(22) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(9),
      addrb(21) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(10),
      addrb(20) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(11),
      addrb(19) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(12),
      addrb(18) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(13),
      addrb(17) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(14),
      addrb(16) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(15),
      addrb(15) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(16),
      addrb(14) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(17),
      addrb(13) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(18),
      addrb(12) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(19),
      addrb(11) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(20),
      addrb(10) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(21),
      addrb(9) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(22),
      addrb(8) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(23),
      addrb(7) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(24),
      addrb(6) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(25),
      addrb(5) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(26),
      addrb(4) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(27),
      addrb(3) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(28),
      addrb(2) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(29),
      addrb(1) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(30),
      addrb(0) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(31),
      clka => lmb_bram_if_cntlr_0_BRAM_PORT_CLK,
      clkb => lmb_bram_if_cntlr_1_BRAM_PORT_CLK,
      douta(31 downto 0) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(31 downto 0),
      doutb(31 downto 0) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(31 downto 0),
      ena => lmb_bram_if_cntlr_0_BRAM_PORT_EN,
      enb => lmb_bram_if_cntlr_1_BRAM_PORT_EN,
      rsta => lmb_bram_if_cntlr_0_BRAM_PORT_RST,
      rsta_busy => NLW_blk_mem_gen_0_rsta_busy_UNCONNECTED,
      rstb => lmb_bram_if_cntlr_1_BRAM_PORT_RST,
      rstb_busy => NLW_blk_mem_gen_0_rstb_busy_UNCONNECTED
    );
lmb_bram_if_cntlr_0: component mb_block_design_lmb_bram_if_cntlr_0_0
     port map (
      BRAM_Addr_A(0 to 31) => lmb_bram_if_cntlr_0_BRAM_PORT_ADDR(0 to 31),
      BRAM_Clk_A => lmb_bram_if_cntlr_0_BRAM_PORT_CLK,
      BRAM_Din_A(0) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(31),
      BRAM_Din_A(1) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(30),
      BRAM_Din_A(2) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(29),
      BRAM_Din_A(3) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(28),
      BRAM_Din_A(4) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(27),
      BRAM_Din_A(5) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(26),
      BRAM_Din_A(6) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(25),
      BRAM_Din_A(7) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(24),
      BRAM_Din_A(8) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(23),
      BRAM_Din_A(9) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(22),
      BRAM_Din_A(10) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(21),
      BRAM_Din_A(11) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(20),
      BRAM_Din_A(12) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(19),
      BRAM_Din_A(13) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(18),
      BRAM_Din_A(14) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(17),
      BRAM_Din_A(15) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(16),
      BRAM_Din_A(16) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(15),
      BRAM_Din_A(17) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(14),
      BRAM_Din_A(18) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(13),
      BRAM_Din_A(19) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(12),
      BRAM_Din_A(20) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(11),
      BRAM_Din_A(21) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(10),
      BRAM_Din_A(22) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(9),
      BRAM_Din_A(23) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(8),
      BRAM_Din_A(24) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(7),
      BRAM_Din_A(25) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(6),
      BRAM_Din_A(26) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(5),
      BRAM_Din_A(27) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(4),
      BRAM_Din_A(28) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(3),
      BRAM_Din_A(29) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(2),
      BRAM_Din_A(30) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(1),
      BRAM_Din_A(31) => lmb_bram_if_cntlr_0_BRAM_PORT_DOUT(0),
      BRAM_Dout_A(0 to 31) => NLW_lmb_bram_if_cntlr_0_BRAM_Dout_A_UNCONNECTED(0 to 31),
      BRAM_EN_A => lmb_bram_if_cntlr_0_BRAM_PORT_EN,
      BRAM_Rst_A => lmb_bram_if_cntlr_0_BRAM_PORT_RST,
      BRAM_WEN_A(0 to 3) => NLW_lmb_bram_if_cntlr_0_BRAM_WEN_A_UNCONNECTED(0 to 3),
      LMB1_ABus(0 to 31) => Conn1_ABUS(0 to 31),
      LMB1_AddrStrobe => Conn1_ADDRSTROBE,
      LMB1_BE(0 to 3) => Conn1_BE(0 to 3),
      LMB1_ReadStrobe => Conn1_READSTROBE,
      LMB1_WriteDBus(0 to 31) => Conn1_WRITEDBUS(0 to 31),
      LMB1_WriteStrobe => Conn1_WRITESTROBE,
      LMB_ABus(0 to 31) => Conn_ABUS(0 to 31),
      LMB_AddrStrobe => Conn_ADDRSTROBE,
      LMB_BE(0 to 3) => Conn_BE(0 to 3),
      LMB_Clk => clk_100MHz_1,
      LMB_ReadStrobe => Conn_READSTROBE,
      LMB_Rst => rst_1,
      LMB_WriteDBus(0 to 31) => Conn_WRITEDBUS(0 to 31),
      LMB_WriteStrobe => Conn_WRITESTROBE,
      Sl1_CE => Conn1_CE,
      Sl1_DBus(0 to 31) => Conn1_READDBUS(0 to 31),
      Sl1_Ready => Conn1_READY,
      Sl1_UE => Conn1_UE,
      Sl1_Wait => Conn1_WAIT,
      Sl_CE => Conn_CE,
      Sl_DBus(0 to 31) => Conn_READDBUS(0 to 31),
      Sl_Ready => Conn_READY,
      Sl_UE => Conn_UE,
      Sl_Wait => Conn_WAIT
    );
lmb_bram_if_cntlr_1: component mb_block_design_lmb_bram_if_cntlr_1_0
     port map (
      BRAM_Addr_A(0 to 31) => lmb_bram_if_cntlr_1_BRAM_PORT_ADDR(0 to 31),
      BRAM_Clk_A => lmb_bram_if_cntlr_1_BRAM_PORT_CLK,
      BRAM_Din_A(0) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(31),
      BRAM_Din_A(1) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(30),
      BRAM_Din_A(2) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(29),
      BRAM_Din_A(3) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(28),
      BRAM_Din_A(4) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(27),
      BRAM_Din_A(5) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(26),
      BRAM_Din_A(6) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(25),
      BRAM_Din_A(7) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(24),
      BRAM_Din_A(8) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(23),
      BRAM_Din_A(9) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(22),
      BRAM_Din_A(10) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(21),
      BRAM_Din_A(11) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(20),
      BRAM_Din_A(12) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(19),
      BRAM_Din_A(13) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(18),
      BRAM_Din_A(14) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(17),
      BRAM_Din_A(15) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(16),
      BRAM_Din_A(16) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(15),
      BRAM_Din_A(17) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(14),
      BRAM_Din_A(18) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(13),
      BRAM_Din_A(19) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(12),
      BRAM_Din_A(20) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(11),
      BRAM_Din_A(21) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(10),
      BRAM_Din_A(22) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(9),
      BRAM_Din_A(23) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(8),
      BRAM_Din_A(24) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(7),
      BRAM_Din_A(25) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(6),
      BRAM_Din_A(26) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(5),
      BRAM_Din_A(27) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(4),
      BRAM_Din_A(28) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(3),
      BRAM_Din_A(29) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(2),
      BRAM_Din_A(30) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(1),
      BRAM_Din_A(31) => lmb_bram_if_cntlr_1_BRAM_PORT_DOUT(0),
      BRAM_Dout_A(0 to 31) => NLW_lmb_bram_if_cntlr_1_BRAM_Dout_A_UNCONNECTED(0 to 31),
      BRAM_EN_A => lmb_bram_if_cntlr_1_BRAM_PORT_EN,
      BRAM_Rst_A => lmb_bram_if_cntlr_1_BRAM_PORT_RST,
      BRAM_WEN_A(0 to 3) => NLW_lmb_bram_if_cntlr_1_BRAM_WEN_A_UNCONNECTED(0 to 3),
      LMB_ABus(0 to 31) => Conn2_ABUS(0 to 31),
      LMB_AddrStrobe => Conn2_ADDRSTROBE,
      LMB_BE(0 to 3) => Conn2_BE(0 to 3),
      LMB_Clk => clk_100MHz_1,
      LMB_ReadStrobe => Conn2_READSTROBE,
      LMB_Rst => rst_1,
      LMB_WriteDBus(0 to 31) => Conn2_WRITEDBUS(0 to 31),
      LMB_WriteStrobe => Conn2_WRITESTROBE,
      Sl_CE => Conn2_CE,
      Sl_DBus(0 to 31) => Conn2_READDBUS(0 to 31),
      Sl_Ready => Conn2_READY,
      Sl_UE => Conn2_UE,
      Sl_Wait => Conn2_WAIT
    );
lmb_v10_0: component mb_block_design_lmb_v10_0_0
     port map (
      LMB_ABus(0 to 31) => Conn1_ABUS(0 to 31),
      LMB_AddrStrobe => Conn1_ADDRSTROBE,
      LMB_BE(0 to 3) => Conn1_BE(0 to 3),
      LMB_CE => microblaze_0_DLMB_CE,
      LMB_Clk => clk_100MHz_1,
      LMB_ReadDBus(0 to 31) => microblaze_0_DLMB_READDBUS(0 to 31),
      LMB_ReadStrobe => Conn1_READSTROBE,
      LMB_Ready => microblaze_0_DLMB_READY,
      LMB_Rst => NLW_lmb_v10_0_LMB_Rst_UNCONNECTED,
      LMB_UE => microblaze_0_DLMB_UE,
      LMB_Wait => microblaze_0_DLMB_WAIT,
      LMB_WriteDBus(0 to 31) => Conn1_WRITEDBUS(0 to 31),
      LMB_WriteStrobe => Conn1_WRITESTROBE,
      M_ABus(0 to 31) => microblaze_0_DLMB_ABUS(0 to 31),
      M_AddrStrobe => microblaze_0_DLMB_ADDRSTROBE,
      M_BE(0 to 3) => microblaze_0_DLMB_BE(0 to 3),
      M_DBus(0 to 31) => microblaze_0_DLMB_WRITEDBUS(0 to 31),
      M_ReadStrobe => microblaze_0_DLMB_READSTROBE,
      M_WriteStrobe => microblaze_0_DLMB_WRITESTROBE,
      SYS_Rst => rst_1,
      Sl_CE(0) => Conn1_CE,
      Sl_DBus(0 to 31) => Conn1_READDBUS(0 to 31),
      Sl_Ready(0) => Conn1_READY,
      Sl_UE(0) => Conn1_UE,
      Sl_Wait(0) => Conn1_WAIT
    );
lmb_v10_1: component mb_block_design_lmb_v10_1_0
     port map (
      LMB_ABus(0 to 31) => Conn_ABUS(0 to 31),
      LMB_AddrStrobe => Conn_ADDRSTROBE,
      LMB_BE(0 to 3) => Conn_BE(0 to 3),
      LMB_CE => Conn3_CE,
      LMB_Clk => clk_100MHz_1,
      LMB_ReadDBus(0 to 31) => Conn3_READDBUS(0 to 31),
      LMB_ReadStrobe => Conn_READSTROBE,
      LMB_Ready => Conn3_READY,
      LMB_Rst => Conn3_RST,
      LMB_UE => Conn3_UE,
      LMB_Wait => Conn3_WAIT,
      LMB_WriteDBus(0 to 31) => Conn_WRITEDBUS(0 to 31),
      LMB_WriteStrobe => Conn_WRITESTROBE,
      M_ABus(0 to 31) => Conn3_ABUS(0 to 31),
      M_AddrStrobe => Conn3_ADDRSTROBE,
      M_BE(0 to 3) => Conn3_BE(0 to 3),
      M_DBus(0 to 31) => Conn3_WRITEDBUS(0 to 31),
      M_ReadStrobe => Conn3_READSTROBE,
      M_WriteStrobe => Conn3_WRITESTROBE,
      SYS_Rst => rst_1,
      Sl_CE(0) => Conn_CE,
      Sl_DBus(0 to 31) => Conn_READDBUS(0 to 31),
      Sl_Ready(0) => Conn_READY,
      Sl_UE(0) => Conn_UE,
      Sl_Wait(0) => Conn_WAIT
    );
lmb_v10_2: component mb_block_design_lmb_v10_2_0
     port map (
      LMB_ABus(0 to 31) => Conn2_ABUS(0 to 31),
      LMB_AddrStrobe => Conn2_ADDRSTROBE,
      LMB_BE(0 to 3) => Conn2_BE(0 to 3),
      LMB_CE => microblaze_0_ILMB_CE,
      LMB_Clk => clk_100MHz_1,
      LMB_ReadDBus(0 to 31) => microblaze_0_ILMB_READDBUS(0 to 31),
      LMB_ReadStrobe => Conn2_READSTROBE,
      LMB_Ready => microblaze_0_ILMB_READY,
      LMB_Rst => NLW_lmb_v10_2_LMB_Rst_UNCONNECTED,
      LMB_UE => microblaze_0_ILMB_UE,
      LMB_Wait => microblaze_0_ILMB_WAIT,
      LMB_WriteDBus(0 to 31) => Conn2_WRITEDBUS(0 to 31),
      LMB_WriteStrobe => Conn2_WRITESTROBE,
      M_ABus(0 to 31) => microblaze_0_ILMB_ABUS(0 to 31),
      M_AddrStrobe => microblaze_0_ILMB_ADDRSTROBE,
      M_BE(0 to 3) => B"0000",
      M_DBus(0 to 31) => B"00000000000000000000000000000000",
      M_ReadStrobe => microblaze_0_ILMB_READSTROBE,
      M_WriteStrobe => '0',
      SYS_Rst => rst_1,
      Sl_CE(0) => Conn2_CE,
      Sl_DBus(0 to 31) => Conn2_READDBUS(0 to 31),
      Sl_Ready(0) => Conn2_READY,
      Sl_UE(0) => Conn2_UE,
      Sl_Wait(0) => Conn2_WAIT
    );
microblaze_0: component mb_block_design_microblaze_0_0
     port map (
      Byte_Enable(0 to 3) => microblaze_0_DLMB_BE(0 to 3),
      Clk => clk_100MHz_1,
      DCE => microblaze_0_DLMB_CE,
      DReady => microblaze_0_DLMB_READY,
      DUE => microblaze_0_DLMB_UE,
      DWait => microblaze_0_DLMB_WAIT,
      D_AS => microblaze_0_DLMB_ADDRSTROBE,
      Data_Addr(0 to 31) => microblaze_0_DLMB_ABUS(0 to 31),
      Data_Read(0 to 31) => microblaze_0_DLMB_READDBUS(0 to 31),
      Data_Write(0 to 31) => microblaze_0_DLMB_WRITEDBUS(0 to 31),
      ICE => microblaze_0_ILMB_CE,
      IFetch => microblaze_0_ILMB_READSTROBE,
      IReady => microblaze_0_ILMB_READY,
      IUE => microblaze_0_ILMB_UE,
      IWAIT => microblaze_0_ILMB_WAIT,
      I_AS => microblaze_0_ILMB_ADDRSTROBE,
      Instr(0 to 31) => microblaze_0_ILMB_READDBUS(0 to 31),
      Instr_Addr(0 to 31) => microblaze_0_ILMB_ABUS(0 to 31),
      Interrupt => '0',
      Interrupt_Ack(0 to 1) => NLW_microblaze_0_Interrupt_Ack_UNCONNECTED(0 to 1),
      Interrupt_Address(0 to 31) => B"00000000000000000000000000000000",
      M_AXI_DP_ARADDR(31 downto 0) => microblaze_0_M_AXI_DP_ARADDR(31 downto 0),
      M_AXI_DP_ARPROT(2 downto 0) => microblaze_0_M_AXI_DP_ARPROT(2 downto 0),
      M_AXI_DP_ARREADY => microblaze_0_M_AXI_DP_ARREADY,
      M_AXI_DP_ARVALID => microblaze_0_M_AXI_DP_ARVALID,
      M_AXI_DP_AWADDR(31 downto 0) => microblaze_0_M_AXI_DP_AWADDR(31 downto 0),
      M_AXI_DP_AWPROT(2 downto 0) => microblaze_0_M_AXI_DP_AWPROT(2 downto 0),
      M_AXI_DP_AWREADY => microblaze_0_M_AXI_DP_AWREADY,
      M_AXI_DP_AWVALID => microblaze_0_M_AXI_DP_AWVALID,
      M_AXI_DP_BREADY => microblaze_0_M_AXI_DP_BREADY,
      M_AXI_DP_BRESP(1 downto 0) => microblaze_0_M_AXI_DP_BRESP(1 downto 0),
      M_AXI_DP_BVALID => microblaze_0_M_AXI_DP_BVALID,
      M_AXI_DP_RDATA(31 downto 0) => microblaze_0_M_AXI_DP_RDATA(31 downto 0),
      M_AXI_DP_RREADY => microblaze_0_M_AXI_DP_RREADY,
      M_AXI_DP_RRESP(1 downto 0) => microblaze_0_M_AXI_DP_RRESP(1 downto 0),
      M_AXI_DP_RVALID => microblaze_0_M_AXI_DP_RVALID,
      M_AXI_DP_WDATA(31 downto 0) => microblaze_0_M_AXI_DP_WDATA(31 downto 0),
      M_AXI_DP_WREADY => microblaze_0_M_AXI_DP_WREADY,
      M_AXI_DP_WSTRB(3 downto 0) => microblaze_0_M_AXI_DP_WSTRB(3 downto 0),
      M_AXI_DP_WVALID => microblaze_0_M_AXI_DP_WVALID,
      Read_Strobe => microblaze_0_DLMB_READSTROBE,
      Reset => rst_1,
      Write_Strobe => microblaze_0_DLMB_WRITESTROBE
    );
end STRUCTURE;
