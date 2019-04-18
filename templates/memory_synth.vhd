----------------------------------------------------------------------------------
-- Company:
-- Engineer:
--
-- Create Date: 19.02.2019 11:56:40
-- Design Name:
-- Module Name: memory - memory_behav
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

use STD.TEXTIO.ALL;
use IEEE.STD_LOGIC_TEXTIO.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity memory is
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
end memory;

architecture memory_behav of memory is
    type mem_8kx8 is array(0 to 2047) of std_logic_vector(31 downto 0);

    signal ram : mem_8kx8;

begin
    inst_mem_proc : process(BRAM_PORT_INST_clk, BRAM_PORT_INST_rst)
    begin
        -- Reset of INST port.
        if BRAM_PORT_INST_rst = '1' then
            BRAM_PORT_INST_dout <= (others => '0');
        -- Rising edge of INST clk.
        elsif rising_edge(BRAM_PORT_INST_clk) and BRAM_PORT_INST_en = '1' then
            -- All WE LOW: Read data.
            if BRAM_PORT_INST_we = "0000" then
                BRAM_PORT_INST_dout <= ram(to_integer(unsigned(BRAM_PORT_INST_addr)));
            -- WE: write to at least one byte.
            else
                ram(to_integer(unsigned(BRAM_PORT_INST_addr))) <= BRAM_PORT_INST_din;
            end if;
        end if;
    end process inst_mem_proc;

    data_mem_proc : process(BRAM_PORT_DATA_clk, BRAM_PORT_DATA_rst)
        variable data_addr_aligned : Integer;
    begin
        -- Reset of DATA port.
        if BRAM_PORT_DATA_rst = '1' then
            BRAM_PORT_DATA_dout <= (others => '0');
        -- Rising edge of DATA clk.
        elsif rising_edge(BRAM_PORT_DATA_clk) and BRAM_PORT_DATA_en = '1' then
            -- Align address on word boundary.
            data_addr_aligned := (to_integer(unsigned(BRAM_PORT_DATA_addr)) / 4) * 4;

            -- All WE LOW: Read data.
            if BRAM_PORT_DATA_we = "0000" then
                BRAM_PORT_DATA_dout <= ram(to_integer(unsigned(BRAM_PORT_DATA_addr)));
            -- WE: write to at least one byte.
            else
                ram(to_integer(unsigned(BRAM_PORT_DATA_addr))) <= BRAM_PORT_DATA_din;
            end if;
        end if;
    end process data_mem_proc;

end memory_behav;
