----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/07/2018 08:59:32 PM
-- Design Name: 
-- Module Name: tb_wrapper - Behavioral
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

entity tb_wrapper is
--  Port ( );
end tb_wrapper;

architecture Behavioral of tb_wrapper is
    component wrapper is
         Port (
                reset: in std_logic;
                clk: in std_logic;
                
                read_data: in std_logic;
                write_data: in std_logic;
                address: in integer range 0 to 3;
                data_ready: out std_logic;
                data : inout std_logic_vector(0 to 511);
                
                go: in std_logic;
                len: in std_logic_vector(0 to 63);
                ready : out std_logic;
                hash : out std_logic_vector(0 to 31)
                );
                
    end component;

    signal clk, reset : std_logic;
    signal clk_period : time := 25 ns;
    signal go, ready : std_logic := '0';
    signal len: std_logic_vector(0 to 63);
    signal hash : std_logic_vector(0 to 31);
    
    signal read_data, write_data, data_ready : std_logic;
    signal address: integer range 0 to 3;
    signal data : std_logic_vector(0 to 511);
    
    signal temp : integer := 0;
begin
    uut0: wrapper port map ( 
                    reset,
                    clk,
                    
                    read_data,
                    write_data,
                    address,
                    data_ready,
                    data,
                    
                    go,
                    len,
                    ready,
                    hash
        );
    -- 'A' as the input : 'A' to hex 41
    data <= x"41000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000";
    reset <= '0',
             '1' after 1 ns,
             '0' after 55 ns; 
           
    len <= x"00000000_00000008"; --8 bit len
    
    read_data <= '0';
    
     clk_process :process
       begin
           clk <= '0';
           wait for clk_period/2;
           clk <= '1';
           wait for clk_period/2;
       end process;
    
    go <= '1' after 85 ns,
            '0' after 180 ns;
    
    process(clk)
    begin
        write_data <= '1';
        address <= 0;
    end process;

end Behavioral;
