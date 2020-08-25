library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;


entity wrapper is
 Port (
		reset: in std_logic;
		clk: in std_logic;
		
		read_data: in std_logic;
		write_data: in std_logic;
		address: in integer range 0 to 3;
		data_ready: out std_logic;
		data : in std_logic_vector(0 to 511);
		
		go: in std_logic;
		len: in std_logic_vector(0 to 63);
		ready : out std_logic;
		hash : out std_logic_vector(0 to 31)
		);
		
end wrapper;

architecture Behavioral of wrapper is
	component sha256 is
		 Port (
				go: in std_logic;
				clk: in std_logic;
				reset: in std_logic;
				len: in std_logic_vector(0 to 63);
				
				ram_data_in : in std_logic_vector(0 to 511);
				ram_data_ready: in std_logic;
				address: out integer range 0 to 3;
				ram_read_data: out std_logic;
				
				ready : out std_logic;
				hash : out std_logic_vector(0 to 31)
				);
	end component;
	
	component ram is
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
		
	end component;
	
	
	signal ram_address, sha256_ram_address : integer range 0 to 3;
	signal ram_read_data, ram_write_data, sha256_ram_read : std_logic;
	signal ram_data_ready : std_logic;
	signal ram_data_out : unsigned(0 to 511);
	begin
	
	ram_read_data <= 	read_data when go = '0' else
						sha256_ram_read;
	
	ram_write_data <= 	write_data when go = '0' else
						'0';
	
	ram_address <= 		address when go = '0' else
						sha256_ram_address;
	
	
	data_ready	<= ram_data_ready;
	
	ram_comp: ram port map 
						(
						reset,
						ram_read_data,
						ram_write_data,
						clk,
						ram_address,
						ram_data_ready,
						unsigned(data),
						ram_data_out
						);
						
	sha256_comp: sha256 port map
						(
						go,
						clk,
						reset,
						len,
						
						std_logic_vector(ram_data_out),
						ram_data_ready,
						sha256_ram_address,
						sha256_ram_read,
						
						ready,
						hash
						);




end Behavioral;
