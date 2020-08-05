// Copyright 1986-2017 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2017.3 (win64) Build 2018833 Wed Oct  4 19:58:22 MDT 2017
// Date        : Wed Jan 31 21:21:55 2018
// Host        : IonTrap7 running 64-bit Service Pack 1  (build 7601)
// Command     : write_verilog -force -mode funcsim
//               o:/Users/thkim/Arty_S7/Sequencer/v3_05/v3_05.srcs/sources_1/ip/c_counter_binary_16bits/c_counter_binary_16bits_sim_netlist.v
// Design      : c_counter_binary_16bits
// Purpose     : This verilog netlist is a functional simulation representation of the design and should not be modified
//               or synthesized. This netlist cannot be used for SDF annotated simulation.
// Device      : xc7s50csga324-1
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

(* CHECK_LICENSE_TYPE = "c_counter_binary_16bits,c_counter_binary_v12_0_11,{}" *) (* downgradeipidentifiedwarnings = "yes" *) (* x_core_info = "c_counter_binary_v12_0_11,Vivado 2017.3" *) 
(* NotValidForBitStream *)
module c_counter_binary_16bits
   (CLK,
    CE,
    SCLR,
    Q);
  (* x_interface_info = "xilinx.com:signal:clock:1.0 clk_intf CLK" *) (* x_interface_parameter = "XIL_INTERFACENAME clk_intf, ASSOCIATED_BUSIF q_intf:thresh0_intf:l_intf:load_intf:up_intf:sinit_intf:sset_intf, ASSOCIATED_RESET SCLR, ASSOCIATED_CLKEN CE, FREQ_HZ 10000000, PHASE 0.000" *) input CLK;
  (* x_interface_info = "xilinx.com:signal:clockenable:1.0 ce_intf CE" *) (* x_interface_parameter = "XIL_INTERFACENAME ce_intf, POLARITY ACTIVE_LOW" *) input CE;
  (* x_interface_info = "xilinx.com:signal:reset:1.0 sclr_intf RST" *) (* x_interface_parameter = "XIL_INTERFACENAME sclr_intf, POLARITY ACTIVE_HIGH" *) input SCLR;
  (* x_interface_info = "xilinx.com:signal:data:1.0 q_intf DATA" *) (* x_interface_parameter = "XIL_INTERFACENAME q_intf, LAYERED_METADATA undef" *) output [15:0]Q;

  wire CE;
  wire CLK;
  wire [15:0]Q;
  wire SCLR;
  wire NLW_U0_THRESH0_UNCONNECTED;

  (* C_AINIT_VAL = "0" *) 
  (* C_CE_OVERRIDES_SYNC = "0" *) 
  (* C_COUNT_BY = "1" *) 
  (* C_COUNT_MODE = "0" *) 
  (* C_COUNT_TO = "1" *) 
  (* C_FB_LATENCY = "0" *) 
  (* C_HAS_CE = "1" *) 
  (* C_HAS_LOAD = "0" *) 
  (* C_HAS_SCLR = "1" *) 
  (* C_HAS_SINIT = "0" *) 
  (* C_HAS_SSET = "0" *) 
  (* C_HAS_THRESH0 = "0" *) 
  (* C_IMPLEMENTATION = "1" *) 
  (* C_LATENCY = "1" *) 
  (* C_LOAD_LOW = "0" *) 
  (* C_RESTRICT_COUNT = "0" *) 
  (* C_SCLR_OVERRIDES_SSET = "1" *) 
  (* C_SINIT_VAL = "0" *) 
  (* C_THRESH0_VALUE = "1" *) 
  (* C_VERBOSITY = "0" *) 
  (* C_WIDTH = "16" *) 
  (* C_XDEVICEFAMILY = "spartan7" *) 
  (* downgradeipidentifiedwarnings = "yes" *) 
  c_counter_binary_16bits_c_counter_binary_v12_0_11 U0
       (.CE(CE),
        .CLK(CLK),
        .L({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}),
        .LOAD(1'b0),
        .Q(Q),
        .SCLR(SCLR),
        .SINIT(1'b0),
        .SSET(1'b0),
        .THRESH0(NLW_U0_THRESH0_UNCONNECTED),
        .UP(1'b1));
endmodule

(* C_AINIT_VAL = "0" *) (* C_CE_OVERRIDES_SYNC = "0" *) (* C_COUNT_BY = "1" *) 
(* C_COUNT_MODE = "0" *) (* C_COUNT_TO = "1" *) (* C_FB_LATENCY = "0" *) 
(* C_HAS_CE = "1" *) (* C_HAS_LOAD = "0" *) (* C_HAS_SCLR = "1" *) 
(* C_HAS_SINIT = "0" *) (* C_HAS_SSET = "0" *) (* C_HAS_THRESH0 = "0" *) 
(* C_IMPLEMENTATION = "1" *) (* C_LATENCY = "1" *) (* C_LOAD_LOW = "0" *) 
(* C_RESTRICT_COUNT = "0" *) (* C_SCLR_OVERRIDES_SSET = "1" *) (* C_SINIT_VAL = "0" *) 
(* C_THRESH0_VALUE = "1" *) (* C_VERBOSITY = "0" *) (* C_WIDTH = "16" *) 
(* C_XDEVICEFAMILY = "spartan7" *) (* ORIG_REF_NAME = "c_counter_binary_v12_0_11" *) (* downgradeipidentifiedwarnings = "yes" *) 
module c_counter_binary_16bits_c_counter_binary_v12_0_11
   (CLK,
    CE,
    SCLR,
    SSET,
    SINIT,
    UP,
    LOAD,
    L,
    THRESH0,
    Q);
  input CLK;
  input CE;
  input SCLR;
  input SSET;
  input SINIT;
  input UP;
  input LOAD;
  input [15:0]L;
  output THRESH0;
  output [15:0]Q;

  wire \<const1> ;
  wire CE;
  wire CLK;
  wire [15:0]L;
  wire [15:0]Q;
  wire SCLR;
  wire NLW_i_synth_THRESH0_UNCONNECTED;

  assign THRESH0 = \<const1> ;
  VCC VCC
       (.P(\<const1> ));
  (* C_AINIT_VAL = "0" *) 
  (* C_CE_OVERRIDES_SYNC = "0" *) 
  (* C_COUNT_BY = "1" *) 
  (* C_COUNT_MODE = "0" *) 
  (* C_COUNT_TO = "1" *) 
  (* C_FB_LATENCY = "0" *) 
  (* C_HAS_CE = "1" *) 
  (* C_HAS_LOAD = "0" *) 
  (* C_HAS_SCLR = "1" *) 
  (* C_HAS_SINIT = "0" *) 
  (* C_HAS_SSET = "0" *) 
  (* C_HAS_THRESH0 = "0" *) 
  (* C_IMPLEMENTATION = "1" *) 
  (* C_LATENCY = "1" *) 
  (* C_LOAD_LOW = "0" *) 
  (* C_RESTRICT_COUNT = "0" *) 
  (* C_SCLR_OVERRIDES_SSET = "1" *) 
  (* C_SINIT_VAL = "0" *) 
  (* C_THRESH0_VALUE = "1" *) 
  (* C_VERBOSITY = "0" *) 
  (* C_WIDTH = "16" *) 
  (* C_XDEVICEFAMILY = "spartan7" *) 
  (* downgradeipidentifiedwarnings = "yes" *) 
  c_counter_binary_16bits_c_counter_binary_v12_0_11_viv i_synth
       (.CE(CE),
        .CLK(CLK),
        .L(L),
        .LOAD(1'b0),
        .Q(Q),
        .SCLR(SCLR),
        .SINIT(1'b0),
        .SSET(1'b0),
        .THRESH0(NLW_i_synth_THRESH0_UNCONNECTED),
        .UP(1'b0));
endmodule
`pragma protect begin_protected
`pragma protect version = 1
`pragma protect encrypt_agent = "XILINX"
`pragma protect encrypt_agent_info = "Xilinx Encryption Tool 2015"
`pragma protect key_keyowner="Cadence Design Systems.", key_keyname="cds_rsa_key", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=64)
`pragma protect key_block
p6lN73FZHRau4FVVDbU55VK5npWJ9A3l3NnyrVKkp9gRUsvTJrVEIDI5AGhcPVlJzqQ34dzBXFpx
wIKyyIg0CA==

`pragma protect key_keyowner="Synopsys", key_keyname="SNPS-VCS-RSA-1", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=128)
`pragma protect key_block
BUKmtqqTtx9zidF71+/yHZa3ECwGppp9LeuaKuDMoK0VR5mQDNuJXaVCAmN2w5n9dAmLlXyX0lnB
hGoIKUT+y3SSIqvIPqPCheTSMXYuiQ19pYW6TbzPDdVB9JnB7vh3NgLqyqa+g/2YAf06PNnoXS+V
SwfzHZBhLxfWRBtCdFU=

`pragma protect key_keyowner="Aldec", key_keyname="ALDEC15_001", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
SSR2s55Tzd6Ho1rxZyvcnfJWSZuItqujVg/Ap2/ljHzo96dSiyhBh4UV4vFcpNzNc5yyBasGN0vb
CTMWg9gZhRSLJKhzBqo8+AQK3ftX/GH/kig/b9fqHrdmgz56CgjHbWbeL8yd2jtGuYkGkG0sf/NJ
ocQeOhQ0dbCv2FZVWE5wpsf7Xfas4/w4OjjEHf6Sx0Qye7Xu7srwYt3P4syyEBgHrTZhvWu4xpzD
iw9rktc3Ddx/0EK+yRrBL/p8rvxhN1Gx0OiostZ7VgRmDDI0vKKe9R4/+Isb1n/6K/CbusvTmqTK
Y/j9hU9LY2BjUPOaOceuHCWmoB4IzmBVEPTe8g==

`pragma protect key_keyowner="ATRENTA", key_keyname="ATR-SG-2015-RSA-3", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
Dwr8cPVfC/g5WUXU4QzkdTEeqGTXbRTHeTnZoCKUYhjDK9Wo//OEMFWAJg3GC2TdRHkEhi/ki2aN
0qSC7QDtNsjiorEz2eaGXgQ8myCJmQyBbyOTfu+03Tw45JKEOnRgoWxf0i3tejlLUotFCV2Euevx
dSLwnlTZa8O1F/M1ohbVQoru8rcL6yaeVaCqi26DLchfdNHq+l/t8ixM4LM3lh/EQL2BmVn1McUj
lhPRjpselY/vwqksQLmsOEisQhbUqHmgfwZBayfgCqjfr713CUYxddyw/mnkIBpVjLo8VulHo7qJ
heHvn/Md89VjZLFqMXrinpzpV7br+gK3y4OZ7w==

`pragma protect key_keyowner="Xilinx", key_keyname="xilinxt_2017_05", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
lSj/MUZnadw1FeV6pQZgdWfaxYF0z9o09aAfY2RylqrTpJqY8wkncEsBeGqZE/vm8LFNBGTSwfhU
0jYASl6hml5cM0Kpe1wrbk8+wQYujTHAD642ml+hd/JI4CHeh+FIPf4uNeC5vvFjJgPtdrTtDgwl
5YTAlzM/n1RXVy7RMQouyRMB5RX91LA0+lr8zmlbASYR1Ecy/ZJ23G/Eq4aRf2Y1DX8IQCDhlA+3
NaDD2VbpWOJIuINpchvE71tnTS6PJXarg9GU6x2h5rxlpEaj3NDbAdOD4UMrDoPqHcFrKomHuD8Q
desEV2nbSKrXsjdkuKv2Z0ouaQAMQDJI3jGbmA==

`pragma protect key_keyowner="Mentor Graphics Corporation", key_keyname="MGC-VELOCE-RSA", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=128)
`pragma protect key_block
QLO8hCFNjwhTo3rtqaIQleebuiC8uv0t3YLeZPi2uK7/uFhPZfkk20Thvro6ouGpnUX/8E7gJZyd
DRaOxn3D1RSVxHpsHsKd6TvYEO+p6tZaJDlz3fc5+V/n0rWpRijLz8PFNVRH3BXu//E7zjiKnx1r
2bxonfHXZHGubFSHaNI=

`pragma protect key_keyowner="Mentor Graphics Corporation", key_keyname="MGC-VERIF-SIM-RSA-2", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
Ek7Lw8Qu6t8JykD1bpIfi9ibtmB5t6JrBSB030QOhViYDSlHMdQRPQEBNTQuot4Xm031OMpNmE/v
QgFZjYr2w1oFbcxibTmhWDLn6emdxlUjVO6b6XBHNhYTdl1h87GKBl0Y/kBHFRmJ7kevrwOYfxPP
SCNk95kUZlJChW7YSeQ4btgyJdbt7FdLQKuPqsU2hXZXD7/C+/30E4AadDqceDpjbt5vwudKDICe
PPXRLJhWW+TtUA7K+L9Smf0wvjPVoQBzfFH81ytsO2oHW53pfZ+t8NUbPVMYrCV5HYDoVtSbwjwy
ff0y302nEfx25mesbrTEG1rjsqMBKaQ+Dy2oWA==

`pragma protect key_keyowner="Mentor Graphics Corporation", key_keyname="MGC-PREC-RSA", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
D2vfNDDNCLYPkrbPgXn9QK5yF8/maxFsuSQn5AjDmvmcqed/3PcmXR6PaAyH8tv6AnOa6yUAOdIe
IAJNnHHM83XPBl505Z+EtlKCJfHbh5ZOuNs0c0xhqLclf96EFb6Sb8bM+3Qro6SiaJ5U82zgVF5d
eJk4Qk7SVAQG1i9F/H2NTaekrK8D7+7e22i9j1CEXAjO3Nd0egPHSrciSHZjvXfvk9Gs5T73y2m6
086gtAyG6Mu29LAOLZyrb2koNyugVq1P5PmoPn4NExZBT3y/19KwqP8CxyjBQ8f7kdD9FWdrkAh0
ZHVf9Z0WBckUocDSnmXxhK+PyO8ePioeLJrkAQ==

`pragma protect key_keyowner="Synplicity", key_keyname="SYNP15_1", key_method="rsa"
`pragma protect encoding = (enctype="BASE64", line_length=76, bytes=256)
`pragma protect key_block
mg6KFpkTiaiviIMgmNpDlt2gY9A6y+ekIXkSGLey5O27x42IhJ5yaEf9v3CikIi5JGstO+vWONCO
Fma0f5o4jwh0LbsaIDSkFClPns1CH9wEehHlx6wVpiBuq+kSblarrYwpGK+XjQsezNf9njnrdlXO
0Y3Yrj0y/v98BvOtlQP9TqKGvkxZkItiiaJxUj7aPv/oI8yxERlbb7pdOD6EBTGvo1idT/YXN5OA
TUU9rpkwlYBapQbbW8wtZsCVyEs2VokAsi3DQ7JUCXpwGn/WY2CkXt/vnVI9KcPp4G7a07JO9wBY
w7IyLkU52Ze2JXZoR+o9PQ7B7iVo3AV2LSH/Lg==

`pragma protect data_method = "AES128-CBC"
`pragma protect encoding = (enctype = "BASE64", line_length = 76, bytes = 11632)
`pragma protect data_block
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
3mve7g==
`pragma protect end_protected
`ifndef GLBL
`define GLBL
`timescale  1 ps / 1 ps

module glbl ();

    parameter ROC_WIDTH = 100000;
    parameter TOC_WIDTH = 0;

//--------   STARTUP Globals --------------
    wire GSR;
    wire GTS;
    wire GWE;
    wire PRLD;
    tri1 p_up_tmp;
    tri (weak1, strong0) PLL_LOCKG = p_up_tmp;

    wire PROGB_GLBL;
    wire CCLKO_GLBL;
    wire FCSBO_GLBL;
    wire [3:0] DO_GLBL;
    wire [3:0] DI_GLBL;
   
    reg GSR_int;
    reg GTS_int;
    reg PRLD_int;

//--------   JTAG Globals --------------
    wire JTAG_TDO_GLBL;
    wire JTAG_TCK_GLBL;
    wire JTAG_TDI_GLBL;
    wire JTAG_TMS_GLBL;
    wire JTAG_TRST_GLBL;

    reg JTAG_CAPTURE_GLBL;
    reg JTAG_RESET_GLBL;
    reg JTAG_SHIFT_GLBL;
    reg JTAG_UPDATE_GLBL;
    reg JTAG_RUNTEST_GLBL;

    reg JTAG_SEL1_GLBL = 0;
    reg JTAG_SEL2_GLBL = 0 ;
    reg JTAG_SEL3_GLBL = 0;
    reg JTAG_SEL4_GLBL = 0;

    reg JTAG_USER_TDO1_GLBL = 1'bz;
    reg JTAG_USER_TDO2_GLBL = 1'bz;
    reg JTAG_USER_TDO3_GLBL = 1'bz;
    reg JTAG_USER_TDO4_GLBL = 1'bz;

    assign (strong1, weak0) GSR = GSR_int;
    assign (strong1, weak0) GTS = GTS_int;
    assign (weak1, weak0) PRLD = PRLD_int;

    initial begin
	GSR_int = 1'b1;
	PRLD_int = 1'b1;
	#(ROC_WIDTH)
	GSR_int = 1'b0;
	PRLD_int = 1'b0;
    end

    initial begin
	GTS_int = 1'b1;
	#(TOC_WIDTH)
	GTS_int = 1'b0;
    end

endmodule
`endif
