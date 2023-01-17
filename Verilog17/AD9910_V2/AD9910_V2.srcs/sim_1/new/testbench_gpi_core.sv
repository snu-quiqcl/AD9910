`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/20 13:34:04
// Design Name: 
// Module Name: testbench_gpi_core
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


module testbench_gpi_core;

logic clk;
logic reset;
logic [31:0] gpi_in;
logic write;
logic [63:0] counter;
wire data_ready;
wire [127:0] gpi_out;

gpi_core_prime 
#(
    .DEST_VAL(16'h5),
    .CHANNEL_LENGTH(12)
)
gpi_core_prime_0
(
    .clk(clk),
    .reset(reset),
    .gpi_in(gpi_in),
    .write(write),
    .counter(counter),
    .data_ready(data_ready),
    .gpi_out(gpi_out)
    );

always begin
    #5
    clk = ~clk;
end
 
initial begin
    clk = 1'b0;
    reset = 1'b0;
    gpi_in[31:0] = 32'h0;
    write = 1'b0;
    counter[63:0] = 64'h0;
    
    #10;
    gpi_in[31:0] = 32'h1234;
    write = 1'b1;
    counter[63:0] = 64'h5;
    
    #10;
    gpi_in[31:0] = 32'h1234;
    write = 1'b0;
    counter[63:0] = 64'h6;
    
    #10;
    gpi_in[31:0] = 32'h5678;
    write = 1'b1;
    counter[63:0] = 64'h7;
    
    #10;
    gpi_in[31:0] = 32'h9999;
    write = 1'b0;
    counter[63:0] = 64'h8;
    
    #10;
    gpi_in[31:0] = 32'h1357;
    write = 1'b1;
    counter[63:0] = 64'h9;
    
    #10;
    gpi_in[31:0] = 32'h2468;
    write = 1'b1;
    counter[63:0] = 64'ha;
    
    #10;
    gpi_in[31:0] = 32'h1369;
    write = 1'b1;
    counter[63:0] = 64'hb;
    
    #10;
    gpi_in[31:0] = 32'h1111;
    write = 1'b0;
    counter[63:0] = 64'hc;
    
    #10
    reset = 1'b1;
    
    #10
    reset = 1'b0;
    #10;
    gpi_in[31:0] = 32'h1234;
    write = 1'b1;
    counter[63:0] = 64'h5;
    
    #10;
    gpi_in[31:0] = 32'h1234;
    write = 1'b0;
    counter[63:0] = 64'h6;
    
    #10;
    gpi_in[31:0] = 32'h5678;
    write = 1'b1;
    counter[63:0] = 64'h7;
    
    #10;
    gpi_in[31:0] = 32'h9999;
    write = 1'b0;
    counter[63:0] = 64'h8;
    
    #10;
    gpi_in[31:0] = 32'h1357;
    write = 1'b1;
    counter[63:0] = 64'h9;
    
    #10;
    gpi_in[31:0] = 32'h2468;
    write = 1'b1;
    counter[63:0] = 64'ha;
    
    #10;
    gpi_in[31:0] = 32'h1369;
    write = 1'b1;
    counter[63:0] = 64'hb;
    
    #10;
    gpi_in[31:0] = 32'h1111;
    write = 1'b0;
    counter[63:0] = 64'hc;
end

endmodule
