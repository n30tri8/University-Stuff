----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07/13/2018 06:02:45 PM
-- Design Name: 
-- Module Name: tb_top_wrapper - Behavioral
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
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity tb_top_wrapper is
--  Port ( );
end tb_top_wrapper;

architecture Behavioral of tb_top_wrapper is
component design_1_wrapper is
  port (
    reset : in STD_LOGIC;
    sys_diff_clock_clk_n : in STD_LOGIC;
    sys_diff_clock_clk_p : in STD_LOGIC
  );
end component design_1_wrapper;

    signal reset : STD_LOGIC := '0';
    signal sys_diff_clock_clk_n : STD_LOGIC := '0';
    signal sys_diff_clock_clk_p : STD_LOGIC := '1';
begin
    sys_diff_clock_clk_n <= not (sys_diff_clock_clk_n) after 10ns;
    sys_diff_clock_clk_p <= not (sys_diff_clock_clk_p) after 10ns;
    
    uut0: design_1_wrapper port map (
        reset,
        sys_diff_clock_clk_n,
        sys_diff_clock_clk_p
        );

end Behavioral;
