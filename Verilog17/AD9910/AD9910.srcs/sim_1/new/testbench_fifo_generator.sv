`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/19 15:18:51
// Design Name: 
// Module Name: testbench_fifo_generator
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


module testbench_fifo_generator;

logic CLK100MHZ;
reg reset_FIFO;
reg [31:0] FIFO_din;
reg FIFO_wr_en;
reg FIFO_rd_en;

wire [31:0] FIFO_dout;
wire FIFO_full;
wire FIFO_overflow;
wire FIFO_empty;
wire FIFO_underflow;

fifo_generator_1 temp_FIFO(
    .clk(CLK100MHZ),
    .rst(reset_FIFO),
    .din(FIFO_din),
    .wr_en(FIFO_wr_en),
    .rd_en(FIFO_rd_en),
    .dout(FIFO_dout),
    .full(FIFO_full),
    .overflow(FIFO_overflow),
    .empty(FIFO_empty),
    .underflow(FIFO_underflow)
);

always begin
    #5
    CLK100MHZ = ~CLK100MHZ;
end

initial begin
    CLK100MHZ = 0;
    reset_FIFO = 1'b1;
    FIFO_din = 32'h0;
    FIFO_rd_en = 1'b0;
    FIFO_wr_en = 1'b0;
    
    #10
    reset_FIFO = 1'b0;
    
    #10
    FIFO_din = 32'h1;
    
    #10
    FIFO_wr_en = 1'b1;
    
    #10
    FIFO_wr_en = 1'b0;
    
end

endmodule
