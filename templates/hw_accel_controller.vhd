library IEEE;

use IEEE.STD_LOGIC_1164.all;

entity hw_accel_controller is
    port (
        clk                     : in std_logic;
        rst                     : in std_logic;

        wakeup                  : out std_logic_vector(1 downto 0);
        sleep                   : in std_logic;

        m_rdy                   : out std_logic;
        m_wr                    : in std_logic_vector(3 downto 0);
        m_rd                    : in std_logic;

        m_addr                  : in std_logic_vector(31 downto 0);
        m_data_to_accel         : out std_logic_vector(31 downto 0);
        m_data_from_accel       : in std_logic_vector(31 downto 0);

        carry_out               : in std_logic;
        carry_in                : out std_logic;

%%STATEMACHINE_PORTS%%

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
    type STATE is (
        S_DONE,
        S_WAITING_FOR_CORE,
        S_WAITING_FOR_MB,
        S_READY
    );

    type LMB_STATE is (
        LMB_DONE,
        LMB_WAITING_START,
        LMB_WAITING_END,
        LMB_READ,
        LMB_WRITE
    );

    signal int_state : STATE := S_READY;
    signal int_msr   : std_logic_vector(31 downto 0);
    signal int_lmb_state : LMB_STATE := LMB_WAITING_START;

    signal addr_latch : std_logic_vector(31 downto 0);
    signal addr_latch_set : std_logic;

begin
    control_proc : process(clk, rst)
    begin
        if rst = '1' then
            int_state <= S_READY;
            m_rdy <= '0';
            wakeup <= "00";

            LMB_M_0_addrstrobe <= '0';
            LMB_M_0_readstrobe <= '0';
            LMB_M_0_writestrobe <= '0';

            addr_latch <= (others => '0');
            addr_latch_set <= '0';

%%RESET_STATEMACHINES%%

%%DESELECT_STATEMACHINES%%

        else
            if rising_edge(clk) then
                case int_lmb_state is
                when LMB_WAITING_START =>
                    if m_rd = '1' then
                        LMB_M_0_abus <= m_addr;
                        LMB_M_0_addrstrobe <= '1';

                        LMB_M_0_readstrobe <= '1';

                        m_rdy <= '0';

                        int_lmb_state <= LMB_READ;

                    elsif m_wr /= "0000" and m_wr /= "ZZZZ" then
                        LMB_M_0_abus <= m_addr;
                        LMB_M_0_addrstrobe <= '1';

                        LMB_M_0_writedbus <= m_data_from_accel;
                        LMB_M_0_writestrobe <= '1';
                        LMB_M_0_be <= m_wr;

                        m_rdy <= '0';

                        int_lmb_state <= LMB_WRITE;
                    end if;

                when LMB_READ =>
                    if LMB_M_0_ready = '1' then
                        m_data_to_accel <= LMB_M_0_readdbus;
                        m_rdy <= '1';
                        int_lmb_state <= LMB_DONE;
                    end if;

                when LMB_WRITE =>
                    if LMB_M_0_ready = '1' then
                        m_rdy <= '1';
                        int_lmb_state <= LMB_DONE;
                    end if;

                when LMB_DONE =>
                    m_rdy <= '0';
                    LMB_M_0_readstrobe <= '0';
                    LMB_M_0_writestrobe <= '0';
                    LMB_M_0_addrstrobe <= '0';
                    int_lmb_state <= LMB_WAITING_END;

                when LMB_WAITING_END =>
                    int_lmb_state <= LMB_WAITING_START;

                end case;

%%UNRESET_STATEMACHINES%%

                wakeup <= "00";

                M_AXI_DP_0_awready <= '0';
                M_AXI_DP_0_wready <= '0';

                M_AXI_DP_0_bvalid <= '0';

                M_AXI_DP_0_arready <= '0';
                M_AXI_DP_0_rvalid <= '0';
                M_AXI_DP_0_rresp <= "10";

                case int_state is
                when S_WAITING_FOR_CORE =>
%%STATEMACHINES_DONE%%

                when S_READY =>
                    M_AXI_DP_0_awready <= '1';

                    M_AXI_DP_0_bresp <= "00";
                    M_AXI_DP_0_bvalid <= '1';

                    -- Write transaction: set data.
                    if M_AXI_DP_0_wvalid = '1' and addr_latch_set = '1' then
                        case addr_latch is
%%WRITE_REG_TO_ACCEL%%
                        when others => null;
                        end case;

                        addr_latch_set <= '0';
                        M_AXI_DP_0_wready <= '0';
                    end if;

		    -- Write transaction: set address latch.
                    if M_AXI_DP_0_awvalid = '1' then
                        addr_latch <= M_AXI_DP_0_awaddr;
                        addr_latch_set <= '1';
                        M_AXI_DP_0_wready <= '1';
                    end if;

                when S_DONE =>
                    if sleep = '0' then
                        int_state <= S_WAITING_FOR_MB;
                    end if;

                when S_WAITING_FOR_MB =>
                    M_AXI_DP_0_arready <= '1';

                    if M_AXI_DP_0_arvalid = '1' then
                        case M_AXI_DP_0_araddr is
%%READ_REG_FROM_ACCEL%%
                        when others => null;
                        end case;

                        M_AXI_DP_0_rvalid <= '1';
                    end if;
                end case;
            end if;
        end if;
    end process control_proc;
end architecture hw_accel_controller_behav;
