`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/01/09 07:06:13
// Design Name: 
// Module Name: single_x8_output_port
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


module single_x8_output_port
#(
    parameter NUM_DATA = 8,
    parameter DEST_VAL = 0,
    parameter CHANNEL_LENGTH = 12
)
(
    input clk,
    input reset,
    input wr_en,
    input [NUM_DATA-1:0] data_in,
    output [NUM_DATA << 8:0] data_out
    );

reg[NUM_DATA-1:0] data_buffer;

assign data_out[NUM_DATA-1:0] = data_buffer[NUM_DATA-1:0];

always @(posedge clk) begin
    if( reset == 1'b1 ) begin
        data_buffer <= 0;
    end
    
    else begin
        if( wr_en == 1'b1 ) begin
            data_buffer[NUM_DATA-1:0] <= data_in[NUM_DATA-1:0];
        end
    end
end



endmodule
