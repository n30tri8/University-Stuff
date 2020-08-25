----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06/06/2018 05:16:16 PM
-- Design Name: 
-- Module Name: monitor - Behavioral
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

entity monitor is
    Port ( 
		h0 : in STD_LOGIC_VECTOR (0 to 31);
		h1 : in STD_LOGIC_VECTOR (0 to 31);
		h2 : in STD_LOGIC_VECTOR (0 to 31);
		h3 : in STD_LOGIC_VECTOR (0 to 31);
		h4 : in STD_LOGIC_VECTOR (0 to 31);
		h5 : in STD_LOGIC_VECTOR (0 to 31);
		h6 : in STD_LOGIC_VECTOR (0 to 31);
		h7 : in STD_LOGIC_VECTOR (0 to 31);
		nounce : in STD_LOGIC_VECTOR (0 to 31);
		run_time : in STD_LOGIC_VECTOR (0 to 31)
		);
end monitor;

architecture Behavioral of monitor is

begin


end Behavioral;
