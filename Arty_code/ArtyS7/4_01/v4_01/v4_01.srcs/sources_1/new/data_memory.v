`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2018/01/12 20:50:38
// Design Name: 
// Module Name: data_memory
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
//  I should consider if I really want to reset data memory at once as was pointed out at
//  https://electronics.stackexchange.com/questions/209224/how-to-reset-a-memory-array-in-verilog
//////////////////////////////////////////////////////////////////////////////////



module data_memory
    #(parameter DATA_MEMORY_DATA_WIDTH = 16,
      parameter DATA_MEMORY_ADDR_WIDTH = 10
    )
    (
    input clk,
    input we,
    input [DATA_MEMORY_ADDR_WIDTH -1:0] addr,
    input [DATA_MEMORY_DATA_WIDTH -1:0] d_in,
    output [DATA_MEMORY_DATA_WIDTH -1:0] d_out
    );
    reg [DATA_MEMORY_DATA_WIDTH -1:0] memory[(1<<DATA_MEMORY_ADDR_WIDTH)-1:0];
    
    integer j;
    
    always@(posedge clk)
        if (we) memory[addr] <= d_in;

    assign d_out = memory[addr];
    
endmodule
