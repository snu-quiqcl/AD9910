`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/19 14:50:13
// Design Name: 
// Module Name: rto_core_prime
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


module rto_core_prime(
    input wire CLK100MHZ,
    input wire auto_start,
    input wire reset,
    input wire write,
    input wire [63:0] counter,
    input wire cs,
    input wire read,
    input wire [4:0] addr,
    input wire clk,
    input wire [15:0] dest,
    output wire counter_matched,
    output wire [111:0] rto_out,
    output wire [111:0] timestamp_error_data,
    output wire [111:0] overflow_error_data,
    output wire timestamp_error,
    output wire overflow_error,
    output wire [31:0] rd_data,
    output wire full,
    output wire empty
    );

reg counter_match;
reg [111:0] fifo_output;
reg [63:0] time_reg;

wire flush;
wire wr_en;

endmodule
