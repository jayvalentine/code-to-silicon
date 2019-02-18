library IEEE;

use IEEE.STD_LOGIC_1164.all;

entity hw_accel_controller is
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
end entity hw_accel_controller;

architecture hw_accel_controller_behav of hw_accel_controller is
begin
end architecture hw_accel_controller_behav;