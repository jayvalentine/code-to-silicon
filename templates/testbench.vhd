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
use IEEE.NUMERIC_STD.ALL;

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

            m_rdy                   : out std_logic;
            m_wr                    : in std_logic;
            m_rd                    : in std_logic;

            m_addr                  : in std_logic_vector(31 downto 0);
            m_data_to_accel         : out std_logic_vector(31 downto 0);
            m_data_from_accel       : in std_logic_vector(31 downto 0);
            accel_select            : out std_logic_vector(31 downto 0);

            reg_from_accel_01       : in std_logic_vector(31 downto 0);
            reg_from_accel_02       : in std_logic_vector(31 downto 0);
            reg_from_accel_03       : in std_logic_vector(31 downto 0);
            reg_from_accel_04       : in std_logic_vector(31 downto 0);
            reg_from_accel_05       : in std_logic_vector(31 downto 0);
            reg_from_accel_06       : in std_logic_vector(31 downto 0);
            reg_from_accel_07       : in std_logic_vector(31 downto 0);
            reg_from_accel_08       : in std_logic_vector(31 downto 0);
            reg_from_accel_09       : in std_logic_vector(31 downto 0);
            reg_from_accel_10       : in std_logic_vector(31 downto 0);
            reg_from_accel_11       : in std_logic_vector(31 downto 0);
            reg_from_accel_12       : in std_logic_vector(31 downto 0);
            reg_from_accel_13       : in std_logic_vector(31 downto 0);
            reg_from_accel_14       : in std_logic_vector(31 downto 0);
            reg_from_accel_15       : in std_logic_vector(31 downto 0);
            reg_from_accel_16       : in std_logic_vector(31 downto 0);
            reg_from_accel_17       : in std_logic_vector(31 downto 0);
            reg_from_accel_18       : in std_logic_vector(31 downto 0);
            reg_from_accel_19       : in std_logic_vector(31 downto 0);
            reg_from_accel_20       : in std_logic_vector(31 downto 0);
            reg_from_accel_21       : in std_logic_vector(31 downto 0);
            reg_from_accel_22       : in std_logic_vector(31 downto 0);
            reg_from_accel_23       : in std_logic_vector(31 downto 0);
            reg_from_accel_24       : in std_logic_vector(31 downto 0);
            reg_from_accel_25       : in std_logic_vector(31 downto 0);
            reg_from_accel_26       : in std_logic_vector(31 downto 0);
            reg_from_accel_27       : in std_logic_vector(31 downto 0);
            reg_from_accel_28       : in std_logic_vector(31 downto 0);
            reg_from_accel_29       : in std_logic_vector(31 downto 0);
            reg_from_accel_30       : in std_logic_vector(31 downto 0);
            reg_from_accel_31       : in std_logic_vector(31 downto 0);

            reg_to_accel_01         : out std_logic_vector(31 downto 0);
            reg_to_accel_02         : out std_logic_vector(31 downto 0);
            reg_to_accel_03         : out std_logic_vector(31 downto 0);
            reg_to_accel_04         : out std_logic_vector(31 downto 0);
            reg_to_accel_05         : out std_logic_vector(31 downto 0);
            reg_to_accel_06         : out std_logic_vector(31 downto 0);
            reg_to_accel_07         : out std_logic_vector(31 downto 0);
            reg_to_accel_08         : out std_logic_vector(31 downto 0);
            reg_to_accel_09         : out std_logic_vector(31 downto 0);
            reg_to_accel_10         : out std_logic_vector(31 downto 0);
            reg_to_accel_11         : out std_logic_vector(31 downto 0);
            reg_to_accel_12         : out std_logic_vector(31 downto 0);
            reg_to_accel_13         : out std_logic_vector(31 downto 0);
            reg_to_accel_14         : out std_logic_vector(31 downto 0);
            reg_to_accel_15         : out std_logic_vector(31 downto 0);
            reg_to_accel_16         : out std_logic_vector(31 downto 0);
            reg_to_accel_17         : out std_logic_vector(31 downto 0);
            reg_to_accel_18         : out std_logic_vector(31 downto 0);
            reg_to_accel_19         : out std_logic_vector(31 downto 0);
            reg_to_accel_20         : out std_logic_vector(31 downto 0);
            reg_to_accel_21         : out std_logic_vector(31 downto 0);
            reg_to_accel_22         : out std_logic_vector(31 downto 0);
            reg_to_accel_23         : out std_logic_vector(31 downto 0);
            reg_to_accel_24         : out std_logic_vector(31 downto 0);
            reg_to_accel_25         : out std_logic_vector(31 downto 0);
            reg_to_accel_26         : out std_logic_vector(31 downto 0);
            reg_to_accel_27         : out std_logic_vector(31 downto 0);
            reg_to_accel_28         : out std_logic_vector(31 downto 0);
            reg_to_accel_29         : out std_logic_vector(31 downto 0);
            reg_to_accel_30         : out std_logic_vector(31 downto 0);
            reg_to_accel_31         : out std_logic_vector(31 downto 0);

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
            LMB_M_0_writestrobe     : out std_logic;

            M_AXI_DP_0_araddr       : in STD_LOGIC_VECTOR (31 downto 0);
            M_AXI_DP_0_arprot       : in STD_LOGIC_VECTOR (2 downto 0);
            M_AXI_DP_0_arready      : out STD_LOGIC;
            M_AXI_DP_0_arvalid      : in STD_LOGIC;
            M_AXI_DP_0_awaddr       : in STD_LOGIC_VECTOR (31 downto 0);
            M_AXI_DP_0_awprot       : in STD_LOGIC_VECTOR (2 downto 0);
            M_AXI_DP_0_awready      : out STD_LOGIC;
            M_AXI_DP_0_awvalid      : in STD_LOGIC;
            M_AXI_DP_0_bready       : in STD_LOGIC;
            M_AXI_DP_0_bresp        : out STD_LOGIC_VECTOR (1 downto 0);
            M_AXI_DP_0_bvalid       : out STD_LOGIC;
            M_AXI_DP_0_rdata        : out STD_LOGIC_VECTOR (31 downto 0);
            M_AXI_DP_0_rready       : in STD_LOGIC;
            M_AXI_DP_0_rresp        : out STD_LOGIC_VECTOR (1 downto 0);
            M_AXI_DP_0_rvalid       : out STD_LOGIC;
            M_AXI_DP_0_wdata        : in STD_LOGIC_VECTOR (31 downto 0);
            M_AXI_DP_0_wready       : out STD_LOGIC;
            M_AXI_DP_0_wstrb        : in STD_LOGIC_VECTOR (3 downto 0);
            M_AXI_DP_0_wvalid       : in STD_LOGIC
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

%%STATEMACHINE_COMPONENTS%%

    signal clk                      : std_logic;
    signal rst                      : std_logic;

    signal accel_select             : std_logic_vector(31 downto 0);

    signal reg_from_accel_01       : std_logic_vector(31 downto 0);
    signal reg_from_accel_02       : std_logic_vector(31 downto 0);
    signal reg_from_accel_03       : std_logic_vector(31 downto 0);
    signal reg_from_accel_04       : std_logic_vector(31 downto 0);
    signal reg_from_accel_05       : std_logic_vector(31 downto 0);
    signal reg_from_accel_06       : std_logic_vector(31 downto 0);
    signal reg_from_accel_07       : std_logic_vector(31 downto 0);
    signal reg_from_accel_08       : std_logic_vector(31 downto 0);
    signal reg_from_accel_09       : std_logic_vector(31 downto 0);
    signal reg_from_accel_10       : std_logic_vector(31 downto 0);
    signal reg_from_accel_11       : std_logic_vector(31 downto 0);
    signal reg_from_accel_12       : std_logic_vector(31 downto 0);
    signal reg_from_accel_13       : std_logic_vector(31 downto 0);
    signal reg_from_accel_14       : std_logic_vector(31 downto 0);
    signal reg_from_accel_15       : std_logic_vector(31 downto 0);
    signal reg_from_accel_16       : std_logic_vector(31 downto 0);
    signal reg_from_accel_17       : std_logic_vector(31 downto 0);
    signal reg_from_accel_18       : std_logic_vector(31 downto 0);
    signal reg_from_accel_19       : std_logic_vector(31 downto 0);
    signal reg_from_accel_20       : std_logic_vector(31 downto 0);
    signal reg_from_accel_21       : std_logic_vector(31 downto 0);
    signal reg_from_accel_22       : std_logic_vector(31 downto 0);
    signal reg_from_accel_23       : std_logic_vector(31 downto 0);
    signal reg_from_accel_24       : std_logic_vector(31 downto 0);
    signal reg_from_accel_25       : std_logic_vector(31 downto 0);
    signal reg_from_accel_26       : std_logic_vector(31 downto 0);
    signal reg_from_accel_27       : std_logic_vector(31 downto 0);    signal reg_out                  : std_logic_vector(991 downto 0);
    signal reg_in                   : std_logic_vector(991 downto 0);
    signal reg_from_accel_28       : std_logic_vector(31 downto 0);
    signal reg_from_accel_29       : std_logic_vector(31 downto 0);
    signal reg_from_accel_30       : std_logic_vector(31 downto 0);
    signal reg_from_accel_31       : std_logic_vector(31 downto 0);

    signal reg_to_accel_01         : std_logic_vector(31 downto 0);
    signal reg_to_accel_02         : std_logic_vector(31 downto 0);
    signal reg_to_accel_03         : std_logic_vector(31 downto 0);
    signal reg_to_accel_04         : std_logic_vector(31 downto 0);
    signal reg_to_accel_05         : std_logic_vector(31 downto 0);
    signal reg_to_accel_06         : std_logic_vector(31 downto 0);
    signal reg_to_accel_07         : std_logic_vector(31 downto 0);
    signal reg_to_accel_08         : std_logic_vector(31 downto 0);
    signal reg_to_accel_09         : std_logic_vector(31 downto 0);
    signal reg_to_accel_10         : std_logic_vector(31 downto 0);
    signal reg_to_accel_11         : std_logic_vector(31 downto 0);
    signal reg_to_accel_12         : std_logic_vector(31 downto 0);
    signal reg_to_accel_13         : std_logic_vector(31 downto 0);
    signal reg_to_accel_14         : std_logic_vector(31 downto 0);
    signal reg_to_accel_15         : std_logic_vector(31 downto 0);
    signal reg_to_accel_16         : std_logic_vector(31 downto 0);
    signal reg_to_accel_17         : std_logic_vector(31 downto 0);
    signal reg_to_accel_18         : std_logic_vector(31 downto 0);
    signal reg_to_accel_19         : std_logic_vector(31 downto 0);
    signal reg_to_accel_20         : std_logic_vector(31 downto 0);
    signal reg_to_accel_21         : std_logic_vector(31 downto 0);
    signal reg_to_accel_22         : std_logic_vector(31 downto 0);
    signal reg_to_accel_23         : std_logic_vector(31 downto 0);
    signal reg_to_accel_24         : std_logic_vector(31 downto 0);
    signal reg_to_accel_25         : std_logic_vector(31 downto 0);
    signal reg_to_accel_26         : std_logic_vector(31 downto 0);
    signal reg_to_accel_27         : std_logic_vector(31 downto 0);
    signal reg_to_accel_28         : std_logic_vector(31 downto 0);
    signal reg_to_accel_29         : std_logic_vector(31 downto 0);
    signal reg_to_accel_30         : std_logic_vector(31 downto 0);
    signal reg_to_accel_31         : std_logic_vector(31 downto 0);

    signal m_rdy                    : std_logic;
    signal m_rd                     : std_logic;
    signal m_wr                     : std_logic;

    signal m_addr                   : STD_LOGIC_VECTOR(31 downto 0);
    signal m_data_to_accel          : STD_LOGIC_VECTOR(31 downto 0);
    signal m_data_from_accel        : STD_LOGIC_VECTOR(31 downto 0);

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

%%STATEMACHINE_SIGNALS%%

    constant clk_period             : time := 10ns;
    signal clk_hold                 : std_logic := '0';
    signal cycles                   : Integer := 0;

    function byte_to_hex(b: std_logic_vector(7 downto 0)) return string is
        variable upper : character;
        variable lower : character;

        variable returnString : string(1 to 2);
    begin
        case b(7 downto 4) is
            when "0000" => upper := '0';
            when "0001" => upper := '1';
            when "0010" => upper := '2';
            when "0011" => upper := '3';
            when "0100" => upper := '4';
            when "0101" => upper := '5';
            when "0110" => upper := '6';
            when "0111" => upper := '7';
            when "1000" => upper := '8';
            when "1001" => upper := '9';
            when "1010" => upper := 'A';
            when "1011" => upper := 'B';
            when "1100" => upper := 'C';
            when "1101" => upper := 'D';
            when "1110" => upper := 'E';
            when "1111" => upper := 'F';
        end case;

        case b(3 downto 0) is
            when "0000" => lower := '0';
            when "0001" => lower := '1';
            when "0010" => lower := '2';
            when "0011" => lower := '3';
            when "0100" => lower := '4';
            when "0101" => lower := '5';
            when "0110" => lower := '6';
            when "0111" => lower := '7';
            when "1000" => lower := '8';
            when "1001" => lower := '9';
            when "1010" => lower := 'A';
            when "1011" => lower := 'B';
            when "1100" => lower := 'C';
            when "1101" => lower := 'D';
            when "1110" => lower := 'E';
            when "1111" => lower := 'F';
        end case;

        returnString := upper & lower;
        return returnString;
    end byte_to_hex;


    function std_logic_vec_to_hex(vec: std_logic_vector(31 downto 0)) return string is
        variable byte1 : std_logic_vector(7 downto 0);
        variable byte2 : std_logic_vector(7 downto 0);
        variable byte3 : std_logic_vector(7 downto 0);
        variable byte4 : std_logic_vector(7 downto 0);

        variable returnString : string(1 to 8);
    begin
        byte1 := vec(31 downto 24);
        byte2 := vec(23 downto 16);
        byte3 := vec(15 downto 8);
        byte4 := vec(7 downto 0);

        returnString := byte_to_hex(byte1) & byte_to_hex(byte2) & byte_to_hex(byte3) & byte_to_hex(byte4);
        return returnString;
    end std_logic_vec_to_hex;
begin
    hw_accel_controller_uut: hw_accel_controller port map
    (
        clk                     => clk,
        rst                     => rst,

        reg_from_accel_01       => reg_from_accel_01,
        reg_from_accel_02       => reg_from_accel_02,
        reg_from_accel_03       => reg_from_accel_03,
        reg_from_accel_04       => reg_from_accel_04,
        reg_from_accel_05       => reg_from_accel_05,
        reg_from_accel_06       => reg_from_accel_06,
        reg_from_accel_07       => reg_from_accel_07,
        reg_from_accel_08       => reg_from_accel_08,
        reg_from_accel_09       => reg_from_accel_09,
        reg_from_accel_10       => reg_from_accel_10,
        reg_from_accel_11       => reg_from_accel_11,
        reg_from_accel_12       => reg_from_accel_12,
        reg_from_accel_13       => reg_from_accel_13,
        reg_from_accel_14       => reg_from_accel_14,
        reg_from_accel_15       => reg_from_accel_15,
        reg_from_accel_16       => reg_from_accel_16,
        reg_from_accel_17       => reg_from_accel_17,
        reg_from_accel_18       => reg_from_accel_18,
        reg_from_accel_19       => reg_from_accel_19,
        reg_from_accel_20       => reg_from_accel_20,
        reg_from_accel_21       => reg_from_accel_21,
        reg_from_accel_22       => reg_from_accel_22,
        reg_from_accel_23       => reg_from_accel_23,
        reg_from_accel_24       => reg_from_accel_24,
        reg_from_accel_25       => reg_from_accel_25,
        reg_from_accel_26       => reg_from_accel_26,
        reg_from_accel_27       => reg_from_accel_27,
        reg_from_accel_28       => reg_from_accel_28,
        reg_from_accel_29       => reg_from_accel_29,
        reg_from_accel_30       => reg_from_accel_30,
        reg_from_accel_31       => reg_from_accel_31,

        reg_to_accel_01         => reg_to_accel_01,
        reg_to_accel_02         => reg_to_accel_02,
        reg_to_accel_03         => reg_to_accel_03,
        reg_to_accel_04         => reg_to_accel_04,
        reg_to_accel_05         => reg_to_accel_05,
        reg_to_accel_06         => reg_to_accel_06,
        reg_to_accel_07         => reg_to_accel_07,
        reg_to_accel_08         => reg_to_accel_08,
        reg_to_accel_09         => reg_to_accel_09,
        reg_to_accel_10         => reg_to_accel_10,
        reg_to_accel_11         => reg_to_accel_11,
        reg_to_accel_12         => reg_to_accel_12,
        reg_to_accel_13         => reg_to_accel_13,
        reg_to_accel_14         => reg_to_accel_14,
        reg_to_accel_15         => reg_to_accel_15,
        reg_to_accel_16         => reg_to_accel_16,
        reg_to_accel_17         => reg_to_accel_17,
        reg_to_accel_18         => reg_to_accel_18,
        reg_to_accel_19         => reg_to_accel_19,
        reg_to_accel_20         => reg_to_accel_20,
        reg_to_accel_21         => reg_to_accel_21,
        reg_to_accel_22         => reg_to_accel_22,
        reg_to_accel_23         => reg_to_accel_23,
        reg_to_accel_24         => reg_to_accel_24,
        reg_to_accel_25         => reg_to_accel_25,
        reg_to_accel_26         => reg_to_accel_26,
        reg_to_accel_27         => reg_to_accel_27,
        reg_to_accel_28         => reg_to_accel_28,
        reg_to_accel_29         => reg_to_accel_29,
        reg_to_accel_30         => reg_to_accel_30,
        reg_to_accel_31         => reg_to_accel_31,

        m_rdy                   => m_rdy,
        m_rd                    => m_rd,
        m_wr                    => m_wr,

        m_addr                  => m_addr,
        m_data_to_accel         => m_data_to_accel,
        m_data_from_accel       => m_data_from_accel,

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
        M_AXI_DP_0_arprot       => M_AXI_DP_0_arprot,
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
        M_AXI_DP_0_wvalid       => M_AXI_DP_0_wvalid
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

%%STATEMACHINE_UUTS%%

    clk_proc : process
    begin
        if clk_hold = '1' then
            wait;

        else
            clk <= '0';
            wait for clk_period/2;
            clk <= '1';
            wait for clk_period/2;
            cycles <= cycles + 1;
        end if;
    end process clk_proc;

    test_proc : process
    begin
        rst <= '1';
        clk_hold <= '0';
        wait for clk_period;
        rst <= '0';

        loop
            -- Report any writes on the AXI bus.
            if M_AXI_DP_0_wvalid = '1' and M_AXI_DP_0_awvalid = '1' then
                report "TESTBENCH: AXI WRITE DETECTED.";
                report "TESTBENCH: ADDR: " & std_logic_vec_to_hex(M_AXI_DP_0_awaddr);
                report "TESTBENCH: DATA: " & std_logic_vec_to_hex(M_AXI_DP_0_wdata);
            end if;

            -- Report any reads on the AXI bus.
            if M_AXI_DP_0_rvalid = '1' and M_AXI_DP_0_arvalid = '1' then
                report "TESTBENCH: AXI READ DETECTED.";
                report "TESTBENCH: ADDR: " & std_logic_vec_to_hex(M_AXI_DP_0_araddr);
                report "TESTBENCH: DATA: " & std_logic_vec_to_hex(M_AXI_DP_0_rdata);
            end if;

            -- Trap if we reach the test_failed function, and report the test failure.
            if BRAM_PORT_INST_addr = x"%%FAILED_ADDR%%" then
                report "TESTBENCH: !!!FAILED!!!";
                clk_hold <= '1';
                exit;
            -- Likewise, trap if we reach the test_passed function, and report the passing test.
            elsif BRAM_PORT_INST_addr = x"%%PASSED_ADDR%%" then
                report "TESTBENCH: !!!PASSED!!!";
                clk_hold <= '1';
                exit;
            end if;

            wait for clk_period;
        end loop;

        report "TESTBENCH: CYCLES: " & Integer'image(cycles);

        wait;
    end process test_proc;
end Behavioral;
