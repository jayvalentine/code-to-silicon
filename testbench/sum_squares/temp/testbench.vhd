----------------------------------------------------------------------------------
-- Company:
-- Engineer:
--
-- Create Date: 18.02.2019 14:43:25
-- Design Name:
-- Module Name: testbench_test - Behavioral
-- Project Name:
-- Target Devices:
-- Tool Versions:
-- Description:
--
-- Dependencies:
--
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
--
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity testbench is
--  Port ( );
end testbench;

architecture Behavioral of testbench is
    component hw_accel_controller is
        port (
            clk                     : in std_logic;
            rst                     : in std_logic;

            accel_select            : out std_logic_vector(31 downto 0);
            reg_out                 : out std_logic_vector(991 downto 0);
            reg_in                  : in std_logic_vector(991 downto 0);

            LMB_M_0_abus            : out std_logic_vector(31 downto 0);
            LMB_M_0_addrstrobe      : out std_logic;
            LMB_M_0_be              : out std_logic_vector(3 downto 0);
            LMB_M_0_ce              : out std_logic;
            LMB_M_0_readdbus        : in std_logic_vector (31 downto 0);
            LMB_M_0_readstrobe      : out std_logic;
            LMB_M_0_ready           : in std_logic;
            LMB_M_0_rst             : in std_logic;
            LMB_M_0_ue              : in std_logic;
            LMB_M_0_wait            : in std_logic;
            LMB_M_0_writedbus       : out std_logic_vector(31 downto 0);
            LMB_M_0_writestrobe     : out std_logic
        );
    end component hw_accel_controller;

    component mb_block_design_wrapper is
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
    end component mb_block_design_wrapper;

    component memory is
        port (
            BRAM_PORT_INST_addr : in STD_LOGIC_VECTOR ( 0 to 31 );
            BRAM_PORT_INST_clk : in STD_LOGIC;
            BRAM_PORT_INST_din : in STD_LOGIC_VECTOR ( 0 to 31 );
            BRAM_PORT_INST_dout : out STD_LOGIC_VECTOR ( 0 to 31 );
            BRAM_PORT_INST_en : in STD_LOGIC;
            BRAM_PORT_INST_rst : in STD_LOGIC;
            BRAM_PORT_INST_we : in STD_LOGIC_VECTOR ( 0 to 3 );
            BRAM_PORT_DATA_addr : in STD_LOGIC_VECTOR ( 0 to 31 );
            BRAM_PORT_DATA_clk : in STD_LOGIC;
            BRAM_PORT_DATA_din : in STD_LOGIC_VECTOR ( 0 to 31 );
            BRAM_PORT_DATA_dout : out STD_LOGIC_VECTOR ( 0 to 31 );
            BRAM_PORT_DATA_en : in STD_LOGIC;
            BRAM_PORT_DATA_rst : in STD_LOGIC;
            BRAM_PORT_DATA_we : in STD_LOGIC_VECTOR ( 0 to 3 )
        );
    end component memory;

    signal clk                      : std_logic;
    signal rst                      : std_logic;

    signal accel_select             : std_logic_vector(31 downto 0);
    signal reg_out                  : std_logic_vector(991 downto 0);
    signal reg_in                   : std_logic_vector(991 downto 0);

    signal LMB_M_0_abus             : std_logic_vector(31 downto 0);
    signal LMB_M_0_addrstrobe       : std_logic;
    signal LMB_M_0_be               : std_logic_vector(3 downto 0);
    signal LMB_M_0_ce               : std_logic;
    signal LMB_M_0_readdbus         : std_logic_vector (31 downto 0);
    signal LMB_M_0_readstrobe       : std_logic;
    signal LMB_M_0_ready            : std_logic;
    signal LMB_M_0_rst              : std_logic;
    signal LMB_M_0_ue               : std_logic;
    signal LMB_M_0_wait             : std_logic;
    signal LMB_M_0_writedbus        : std_logic_vector(31 downto 0);
    signal LMB_M_0_writestrobe      : std_logic;

    signal M_AXI_DP_0_araddr  : STD_LOGIC_VECTOR ( 31 downto 0 );
    signal M_AXI_DP_0_arprot  : STD_LOGIC_VECTOR ( 2 downto 0 );
    signal M_AXI_DP_0_arready : STD_LOGIC;
    signal M_AXI_DP_0_arvalid : STD_LOGIC;
    signal M_AXI_DP_0_awaddr  : STD_LOGIC_VECTOR ( 31 downto 0 );
    signal M_AXI_DP_0_awprot  : STD_LOGIC_VECTOR ( 2 downto 0 );
    signal M_AXI_DP_0_awready : STD_LOGIC;
    signal M_AXI_DP_0_awvalid : STD_LOGIC;
    signal M_AXI_DP_0_bready  : STD_LOGIC;
    signal M_AXI_DP_0_bresp   : STD_LOGIC_VECTOR ( 1 downto 0 );
    signal M_AXI_DP_0_bvalid  : STD_LOGIC;
    signal M_AXI_DP_0_rdata   : STD_LOGIC_VECTOR ( 31 downto 0 );
    signal M_AXI_DP_0_rready  : STD_LOGIC;
    signal M_AXI_DP_0_rresp   : STD_LOGIC_VECTOR ( 1 downto 0 );
    signal M_AXI_DP_0_rvalid  : STD_LOGIC;
    signal M_AXI_DP_0_wdata   : STD_LOGIC_VECTOR ( 31 downto 0 );
    signal M_AXI_DP_0_wready  : STD_LOGIC;
    signal M_AXI_DP_0_wstrb   : STD_LOGIC_VECTOR ( 3 downto 0 );
    signal M_AXI_DP_0_wvalid  : STD_LOGIC;

    signal BRAM_PORT_INST_addr : STD_LOGIC_VECTOR ( 0 to 31 );
    signal BRAM_PORT_INST_clk  : STD_LOGIC;
    signal BRAM_PORT_INST_din  : STD_LOGIC_VECTOR ( 0 to 31 );
    signal BRAM_PORT_INST_dout : STD_LOGIC_VECTOR ( 0 to 31 );
    signal BRAM_PORT_INST_en   : STD_LOGIC;
    signal BRAM_PORT_INST_rst  : STD_LOGIC;
    signal BRAM_PORT_INST_we   : STD_LOGIC_VECTOR ( 0 to 3 );
    signal BRAM_PORT_DATA_addr : STD_LOGIC_VECTOR ( 0 to 31 );
    signal BRAM_PORT_DATA_clk  : STD_LOGIC;
    signal BRAM_PORT_DATA_din  : STD_LOGIC_VECTOR ( 0 to 31 );
    signal BRAM_PORT_DATA_dout : STD_LOGIC_VECTOR ( 0 to 31 );
    signal BRAM_PORT_DATA_en   : STD_LOGIC;
    signal BRAM_PORT_DATA_rst  : STD_LOGIC;
    signal BRAM_PORT_DATA_we   : STD_LOGIC_VECTOR ( 0 to 3 );

    constant clk_period             : time := 10ns;
    signal clk_hold                 : std_logic := '0';
begin
    hw_accel_controller_uut: hw_accel_controller port map
    (
        clk                     => clk,
        rst                     => rst,
        accel_select            => accel_select,
        reg_out                 => reg_out,
        reg_in                  => reg_in,

        LMB_M_0_abus            => LMB_M_0_abus,
        LMB_M_0_addrstrobe      => LMB_M_0_addrstrobe,
        LMB_M_0_be              => LMB_M_0_be,
        LMB_M_0_ce              => LMB_M_0_ce,
        LMB_M_0_readdbus        => LMB_M_0_readdbus,
        LMB_M_0_readstrobe      => LMB_M_0_readstrobe,
        LMB_M_0_ready           => LMB_M_0_ready,
        LMB_M_0_rst             => LMB_M_0_rst,
        LMB_M_0_ue              => LMB_M_0_ue,
        LMB_M_0_wait            => LMB_M_0_wait,
        LMB_M_0_writedbus       => LMB_M_0_writedbus,
        LMB_M_0_writestrobe     => LMB_M_0_writestrobe
    );

    mb_uut : mb_block_design_wrapper port map
    (
        clk_100MHz              => clk,
        rst                     => rst,

        LMB_M_0_abus            => LMB_M_0_abus,
        LMB_M_0_addrstrobe      => LMB_M_0_addrstrobe,
        LMB_M_0_be              => LMB_M_0_be,
        LMB_M_0_ce              => LMB_M_0_ce,
        LMB_M_0_readdbus        => LMB_M_0_readdbus,
        LMB_M_0_readstrobe      => LMB_M_0_readstrobe,
        LMB_M_0_ready           => LMB_M_0_ready,
        LMB_M_0_rst             => LMB_M_0_rst,
        LMB_M_0_ue              => LMB_M_0_ue,
        LMB_M_0_wait            => LMB_M_0_wait,
        LMB_M_0_writedbus       => LMB_M_0_writedbus,
        LMB_M_0_writestrobe     => LMB_M_0_writestrobe,

        M_AXI_DP_0_araddr       => M_AXI_DP_0_araddr,
        M_AXI_DP_0_arready      => M_AXI_DP_0_arready,
        M_AXI_DP_0_arvalid      => M_AXI_DP_0_arvalid,
        M_AXI_DP_0_awaddr       => M_AXI_DP_0_awaddr,
        M_AXI_DP_0_awprot       => M_AXI_DP_0_awprot,
        M_AXI_DP_0_awready      => M_AXI_DP_0_awready,
        M_AXI_DP_0_awvalid      => M_AXI_DP_0_awvalid,
        M_AXI_DP_0_bready       => M_AXI_DP_0_bready,
        M_AXI_DP_0_bresp        => M_AXI_DP_0_bresp,
        M_AXI_DP_0_bvalid       => M_AXI_DP_0_bvalid,
        M_AXI_DP_0_rdata        => M_AXI_DP_0_rdata,
        M_AXI_DP_0_rready       => M_AXI_DP_0_rready,
        M_AXI_DP_0_rresp        => M_AXI_DP_0_rresp,
        M_AXI_DP_0_rvalid       => M_AXI_DP_0_rvalid,
        M_AXI_DP_0_wdata        => M_AXI_DP_0_wdata,
        M_AXI_DP_0_wready       => M_AXI_DP_0_wready,
        M_AXI_DP_0_wstrb        => M_AXI_DP_0_wstrb,
        M_AXI_DP_0_wvalid       => M_AXI_DP_0_wvalid,

        BRAM_PORT_INST_addr     => BRAM_PORT_INST_addr,
        BRAM_PORT_INST_clk      => BRAM_PORT_INST_clk,
        BRAM_PORT_INST_din      => BRAM_PORT_INST_din,
        BRAM_PORT_INST_dout     => BRAM_PORT_INST_dout,
        BRAM_PORT_INST_en       => BRAM_PORT_INST_en,
        BRAM_PORT_INST_rst      => BRAM_PORT_INST_rst,
        BRAM_PORT_INST_we       => BRAM_PORT_INST_we,
        BRAM_PORT_DATA_addr     => BRAM_PORT_DATA_addr,
        BRAM_PORT_DATA_clk      => BRAM_PORT_DATA_clk,
        BRAM_PORT_DATA_din      => BRAM_PORT_DATA_din,
        BRAM_PORT_DATA_dout     => BRAM_PORT_DATA_dout,
        BRAM_PORT_DATA_en       => BRAM_PORT_DATA_en,
        BRAM_PORT_DATA_rst      => BRAM_PORT_DATA_rst,
        BRAM_PORT_DATA_we       => BRAM_PORT_DATA_we
    );

    mem_uut : memory port map
    (
        BRAM_PORT_INST_addr     => BRAM_PORT_INST_addr,
        BRAM_PORT_INST_clk      => BRAM_PORT_INST_clk,
        BRAM_PORT_INST_din      => BRAM_PORT_INST_din,
        BRAM_PORT_INST_dout     => BRAM_PORT_INST_dout,
        BRAM_PORT_INST_en       => BRAM_PORT_INST_en,
        BRAM_PORT_INST_rst      => BRAM_PORT_INST_rst,
        BRAM_PORT_INST_we       => BRAM_PORT_INST_we,
        BRAM_PORT_DATA_addr     => BRAM_PORT_DATA_addr,
        BRAM_PORT_DATA_clk      => BRAM_PORT_DATA_clk,
        BRAM_PORT_DATA_din      => BRAM_PORT_DATA_din,
        BRAM_PORT_DATA_dout     => BRAM_PORT_DATA_dout,
        BRAM_PORT_DATA_en       => BRAM_PORT_DATA_en,
        BRAM_PORT_DATA_rst      => BRAM_PORT_DATA_rst,
        BRAM_PORT_DATA_we       => BRAM_PORT_DATA_we
    );

    clk_proc : process
    begin
        if clk_hold = '1' then
            wait;

        else
            clk <= '0';
            wait for clk_period/2;
            clk <= '1';
            wait for clk_period/2;
        end if;
    end process clk_proc;

    test_proc : process
    begin
        rst <= '1';
        clk_hold <= '0';
        wait for clk_period;
        rst <= '0';

        loop
            -- Trap if we reach the test_failed function, and report the test failure.
            if BRAM_PORT_INST_addr = x"00000150" then
                report "TESTBENCH: FAILED";
                clk_hold <= '1';
                exit;
            -- Likewise, trap if we reach the test_passed function, and report the passing test.
            elsif BRAM_PORT_INST_addr = x"0000016c" then
                report "TESTBENCH: PASSED";
                clk_hold <= '1';
                exit;
            end if;

            wait for clk_period/8;
        end loop;

        wait;
    end process test_proc;
end Behavioral;
