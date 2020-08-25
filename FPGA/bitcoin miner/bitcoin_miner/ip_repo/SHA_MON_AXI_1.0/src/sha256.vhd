library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;


entity sha256 is
 Port (
		go: in std_logic;
		clk: in std_logic;
		reset: in std_logic;
		len: in std_logic_vector(0 to 63);
		
		data_in0 : in std_logic_vector(0 to 511);
		data_in1 : in std_logic_vector(0 to 511);
		
		busy : out std_logic;
		ready : out std_logic;
		h0 : out std_logic_vector(0 to 31);
		h1 : out std_logic_vector(0 to 31);
		h2 : out std_logic_vector(0 to 31);
		h3 : out std_logic_vector(0 to 31);
		h4 : out std_logic_vector(0 to 31);
		h5 : out std_logic_vector(0 to 31);
		h6 : out std_logic_vector(0 to 31);
		h7 : out std_logic_vector(0 to 31)
		);
end sha256;

architecture Behavioral of sha256 is
subtype word is unsigned (0 to 31) ; 
type w_array is array  (0 to 63 ) of word ;
type h_array is array ( 0 to 7 ) of word ;
type block512 is array ( 0 to 15 ) of word ;

 
signal W : w_array ;
signal loaded_block : block512 ;
signal H : h_array ;
signal w_loaded : std_logic;
signal do_process : std_logic := '0';
signal h_calc : std_logic := '1';
-------------------
signal AA , BB , CC , DD , EE , FF , GG , HH : word;
signal ready_wi : std_logic_vector ( 0 to 63 );
signal cnt_loop1 : integer range 0  to 64  ;
signal cnt_loop2 : integer range -1 to 64  ;
constant K : w_array :=
				(
				0 => x"428a2f98",
				1 => x"71374491",
				2 => x"b5c0fbcf",
				3 => x"e9b5dba5",
				4 => x"3956c25b",
				5 => x"59f111f1",
				6 => x"923f82a4",
				7 => x"ab1c5ed5",
				8 => x"d807aa98",
				9 => x"12835b01",
				10 => x"243185be",
				11 => x"550c7dc3",
				12 => x"72be5d74",
				13 => x"80deb1fe",
				14 => x"9bdc06a7",
				15 => x"c19bf174",
				16 => x"e49b69c1",
				17 => x"efbe4786",
				18 => x"0fc19dc6",
				19 => x"240ca1cc",
				20 => x"2de92c6f",
				21 => x"4a7484aa",
				22 => x"5cb0a9dc",
				23 => x"76f988da",
				24 => x"983e5152",
				25 => x"a831c66d",
				26 => x"b00327c8",
				27 => x"bf597fc7",
				28 => x"c6e00bf3",
				29 => x"d5a79147",
				30 => x"06ca6351",
				31 => x"14292967",
				32 => x"27b70a85",
				33 => x"2e1b2138",
				34 => x"4d2c6dfc",
				35 => x"53380d13",
				36 => x"650a7354",
				37 => x"766a0abb",
				38 => x"81c2c92e",
				39 => x"92722c85",
				40 => x"a2bfe8a1",
				41 => x"a81a664b",
				42 => x"c24b8b70",
				43 => x"c76c51a3",
				44 => x"d192e819",
				45 => x"d6990624",
				46 => x"f40e3585",
				47 => x"106aa070",
				48 => x"19a4c116",
				49 => x"1e376c08",
				50 => x"2748774c",
				51 => x"34b0bcb5",
				52 => x"391c0cb3",
				53 => x"4ed8aa4a",
				54 => x"5b9cca4f",
				55 => x"682e6ff3",
				56 => x"748f82ee",
				57 => x"78a5636f",
				58 => x"84c87814",
				59 => x"8cc70208",
				60 => x"90befffa",
				61 => x"a4506ceb",
				62 => x"be49a3f7",
				63 => x"c67178f2"
				);
---------------
signal nob : integer range 0 to 3;
signal cur_block, next_block: integer range 0 to 3;
type state is (s0, s1, s2, s2to3, s3);
signal cur_state, next_state: state;
signal next_loaded_block : block512;
signal next_w_loaded: std_logic;

begin
	
	process(len, reset)
	variable nob_var : integer range 0 to 3;
	variable len_var: unsigned(0 to 63);
	begin
		if(reset = '1')then
			nob <= 1;		--there always is at least one block to hash
		else
			len_var := unsigned(len);
			nob_var := 0;
			for I in 0 to 2 loop
				if (len_var > x"0000000000000200") then		-- > 512
					len_var := len_var - x"0000000000000200";
					nob_var := nob_var + 1;
				elsif(len_var > x"00000000000001BF") then	-- 448 <= len_var <= 512 
					len_var := (others => '0');
					nob_var := nob_var + 2;
				elsif(len_var > x"0000000000000000") then	-- 000 <= len_var <= 447 
					len_var := (others => '0');
					nob_var := nob_var + 1;
				else
					len_var := (others => '0');
					nob_var := nob_var;
				end if;
			end loop;
			
			nob <= nob_var;
		end if;
	end process;
	-------------------fsm
	process(clk)
	begin
		if(rising_edge(clk))then
			if(reset = '1')then
				cur_state <= s0;
				cur_block <= 0;
				w_loaded <= '0';
				loaded_block(0 to 15) <= (others => x"00000000");
			else
				cur_state <= next_state;
				cur_block <= next_block;
				loaded_block <= next_loaded_block;
				w_loaded <= next_w_loaded;
			end if;
			
		end if;
	end process;
	
	process(cur_state, cur_block, go, h_calc, data_in0, data_in1, loaded_block, nob, len)
	variable special_index : integer;
	variable data_in_v : unsigned(0 to 511);
	begin
		case cur_state is
			when s0 =>
				if(go = '1')then
					next_state <= s1;
					next_block <= 0;
					next_loaded_block <= loaded_block;
					next_w_loaded <= '0';
				else
					next_state <= s0;
					next_block <= 0;
					next_loaded_block <= loaded_block;
					next_w_loaded <= '0';
				end if;
			when s1 =>
				if(h_calc = '1')then
					next_state <= s2;
					next_block <= cur_block + 1;
					if(cur_block = 0)then
						data_in_v := unsigned(data_in0);
					else
						data_in_v := unsigned(data_in1);
					end if;
					if((cur_block + 1) = nob)then
						special_index := to_integer(unsigned(len(32 to 63)));
						if(special_index > 511)then
						  special_index := special_index - 512;
						else
						  special_index := special_index;
						end if;
						data_in_v(special_index) := '1';
						next_loaded_block <= (	0=> data_in_v(0 to 31),
									1=> data_in_v(32 to 63),
									2=> data_in_v(64 to 95),
									3=> data_in_v(96 to 127),
									4=> data_in_v(128 to 159),
									5=> data_in_v(160 to 191),
									6=> data_in_v(192 to 223),
									7=> data_in_v(224 to 255),
									8=> data_in_v(256 to 287),
									9=> data_in_v(288 to 319),
									10=> data_in_v(320 to 351),
									11=> data_in_v(352 to 383),
									12=> data_in_v(384 to 415),
									13=> data_in_v(416 to 447),
									14=> unsigned(len(0 to 31)),
									15=> unsigned(len(32 to 63))
									);
					else
						next_loaded_block <= (	0=> data_in_v(0 to 31),
									1=> data_in_v(32 to 63),
									2=> data_in_v(64 to 95),
									3=> data_in_v(96 to 127),
									4=> data_in_v(128 to 159),
									5=> data_in_v(160 to 191),
									6=> data_in_v(192 to 223),
									7=> data_in_v(224 to 255),
									8=> data_in_v(256 to 287),
									9=> data_in_v(288 to 319),
									10=> data_in_v(320 to 351),
									11=> data_in_v(352 to 383),
									12=> data_in_v(384 to 415),
									13=> data_in_v(416 to 447),
									14=> data_in_v(448 to 479),
									15=> data_in_v(480 to 511)
									);
					end if;
					next_w_loaded <= '1';
				else
					next_state <= s1;
					next_block <= cur_block;
					next_loaded_block <= loaded_block;
					next_w_loaded <= '0';
				end if;
			when s2 =>
				if(cur_block < nob)then
					next_state <= s1;
					next_block <= cur_block;
					next_loaded_block <= loaded_block;
					next_w_loaded <= '0';
				else
					next_state <= s2to3;
					next_block <= 0;
					next_loaded_block <= loaded_block;
					next_w_loaded <= '0';
				end if;
			when s2to3 =>	
				if(h_calc = '1')then
					next_state <= s3;
					next_block <= 0;
					next_loaded_block <= loaded_block;
					next_w_loaded <= '0';
				else
					next_state <= s2to3;
					next_block <= 0;
					next_loaded_block <= loaded_block;
					next_w_loaded <= '0';
				end if;
			when s3 =>
				if(go = '1')then
					next_state <= s1;
					next_block <= 0;
					next_loaded_block <= loaded_block;
					next_w_loaded <= '0';
				else
					next_state <= s3;
					next_block <= 0;
					next_loaded_block <= loaded_block;
					next_w_loaded <= '0';
				end if;				
			when others =>
				next_state <= s0;
				next_block <= 0;
				next_loaded_block(0 to 15) <= (others => x"00000000");
				next_w_loaded <= '0';
		end case;
	end process;
	
	process(cur_state)
	begin
		case cur_state is
			when s1 | s2 | s2to3 =>
				ready <= '0';
				busy <= '1';
			when s3 =>
				ready <= '1';
				busy <= '0';
			when others =>
				ready <= '0';
				busy <= '0';
		end case;
	end process;
	
	h0 <= std_logic_vector(H(0));
	h1 <= std_logic_vector(H(1));
	h2 <= std_logic_vector(H(2));
	h3 <= std_logic_vector(H(3));
	h4 <= std_logic_vector(H(4));
	h5 <= std_logic_vector(H(5));
	h6 <= std_logic_vector(H(6));
	h7 <= std_logic_vector(H(7));
	
	-----------------------end fsm
	process ( clk , reset, loaded_block, cnt_loop1, do_process)
	variable WT  , t1 , t2  , t3 , t4 : unsigned ( 0 to 31 );
	variable W2  :w_array;
	variable ROT14 , ROT17 , ROT9 , ROT19 : unsigned ( 0 to 31 );
	variable SHF12 , SHF9 : unsigned ( 0 to 31 );
		begin 
		if(clk 'event and clk = '1')then 
			if (reset = '1')then
				cnt_loop1 <= 64;
				do_process <= '0';
				ready_wi <= ( others => '0');
			elsif (do_process = '0' and w_loaded = '1' )then 
				do_process <= '1';
				cnt_loop1 <= 16 ;
 ---------------------------------------------------------------              
				 for I1 in 0 to 15 loop 
					for I2 in 0 to 7 loop
					  W(I1)(I2) <= loaded_block(I1)(31-I2);
					end loop;
					for I3 in 16 to 31 loop                  
					  W(I1)(I3) <= loaded_block(I1)(31-I3);
					end loop; 
					W(I1)(8 to 15 ) <= loaded_block(I1)(16 to 23);
				 end loop;  
				  
				 ready_wi <= ( 0 to 15  => '1'  , others => '0');  --frist 16 Wi are ready for loop2
 --------------------------------------------------------------------              
				 
			
			elsif (cnt_loop1 = 64 ) then
				do_process <= '0';
				ready_wi(0) <= '0';	--to prevent second process from looping without next block loaded
				ready_wi(1 to 63) <= ready_wi(1 to 63);	--to prevent second process from looping without next block loaded
				cnt_loop1 <= 64 ;
			else-- if(ready_wi(63) = '0') then  -- with this condition that the blocks are not finished
				ROT17 := W(cnt_loop1 - 12) ror 17;--
				ROT14 := W(cnt_loop1 - 12) ror 14;--
				ROT19 := W(cnt_loop1 - 1 ) ror 19;--this operations didn't test!!!test them for confident.
				ROT9  := W(cnt_loop1 - 1 ) ror 9 ;
				SHF12 := W(cnt_loop1 - 12) srl 12;
				SHF9  := W(cnt_loop1 - 1 ) srl 9 ;
				t1  := (ROT9 xor ROT19 xor SHF9);
				t2  := W(cnt_loop1 - 6);
				t3  := (SHF12 xor ROT14 xor ROT17);
				t4  :=  W(cnt_loop1 - 15 );
				WT     := t1 + t2 + t3 + t4 ;
				--WT     := (ROT9 xor ROT19 xor SHF9) + W(cnt_loop1 - 6) + (SHF12 xor ROT14 xor ROT17) + W(cnt_loop1 - 15 );
			    
--				for I2 in 0 to 7 loop
--					W(cnt_loop1)(I2)   <= WT(31-I2);
--				end loop;
--				for I3 in 16 to 31 loop
--					W(cnt_loop1)(I3)   <= WT(31-I3);
--				end loop;
--             W(cnt_loop1)(8 to 15 ) <= WT(16 to 23);

                      for I2 in 0 to 7 loop
                            W2(cnt_loop1)(I2)   := WT(31-I2);
                        end loop;
                        for I3 in 16 to 31 loop
                            W2(cnt_loop1)(I3)   := WT(31-I3);
                        end loop;
                        W2(cnt_loop1)(8 to 15 ) := WT(16 to 23);
				        W(cnt_loop1)       <= W2(cnt_loop1);

				ready_wi(0 to (cnt_loop1-1)) <= ready_wi(0 to (cnt_loop1-1));
				ready_wi(cnt_loop1) <= '1' ;
				ready_wi((cnt_loop1+1) to 63) <= ready_wi((cnt_loop1+1) to 63);
				
				do_process <= '1';
				cnt_loop1 <= cnt_loop1 + 1;  
			 
			end if; 
		end if;      
	   end process; 
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	   
	process (clk , reset, ready_wi, cnt_loop2, cur_block, AA , BB , CC , DD , EE , FF , GG , HH , cur_state)
	variable T1 , T2 : word;
	variable ROT2 , ROT13 , ROT2_A ,ROT22 , ROT6 , ROT11 , ROT25 , ROT2_CD, ROT3 , ROT15   :word;
	variable AA_v , BB_v , CC_v , DD_v , EE_v , FF_v , GG_v , HH_v : word;
	variable SHF7 , SHF5 : word;
	variable CD , Ch , Maj , Z0 , Z1 , Z2 : word;
	variable three : word;
	variable mult : unsigned (0 to 63 );	   
	begin
		if(clk'event and clk = '1')then
			if (reset = '1') then 
				cnt_loop2 <= -1;
				h_calc <= '1';
			elsif (cnt_loop2 = -1) then 
				if(cur_state /= s2to3 and cur_state /= s3)then
                      if(cur_block = 0)then
                        AA <= x"6a09e667";
                        BB <= x"bb67ae85";
                        CC <= x"3c6ef372";
                        DD <= x"a54ff53a";
                        EE <= x"510e527f";
                        FF <= x"9b05688c";
                        GG <= x"1f83d9ab";
                        HH <= x"5be0cd19";
                        
                        H(0) <= x"6a09e667";
                        H(1) <= x"bb67ae85";
                        H(2) <= x"3c6ef372";
                        H(3) <= x"a54ff53a";
                        H(4) <= x"510e527f";
                        H(5) <= x"9b05688c";
                        H(6) <= x"1f83d9ab";
                        H(7) <= x"5be0cd19";
                      else
                        AA <= H(0);
                        BB <= H(1);
                        CC <= H(2);
                        DD <= H(3);
                        EE <= H(4);
                        FF <= H(5);
                        GG <= H(6);
                        HH <= H(7);
                      end if;
                      cnt_loop2 <= 0;
                    else
                      H(0) <= H(0);
                      H(1) <= H(1);
                      H(2) <= H(2);
                      H(3) <= H(3);
                      H(4) <= H(4);
                      H(5) <= H(5);
                      H(6) <= H(6);
                      H(7) <= H(7);
                      cnt_loop2 <= -1;
                    end if;
                    h_calc <= '1';
			elsif(w_loaded = '1')then
				h_calc <= '0';
			elsif (cnt_loop2 = 64) then
				cnt_loop2 <= -1;
				h_calc <= '1';
				H(0) <= H(0) + AA;
				H(1) <= H(1) + BB;
				H(2) <= H(2) + CC;
				H(3) <= H(3) + DD;
				H(4) <= H(4) + EE;
				H(5) <= H(5) + FF;
				H(6) <= H(6) + GG;
				H(7) <= H(7) + HH;
			elsif(ready_wi(cnt_loop2) = '1') then 
				h_calc <= '0';

				CD      := CC + DD;
				ROT2_A  := AA ror 2;
				ROT13   := AA ror 13;    
				ROT22   := AA ror 22;
				SHF7    := AA srl 7;
				ROT6    := EE ror 6;
				ROT11   := EE ror 11;
				ROT25   := EE ror 25;
				ROT2_CD := CD ror 2 ;
				ROT3    := CD ror 3 ;
				ROT15   := CD ror 15;
				SHF5    := CD srl 5;
				Ch      := (EE and FF) xor ((not FF) and GG )xor ((not EE) and GG);
				Maj     := (AA and CC) xor (AA and BB) xor (BB and CC);
				Z0      := (ROT2_A xor ROT13) xor (ROT22 xor SHF7);
				Z1      := (ROT6 xor ROT11 xor ROT25);
				Z2      := (ROT2_CD xor ROT3) xor (ROT15 xor SHF5);
				T2      := (HH + Z1) + (Ch + K(cnt_loop2)) + W(cnt_loop2);
				T1      := Z0 + Maj + Z2 ;
				HH_v      := GG;
				FF_v      := EE;
				DD_v      := CC;
				BB_v      := AA;
				GG_v      := FF_v;
				EE_v      := DD_v + T1;
				CC_v      := BB_v;
				three := (30 to 31 => '1' , others => '0');
				mult    := three * T1;
				AA_v      := mult(32 to 63) - T2;

				HH <= HH_v;
				FF <= FF_v;
				DD <= DD_v;
				BB <= BB_v;
				GG <= GG_v;
				EE <= EE_v;
				CC <= CC_v;
				AA <= AA_v;








				cnt_loop2 <= cnt_loop2 + 1;				
			else
				null;
			end if ;
		end if ;
	end process;           
end Behavioral;
