library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;


entity ram is
 Port (
		reset: in std_logic;
		read_data: in std_logic;
		write_data: in std_logic;
		clk: in std_logic;
		address: in integer range 0 to 3;
		data_ready: out std_logic;
		data_in : in unsigned(0 to 511);
		data_out : out unsigned(0 to 511)
		);
		
end ram;

architecture Behavioral of ram is

signal c0, c1, c2, c3: unsigned(0 to 511);
signal data_out_reg : unsigned(0 to 511);
begin
	data_out <= data_out_reg;
	process(clk, write_data, read_data, reset, address, data_in)	
	begin
		if(rising_edge(clk))then
			if(write_data = '1')then
				if(reset = '1')then
					c0 <= (others => '0');
					c1 <= (others => '0');
					c2 <= (others => '0');
					c3 <= (others => '0');
				else
					case address is
						when 0 =>
							c0 <= data_in;
						when 1 =>
							c1 <= data_in;
						when 2 =>
							c2 <= data_in;
						when 3 =>
							c3 <= data_in;
						when others =>
							null;
					end case;
				end if;
				data_ready <= '1';
			elsif(read_data = '1')then
				case address is
					when 0 =>
						data_out_reg <= c0;
						c0 <= (others => '0');
					when 1 =>
						data_out_reg <= c1;
						c1 <= (others => '0');
					when 2 =>
						data_out_reg <= c2;
						c2 <= (others => '0');
					when 3 =>
						data_out_reg <= c3;
						c3 <= (others => '0');
					when others =>
						data_out_reg <= data_out_reg;
				end case;
				data_ready <= '1';
			else
				data_ready <= '0';
			end if;
		end if;
	end process;


end Behavioral;