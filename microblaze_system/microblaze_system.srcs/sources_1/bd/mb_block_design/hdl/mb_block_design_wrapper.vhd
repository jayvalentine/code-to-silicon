--Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2018.2.1 (lin64) Build 2288692 Thu Jul 26 18:23:50 MDT 2018
--Date        : Wed Feb 20 12:53:30 2019
--Host        : cse069pc-35 running 64-bit Ubuntu 18.04.2 LTS
--Command     : generate_target mb_block_design_wrapper.bd
--Design      : mb_block_design_wrapper
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity mb_block_design_wrapper is
  port (
    BRAM_PORT_DATA_addr : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_DATA_clk : out STD_LOGIC;
    BRAM_PORT_DATA_din : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_DATA_dout : in STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_DATA_en : out STD_LOGIC;
    BRAM_PORT_DATA_rst : out STD_LOGIC;
    BRAM_PORT_DATA_we : out STD_LOGIC_VECTOR ( 0 to 3 );
    BRAM_PORT_INST_addr : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_INST_clk : out STD_LOGIC;
    BRAM_PORT_INST_din : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_INST_dout : in STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_INST_en : out STD_LOGIC;
    BRAM_PORT_INST_rst : out STD_LOGIC;
    BRAM_PORT_INST_we : out STD_LOGIC_VECTOR ( 0 to 3 );
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
end mb_block_design_wrapper;

architecture STRUCTURE of mb_block_design_wrapper is
  component mb_block_design is
  port (
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
    BRAM_PORT_INST_addr : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_INST_clk : out STD_LOGIC;
    BRAM_PORT_INST_din : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_INST_dout : in STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_INST_en : out STD_LOGIC;
    BRAM_PORT_INST_rst : out STD_LOGIC;
    BRAM_PORT_INST_we : out STD_LOGIC_VECTOR ( 0 to 3 );
    BRAM_PORT_DATA_addr : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_DATA_clk : out STD_LOGIC;
    BRAM_PORT_DATA_din : out STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_DATA_dout : in STD_LOGIC_VECTOR ( 0 to 31 );
    BRAM_PORT_DATA_en : out STD_LOGIC;
    BRAM_PORT_DATA_rst : out STD_LOGIC;
    BRAM_PORT_DATA_we : out STD_LOGIC_VECTOR ( 0 to 3 );
    clk_100MHz : in STD_LOGIC;
    rst : in STD_LOGIC
  );
  end component mb_block_design;
begin
mb_block_design_i: component mb_block_design
     port map (
      BRAM_PORT_DATA_addr(0 to 31) => BRAM_PORT_DATA_addr(0 to 31),
      BRAM_PORT_DATA_clk => BRAM_PORT_DATA_clk,
      BRAM_PORT_DATA_din(0 to 31) => BRAM_PORT_DATA_din(0 to 31),
      BRAM_PORT_DATA_dout(0 to 31) => BRAM_PORT_DATA_dout(0 to 31),
      BRAM_PORT_DATA_en => BRAM_PORT_DATA_en,
      BRAM_PORT_DATA_rst => BRAM_PORT_DATA_rst,
      BRAM_PORT_DATA_we(0 to 3) => BRAM_PORT_DATA_we(0 to 3),
      BRAM_PORT_INST_addr(0 to 31) => BRAM_PORT_INST_addr(0 to 31),
      BRAM_PORT_INST_clk => BRAM_PORT_INST_clk,
      BRAM_PORT_INST_din(0 to 31) => BRAM_PORT_INST_din(0 to 31),
      BRAM_PORT_INST_dout(0 to 31) => BRAM_PORT_INST_dout(0 to 31),
      BRAM_PORT_INST_en => BRAM_PORT_INST_en,
      BRAM_PORT_INST_rst => BRAM_PORT_INST_rst,
      BRAM_PORT_INST_we(0 to 3) => BRAM_PORT_INST_we(0 to 3),
      LMB_M_0_abus(0 to 31) => LMB_M_0_abus(0 to 31),
      LMB_M_0_addrstrobe => LMB_M_0_addrstrobe,
      LMB_M_0_be(0 to 3) => LMB_M_0_be(0 to 3),
      LMB_M_0_ce => LMB_M_0_ce,
      LMB_M_0_readdbus(0 to 31) => LMB_M_0_readdbus(0 to 31),
      LMB_M_0_readstrobe => LMB_M_0_readstrobe,
      LMB_M_0_ready => LMB_M_0_ready,
      LMB_M_0_rst => LMB_M_0_rst,
      LMB_M_0_ue => LMB_M_0_ue,
      LMB_M_0_wait => LMB_M_0_wait,
      LMB_M_0_writedbus(0 to 31) => LMB_M_0_writedbus(0 to 31),
      LMB_M_0_writestrobe => LMB_M_0_writestrobe,
      M_AXI_DP_0_araddr(31 downto 0) => M_AXI_DP_0_araddr(31 downto 0),
      M_AXI_DP_0_arprot(2 downto 0) => M_AXI_DP_0_arprot(2 downto 0),
      M_AXI_DP_0_arready => M_AXI_DP_0_arready,
      M_AXI_DP_0_arvalid => M_AXI_DP_0_arvalid,
      M_AXI_DP_0_awaddr(31 downto 0) => M_AXI_DP_0_awaddr(31 downto 0),
      M_AXI_DP_0_awprot(2 downto 0) => M_AXI_DP_0_awprot(2 downto 0),
      M_AXI_DP_0_awready => M_AXI_DP_0_awready,
      M_AXI_DP_0_awvalid => M_AXI_DP_0_awvalid,
      M_AXI_DP_0_bready => M_AXI_DP_0_bready,
      M_AXI_DP_0_bresp(1 downto 0) => M_AXI_DP_0_bresp(1 downto 0),
      M_AXI_DP_0_bvalid => M_AXI_DP_0_bvalid,
      M_AXI_DP_0_rdata(31 downto 0) => M_AXI_DP_0_rdata(31 downto 0),
      M_AXI_DP_0_rready => M_AXI_DP_0_rready,
      M_AXI_DP_0_rresp(1 downto 0) => M_AXI_DP_0_rresp(1 downto 0),
      M_AXI_DP_0_rvalid => M_AXI_DP_0_rvalid,
      M_AXI_DP_0_wdata(31 downto 0) => M_AXI_DP_0_wdata(31 downto 0),
      M_AXI_DP_0_wready => M_AXI_DP_0_wready,
      M_AXI_DP_0_wstrb(3 downto 0) => M_AXI_DP_0_wstrb(3 downto 0),
      M_AXI_DP_0_wvalid => M_AXI_DP_0_wvalid,
      clk_100MHz => clk_100MHz,
      rst => rst
    );
end STRUCTURE;
