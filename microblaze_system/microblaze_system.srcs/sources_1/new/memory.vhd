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
    type mem_2kx32 is array (0 to 2047) of std_logic_vector(31 downto 0);
    signal ram : mem_2kx32 := (
        x"b00044a0",
        x"20200000",
        x"2040000f",
        x"f8410000",
        others => x"00000000");

begin
    mem_proc : process(BRAM_PORT_INST_clk, BRAM_PORT_INST_rst, BRAM_PORT_DATA_clk, BRAM_PORT_DATA_rst)
    begin
        -- Reset of INST port.
        if BRAM_PORT_INST_rst = '1' then
            BRAM_PORT_INST_dout <= (others => '0');
        -- Rising edge of INST clk.
        elsif rising_edge(BRAM_PORT_INST_clk) and BRAM_PORT_INST_en = '1' then
            -- All WE LOW: Read data.
            if BRAM_PORT_INST_we = "0000" then
                BRAM_PORT_INST_dout <= ram(to_integer(unsigned(BRAM_PORT_INST_addr))/4);
            -- WE: write to at least one byte
            else
                -- First byte write, if applicable.
                if BRAM_PORT_INST_we(0) = '1' then
                    ram(to_integer(unsigned(BRAM_PORT_INST_addr))/4)(7 downto 0) <= BRAM_PORT_INST_din(7 downto 0);
                end if;
                
                -- Second byte write, if applicable.
                if BRAM_PORT_INST_we(1) = '1' then
                    ram(to_integer(unsigned(BRAM_PORT_INST_addr))/4)(15 downto 8) <= BRAM_PORT_INST_din(15 downto 8);
                end if;
                
                -- Third byte write, if applicable.
                if BRAM_PORT_INST_we(2) = '1' then
                    ram(to_integer(unsigned(BRAM_PORT_INST_addr))/4)(23 downto 16) <= BRAM_PORT_INST_din(23 downto 16);
                end if;
                
                -- Fourth byte write, if applicable.
                if BRAM_PORT_INST_we(3) = '1' then
                    ram(to_integer(unsigned(BRAM_PORT_INST_addr))/4)(31 downto 24) <= BRAM_PORT_INST_din(31 downto 24);
                end if;
            end if;
        end if;
    end process mem_proc;

end memory_behav;
