`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    17:23:20 02/17/2012 
// Design Name: 
// Module Name:    ascii2hex 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module ascii2hex(
    input [7:0] ascii_input,
    output [3:0] hex_output,
	 output error
    );

	wire [3:0] hex_data;
	assign hex_data = ((ascii_input >= "0") & (ascii_input <= "9"))? ascii_input - "0" :
								( 
									(ascii_input >= "A" & ascii_input <= "F") ? ascii_input - "A" + 8'hA :
									( 
										(ascii_input >= "a" & ascii_input <= "f") ? ascii_input - "a" + 8'hA : 4'h0
									)
								);

	assign hex_output = hex_data;
	assign error = (ascii_input < "0") | ((ascii_input > "9") & (ascii_input < "A")) | 
						((ascii_input > "F") & (ascii_input < "a")) | (ascii_input > "f");
endmodule
