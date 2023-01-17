`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/20 12:06:10
// Design Name: 
// Module Name: testbench_rto_core_prime
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


module testbench_rto_core_prime;

logic clk;
logic auto_start;
logic reset;
logic flush;
logic write;
logic [127:0] fifo_din;
wire [63:0] counter;
wire counter_matched;
wire [127:0] rto_out;
wire [127:0] timestamp_error_data;
wire [127:0] overflow_error_data;
wire timestamp_error;
wire overflow_error;
wire full;
wire empty;

logic start;
logic [63:0] counter_offset;
logic offset_en;

rto_core_prime rto_core_prime_0(
    .clk(clk),
    .auto_start(auto_start),
    .reset(reset),
    .flush(flush),
    .write(write),
    .fifo_din(fifo_din),
    .counter(counter),
    .counter_matched(counter_matched),
    .rto_out(rto_out),
    .timestamp_error_data(timestamp_error_data),
    .overflow_error_data(overflow_error_data),
    .timestamp_error(timestamp_error),
    .overflow_error(overflow_error),
    .full(full),
    .empty(empty)
    );
    
timestamp_counter timestamp_counter_0(
    .clk(clk),
    .reset(reset),
    .start(start),
    .counter_offset(counter_offset),
    .offset_en(offset_en),
    .counter(counter)
    );
    
always begin
    #5
    clk = ~clk;
end

integer i;
initial begin

    clk = 1'b0;
    auto_start = 1'b0;
    reset = 1'b0;
    flush = 1'b0;
    write = 1'b0;
    fifo_din[127:0] = 128'h0;
    start = 1'b0;
    counter_offset[63:0] = 64'h0;
    offset_en = 1'b0;
    
    #10;
    reset = 1'b1;
    
    #10;
    reset = 1'b0;
    
    #100;
    fifo_din[127:0] <= 128'h9999 | 128'h0 << 32 | 128'h5 << 96;
    write = 1'b1;
    
    #10;
    write = 1'b0;
    
    #10;
    fifo_din[127:0] <= 128'h0002 | 128'h4 << 32 | 128'h5 << 96;
    write = 1'b1;
    
    #10;
    write = 1'b0;
    
    #10;
    fifo_din[127:0] <= 128'h0002 | 128'h10 << 32 | 128'h5 << 96;
    write = 1'b1;
    
    #10;
    write = 1'b0;
    
    #10;
    fifo_din[127:0] <= 128'h0002 | 128'h8 << 32 | 128'h5 << 96;
    write = 1'b1;
    
    #10;
    write = 1'b0;
    
    #10;
    fifo_din[127:0] <= 128'h0002 | 128'h11 << 32 | 128'h5 << 96;
    write = 1'b1;
    
    #10;
    write = 1'b0;
    
    #10;
    auto_start = 1'b1;
    start = 1'b1;
    
    #200
    auto_start = 1'b0;
    start = 1'b0;
    
    #10
    flush = 1'b1;
    counter_offset[63:0] = 64'h5;
    offset_en = 1'b1;
    
    #10
    flush = 1'b0;
    counter_offset[63:0] = 64'h0;
    offset_en = 1'b0;
    
    #100;
    
    for(i = 0; i <512; i++ ) begin
        #10;
        fifo_din[127:0] <= i*10 | (i+5) << 32 | 128'h5 << 96;
        write = 1'b1;
        #10;
        write = 1'b0;
    end
    
    #30
    
    #100;
    fifo_din[127:0] <= 128'h1234 | 128'h3 << 32 | 128'h5 << 96;
    write = 1'b1;
    
    #10;
    write = 1'b0;
    
    #10;
    fifo_din[127:0] <= 128'h5678 | 128'h4 << 32 | 128'h5 << 96;
    write = 1'b1;
    
    #10;
    write = 1'b0;
    
    #10;
    fifo_din[127:0] <= 128'h1111 | 128'h5 << 32 | 128'h5 << 96;
    write = 1'b1;
    
    #10;
    write = 1'b0;
    
    #10;
    auto_start = 1'b1;
    start = 1'b1;
    
    #400;
    auto_start = 1'b1;
    start = 1'b0;
    
    #30
    auto_start = 1'b0;
    start = 1'b1;
    
    #30
    auto_start = 1'b1;
    start = 1'b1;
    
    #100
    auto_start = 1'b0;
    start = 1'b0;
    reset = 1'b1;
    
    #10
    reset = 1'b0;
end

endmodule
