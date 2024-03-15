`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/20 13:25:56
// Design Name: 
// Module Name: gpi_core_prime
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


module gpi_core_prime
#(
    parameter DEST_VAL = 16'h0,
    parameter CHANNEL_LENGTH = 12
)
(
    input wire clk,
    input wire reset,
    input wire [31:0] gpi_in,
    input wire write,
    input wire [63:0] counter,
    output wire data_ready,
    output wire [127:0] gpi_out
    );

reg data_ready_state;
reg [127:0] gpi_out_buffer;

assign gpi_out[127:0] = gpi_out_buffer[127:0];
assign data_ready = data_ready_state;

always @(posedge clk) begin
    if( reset ) begin
        data_ready_state <= 1'b0;
        gpi_out_buffer[127:0] <= 128'h0;
    end
    else begin
        if( write == 1'b1 ) begin
            data_ready_state <= 1'b1;
            gpi_out_buffer[127:0] <= {16'h0, DEST_VAL, counter, gpi_in};
        end
        else begin
            data_ready_state <= 1'b0;
        end
    end
end
endmodule
