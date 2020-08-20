`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/20 16:09:42
// Design Name: 
// Module Name: testbench_ad9910_driver
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


module testbench_ad9910_driver;

logic clk;
logic reset;
logic auto_start;
logic flush_rto_fifo;
logic write_rto_fifo;
logic [127:0] rto_fifo_din;
wire [63:0] counter;
logic flush_rti_fifo;
logic read_rti_fifo;
logic gpo_override_en;
logic gpo_selected_en;
logic [63:0] gpo_override_value;
wire [127:0] rto_timestamp_error_data;
wire [127:0] rto_overflow_error_data;
wire rto_timestamp_error;
wire rto_overflow_error;
wire rto_fifo_full;
wire rto_fifo_empty;
wire [127:0] rti_out;
wire [127:0] rti_overflow_error_data;
wire rti_overflow_error;
wire rti_underflow_error;
wire rti_fifo_full;
wire rti_fifo_empty;
wire busy;
wire [127:0] gpo_error_data;
wire gpo_overrided;
wire gpo_busy_error;
wire gpi_data_ready;
wire [127:0] gpi_out;
wire io;
wire sck;
wire [1:0] cs;
logic io_val;

assign io = (~AD9910_driver_0.slave_en_wire)? 1'bz:io_val;

AD9910_driver
#(
    .NUM_CS(2)
)
AD9910_driver_0
(
    .clk(clk),
    .reset(reset),
    .auto_start(auto_start),
    .flush_rto_fifo(flush_rto_fifo),
    .write_rto_fifo(write_rto_fifo),
    .rto_fifo_din(rto_fifo_din),
    .counter(counter),
    .flush_rti_fifo(flush_rti_fifo),
    .read_rti_fifo(read_rti_fifo),
    .gpo_override_en(gpo_override_en),
    .gpo_selected_en(gpo_selected_en),
    .gpo_override_value(gpo_override_value),
    .rto_timestamp_error_data(rto_timestamp_error_data),
    .rto_overflow_error_data(rto_overflow_error_data),
    .rto_timestamp_error(rto_timestamp_error),
    .rto_overflow_error(rto_overflow_error),
    .rto_fifo_full(rto_fifo_full),
    .rto_fifo_empty(rto_fifo_empty),
    .rti_out(rti_out),
    .rti_overflow_error_data(rti_overflow_error_data),
    .rti_overflow_error(rti_overflow_error),
    .rti_underflow_error(rti_underflow_error),
    .rti_fifo_full(rti_fifo_full),
    .rti_fifo_empty(rti_fifo_empty),
    .busy(busy),
    .gpo_error_data(gpo_error_data),
    .gpo_overrided(gpo_overrided),
    .gpo_busy_error(gpo_busy_error),
    .gpi_data_ready(gpi_data_ready),
    .gpi_out(gpi_out),
    .io(io),
    .sck(sck),
    .cs(cs)
    );

logic start;
logic counter_offset;
logic offset_en;

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

initial begin
    clk = 1'b0;
    reset = 1'b0;
    auto_start = 1'b0;
    flush_rto_fifo = 1'b0;
    write_rto_fifo = 1'b0;
    rto_fifo_din[127:0] = 128'h0;
    flush_rti_fifo = 1'b0;
    read_rti_fifo = 1'b0;
    gpo_override_en = 1'b0;
    gpo_selected_en = 1'b0;
    gpo_override_value[63:0] = 64'h0;
    start = 1'b0;
    counter_offset = 64'h0;
    offset_en = 1'b0;
    
    #10
    reset = 1'b1;
    #10
    reset = 1'b0;
    
    #100
    rto_fifo_din[127:0] = 128'd1 << 111 | 128'd1 << 96 | 128'd5 << 32 | 128'd1 << 31 | 128'd0 << 29 |  128'd1 << 16 |  128'd31 << 11 | 128'd0 << 8 | 128'd8;
    write_rto_fifo = 1'b1;
    #10
    write_rto_fifo = 1'b0;
    
    #100
    rto_fifo_din[127:0] = 128'd0 << 111 | 128'd1 << 96 | 128'd10 << 32 | 128'b10111111111111110000001111001101;
    write_rto_fifo = 1'b1;
    #10
    write_rto_fifo = 1'b0;
    
    #100
    rto_fifo_din[127:0] = 128'd1 << 111 | 128'd1 << 96 | 128'h114 << 32 | 128'd1 << 31 | 128'd1 << 29 |  128'd1 << 16 |  128'd7 << 11 | 128'd1 << 8 | 128'd8;
    write_rto_fifo = 1'b1;
    #10
    write_rto_fifo = 1'b0;
    
    #100
    rto_fifo_din[127:0] = 128'd0 << 111 | 128'd1 << 96 | 128'h115 << 32 | 128'b00110111111111110000001111001101;
    write_rto_fifo = 1'b1;
    #10
    write_rto_fifo = 1'b0;
    
    #100
    rto_fifo_din[127:0] = 128'd1 << 111 | 128'd1 << 96 | 128'h163 << 32 | 128'd0 << 31 | 128'd1 << 30 | 128'd0 << 29 |  128'd1 << 16 |  128'd7 << 11 | 128'd1 << 8 | 128'd8;
    write_rto_fifo = 1'b1;
    #10
    write_rto_fifo = 1'b0;
    
    #100
    rto_fifo_din[127:0] = 128'd0 << 111 | 128'd1 << 96 | 128'h164 << 32 | 128'b0;
    write_rto_fifo = 1'b1;
    #10
    write_rto_fifo = 1'b0;
    
    #100
    rto_fifo_din[127:0] = 128'd1 << 111 | 128'd1 << 96 | 128'h1ae << 32 | 128'd0 << 31 | 128'd1 << 30 | 128'd1 << 29 |  128'd1 << 16 |  128'd7 << 11 | 128'd0 << 8 | 128'd8;
    write_rto_fifo = 1'b1;
    #10
    write_rto_fifo = 1'b0;
    
    #100
    rto_fifo_din[127:0] = 128'd0 << 111 | 128'd1 << 96 | 128'h1af << 32 | 128'b0;
    write_rto_fifo = 1'b1;
    #10
    write_rto_fifo = 1'b0;
    
    #30
    auto_start = 1'b1;
    start = 1'b1;
end

initial begin
    #7000
    read_rti_fifo = 1'b1;
    #10
    read_rti_fifo = 1'b0;
    #10
    read_rti_fifo = 1'b1;
    #10
    read_rti_fifo = 1'b0;
    #10
    read_rti_fifo = 1'b1;
    #10
    read_rti_fifo = 1'b0;
end

initial begin
    io_val = 1'b1;
end

endmodule
