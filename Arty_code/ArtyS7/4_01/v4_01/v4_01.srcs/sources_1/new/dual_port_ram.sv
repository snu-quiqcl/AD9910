`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2018/01/12 20:50:38
// Design Name: 
// Module Name: dual_port_ram
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

//`include "parameterPkg.sv"

import parameterPkg::*;

module dual_port_ram
//    #(parameter INSTRUCTION_MEMORY_DATA_WIDTH = 64,
//      parameter INSTRUCTION_MEMORY_ADDR_WIDTH = 9
//    )
    (
    input clk,
    input [INSTRUCTION_MEMORY_ADDR_WIDTH -1:0] addr_a,
    output [INSTRUCTION_MEMORY_DATA_WIDTH -1:0] dout_a,
    input we_a,
    input [INSTRUCTION_MEMORY_DATA_WIDTH -1:0] din_a,
    input [INSTRUCTION_MEMORY_ADDR_WIDTH -1:0] addr_b,
    output [INSTRUCTION_MEMORY_DATA_WIDTH -1:0] dout_b
    );
    reg [INSTRUCTION_MEMORY_DATA_WIDTH -1:0] memory[(1<<INSTRUCTION_MEMORY_ADDR_WIDTH)-1:0];
    always@(posedge clk)
        if (we_a) memory[addr_a] <= din_a;
    assign dout_a = memory[addr_a];
    assign dout_b = memory[addr_b];
    
endmodule
