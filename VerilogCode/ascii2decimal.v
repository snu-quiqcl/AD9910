`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2017/12/12 11:05:07
// Design Name: 
// Module Name: ascii2decimal
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module ascii2decimal(
    input [7:0] ascii_input,
    output [3:0] decimal_output,
    output decimal_error
    );
    
    assign decimal_output = ascii_input - "0";

    assign decimal_error = (ascii_input < "0") | (ascii_input > "9");
    
endmodule
