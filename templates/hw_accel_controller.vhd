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

%%STATEMACHINE_SEL_PORTS%%

%%STATEMACHINE_RST_PORTS%%

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
end entity hw_accel_controller;

architecture hw_accel_controller_behav of hw_accel_controller is
begin
    control_proc : process(rst, M_AXI_DP_0_awvalid, M_AXI_DP_0_wvalid, M_AXI_DP_0_arvalid, M_AXI_DP_0_rready)
    begin
        if rst = '1' then
%%RESET_STATEMACHINES%%

        else
            if M_AXI_DP_0_awvalid = '1' then
                M_AXI_DP_0_awready <= '1';
            else
                M_AXI_DP_0_awready <= '0';
            end if;

            -- Write transaction.
            if M_AXI_DP_0_wvalid = '1' then
                case M_AXI_DP_0_awaddr is
%%WRITE_REG_TO_ACCEL%%
                end case;

                M_AXI_DP_0_wready <= '1';
            else
                M_AXI_DP_0_wready <= '0';
            end if;

            if M_AXI_DP_0_arvalid = '1' then
                M_AXI_DP_0_arready <= '1';
            else
                M_AXI_DP_0_arready <= '0';
            end if;

            if M_AXI_DP_0_rready = '1' then
                case M_AXI_DP_0_araddr is
%%READ_REG_FROM_ACCEL%%
                end case;

                M_AXI_DP_0_rvalid <= '1';
            else
                M_AXI_DP_0_rvalid <= '0';
            end if;
        end if;
    end process control_proc;
end architecture hw_accel_controller_behav;