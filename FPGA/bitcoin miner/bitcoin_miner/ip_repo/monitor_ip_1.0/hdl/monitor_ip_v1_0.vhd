library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity monitor_ip_v1_0 is
	generic (
		-- Users to add parameters here

		-- User parameters ends
		-- Do not modify the parameters beyond this line


		-- Parameters of Axi Slave Bus Interface MON_AXI
		C_MON_AXI_DATA_WIDTH	: integer	:= 32;
		C_MON_AXI_ADDR_WIDTH	: integer	:= 6
	);
	port (
		-- Users to add ports here

		-- User ports ends
		-- Do not modify the ports beyond this line


		-- Ports of Axi Slave Bus Interface MON_AXI
		mon_axi_aclk	: in std_logic;
		mon_axi_aresetn	: in std_logic;
		mon_axi_awaddr	: in std_logic_vector(C_MON_AXI_ADDR_WIDTH-1 downto 0);
		mon_axi_awprot	: in std_logic_vector(2 downto 0);
		mon_axi_awvalid	: in std_logic;
		mon_axi_awready	: out std_logic;
		mon_axi_wdata	: in std_logic_vector(C_MON_AXI_DATA_WIDTH-1 downto 0);
		mon_axi_wstrb	: in std_logic_vector((C_MON_AXI_DATA_WIDTH/8)-1 downto 0);
		mon_axi_wvalid	: in std_logic;
		mon_axi_wready	: out std_logic;
		mon_axi_bresp	: out std_logic_vector(1 downto 0);
		mon_axi_bvalid	: out std_logic;
		mon_axi_bready	: in std_logic;
		mon_axi_araddr	: in std_logic_vector(C_MON_AXI_ADDR_WIDTH-1 downto 0);
		mon_axi_arprot	: in std_logic_vector(2 downto 0);
		mon_axi_arvalid	: in std_logic;
		mon_axi_arready	: out std_logic;
		mon_axi_rdata	: out std_logic_vector(C_MON_AXI_DATA_WIDTH-1 downto 0);
		mon_axi_rresp	: out std_logic_vector(1 downto 0);
		mon_axi_rvalid	: out std_logic;
		mon_axi_rready	: in std_logic
	);
end monitor_ip_v1_0;

architecture arch_imp of monitor_ip_v1_0 is

	-- component declaration
	component monitor_ip_v1_0_MON_AXI is
		generic (
		C_S_AXI_DATA_WIDTH	: integer	:= 32;
		C_S_AXI_ADDR_WIDTH	: integer	:= 6
		);
		port (
		S_AXI_ACLK	: in std_logic;
		S_AXI_ARESETN	: in std_logic;
		S_AXI_AWADDR	: in std_logic_vector(C_S_AXI_ADDR_WIDTH-1 downto 0);
		S_AXI_AWPROT	: in std_logic_vector(2 downto 0);
		S_AXI_AWVALID	: in std_logic;
		S_AXI_AWREADY	: out std_logic;
		S_AXI_WDATA	: in std_logic_vector(C_S_AXI_DATA_WIDTH-1 downto 0);
		S_AXI_WSTRB	: in std_logic_vector((C_S_AXI_DATA_WIDTH/8)-1 downto 0);
		S_AXI_WVALID	: in std_logic;
		S_AXI_WREADY	: out std_logic;
		S_AXI_BRESP	: out std_logic_vector(1 downto 0);
		S_AXI_BVALID	: out std_logic;
		S_AXI_BREADY	: in std_logic;
		S_AXI_ARADDR	: in std_logic_vector(C_S_AXI_ADDR_WIDTH-1 downto 0);
		S_AXI_ARPROT	: in std_logic_vector(2 downto 0);
		S_AXI_ARVALID	: in std_logic;
		S_AXI_ARREADY	: out std_logic;
		S_AXI_RDATA	: out std_logic_vector(C_S_AXI_DATA_WIDTH-1 downto 0);
		S_AXI_RRESP	: out std_logic_vector(1 downto 0);
		S_AXI_RVALID	: out std_logic;
		S_AXI_RREADY	: in std_logic
		);
	end component monitor_ip_v1_0_MON_AXI;

begin

-- Instantiation of Axi Bus Interface MON_AXI
monitor_ip_v1_0_MON_AXI_inst : monitor_ip_v1_0_MON_AXI
	generic map (
		C_S_AXI_DATA_WIDTH	=> C_MON_AXI_DATA_WIDTH,
		C_S_AXI_ADDR_WIDTH	=> C_MON_AXI_ADDR_WIDTH
	)
	port map (
		S_AXI_ACLK	=> mon_axi_aclk,
		S_AXI_ARESETN	=> mon_axi_aresetn,
		S_AXI_AWADDR	=> mon_axi_awaddr,
		S_AXI_AWPROT	=> mon_axi_awprot,
		S_AXI_AWVALID	=> mon_axi_awvalid,
		S_AXI_AWREADY	=> mon_axi_awready,
		S_AXI_WDATA	=> mon_axi_wdata,
		S_AXI_WSTRB	=> mon_axi_wstrb,
		S_AXI_WVALID	=> mon_axi_wvalid,
		S_AXI_WREADY	=> mon_axi_wready,
		S_AXI_BRESP	=> mon_axi_bresp,
		S_AXI_BVALID	=> mon_axi_bvalid,
		S_AXI_BREADY	=> mon_axi_bready,
		S_AXI_ARADDR	=> mon_axi_araddr,
		S_AXI_ARPROT	=> mon_axi_arprot,
		S_AXI_ARVALID	=> mon_axi_arvalid,
		S_AXI_ARREADY	=> mon_axi_arready,
		S_AXI_RDATA	=> mon_axi_rdata,
		S_AXI_RRESP	=> mon_axi_rresp,
		S_AXI_RVALID	=> mon_axi_rvalid,
		S_AXI_RREADY	=> mon_axi_rready
	);

	-- Add user logic here

	-- User logic ends

end arch_imp;
