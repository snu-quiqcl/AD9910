`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    23:38:19 04/23/2014 
// Design Name: 
// Module Name:    hex2ascii 
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
module hex2ascii(
    input [3:0] hex_input,
    output [7:0] ascii_output
    );

	assign ascii_output = ((hex_input < 4'hA) ? "0" : "A"-8'h0A) +{4'h0, hex_input};

endmodule
