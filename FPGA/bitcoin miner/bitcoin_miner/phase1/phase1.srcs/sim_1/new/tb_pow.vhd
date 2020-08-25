----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/06/2018 09:50:16 PM
-- Design Name: 
-- Module Name: tb_pow - Behavioral
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

entity tb_pow is
--  Port ( );
end tb_pow;

architecture Behavioral of tb_pow is
    component design_1_wrapper is
  port (
    reset : in STD_LOGIC;
    sys_diff_clock_clk_n : in STD_LOGIC;
    sys_diff_clock_clk_p : in STD_LOGIC
    );
    end component;
    
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
