library IEEE;

use IEEE.STD_LOGIC_1164.all;

entity hw_accel_controller is
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
end entity hw_accel_controller;

architecture hw_accel_controller_behav of hw_accel_controller is
begin
    dummy : process(M_AXI_DP_0_awvalid, M_AXI_DP_0_wvalid, M_AXI_DP_0_arvalid, M_AXI_DP_0_rready)
    begin
        -- Dummy response to write transaction.
        if M_AXI_DP_0_awvalid = '1' then
            M_AXI_DP_0_awready <= '1';
        else
            M_AXI_DP_0_awready <= '0';
        end if;

        if M_AXI_DP_0_wvalid = '1' then
            M_AXI_DP_0_wready <= '1';
        else
            M_AXI_DP_0_wready <= '0';
        end if;

        -- Dummy response to read transaction. Return 0x5A5A5A5A
        if M_AXI_DP_0_arvalid = '1' then
            M_AXI_DP_0_arready <= '1';
        else
            M_AXI_DP_0_arready <= '0';
        end if;

        if M_AXI_DP_0_rready = '1' then
            M_AXI_DP_0_rdata <= x"5A5A5A5A";
            M_AXI_DP_0_rvalid <= '1';
        else
            M_AXI_DP_0_rvalid <= '0';
        end if;
    end process dummy;
end architecture hw_accel_controller_behav;
