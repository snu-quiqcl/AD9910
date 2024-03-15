`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/20 10:52:18
// Design Name: 
// Module Name: timestamp_counter
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


module timestamp_counter(
    input wire clk,
    input wire reset,
    input wire start,
    input wire [63:0] counter_offset,
    input wire offset_en,
    output wire [63:0] counter
    );
reg [63:0] counter_reg;

assign counter = counter_reg;

always @(posedge clk) begin
    if( reset ) begin
        counter_reg[63:0] <= 64'h0;
    end
    
    else if(offset_en) begin
        counter_reg[63:0] <= counter_offset[63:0];
    end
    
    else if(start) begin
        counter_reg[63:0] <= counter_reg[63:0] + 64'h1;
    end
end
endmodule
