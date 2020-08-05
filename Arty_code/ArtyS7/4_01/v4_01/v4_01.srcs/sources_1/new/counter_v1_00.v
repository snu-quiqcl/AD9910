`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    16:53:46 04/24/2014 
// Design Name: 
// Module Name:    counter 
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
module counter
#(parameter counterByte = 2,
parameter width =counterByte*8)
(
    input clock,
    input clockEnable,
    input reset,
    output reg [width-1:0] q
    );

	initial q <= 0;
	wire internalClock;
	assign internalClock = clock & clockEnable;

	always @ (posedge internalClock, posedge reset)
		if (reset) q <= 0;
		else q <= q + 1;

endmodule
