`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/11 17:47:37
// Design Name: 
// Module Name: fifo_sync
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


module fifo_sync
#(
    parameter FIFO_DEPTH = 1024
)
(
    input clk,
    input read,
    input write,
    input[83:0] data_in,
    input reset,
    output empty,
    output full,
    output[83:0] data_out
    );
endmodule
