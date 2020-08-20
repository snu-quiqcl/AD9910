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
    input wire clk,
    input wire auto_start,
    input wire reset,
    input wire flush,
    input wire write,
    input wire [127:0] fifo_din,
    input wire [63:0] counter,
    output wire counter_matched,
    output wire [127:0] rto_out,
    output wire [127:0] timestamp_error_data,
    output wire [127:0] overflow_error_data,
    output wire timestamp_error,
    output wire overflow_error,
    output wire full,
    output wire empty
    );

reg counter_match;
reg [127:0] fifo_output;
reg [127:0] overflow_error_data_buffer;
reg [127:0] timestamp_error_data_buffer;
reg overflow_error_state;
reg timestamp_error_state;

wire flush_fifo;
wire wr_en;
wire write_en;;
wire rd_en;
wire overflow_error_wire;
wire timestamp_error_wire;
wire timestamp_match;
wire[127:0] fifo_dout;
wire full_wire;
wire empty_wire;
wire overflow_dummy_wire;
wire underflow_dummy_wire;
wire timestamp_match_not_empty;
wire fifo_output_en;

assign flush_fifo = flush || reset;
assign write_en = write;
assign timestamp_match = ( fifo_dout[95:32] == counter[63:0] );
assign timestamp_match_not_empty = ( ~empty_wire && timestamp_match && auto_start );
assign timestamp_error_wire = (counter[63:0] > fifo_dout[95:32]) && auto_start && ~empty_wire;
assign rd_en = timestamp_error_wire || timestamp_match_not_empty;
assign wr_en = write_en && ~full_wire;
assign overflow_error_wire = full_wire && write_en;
assign fifo_output_en = ~timestamp_error_wire && timestamp_match_not_empty;
assign rto_out[127:0] = fifo_output[127:0];
assign overflow_error = overflow_error_state;
assign timestamp_error = timestamp_error_state;
assign empty = empty_wire;
assign full = full_wire;
assign overflow_error_data[127:0] = overflow_error_data_buffer[127:0];
assign timestamp_error_data[127:0] = timestamp_error_data_buffer[127:0];
assign counter_matched = counter_match;

fifo_generator_1 rto_core_FIFO(
    .clk(clk),
    .rst(flush_fifo),
    .din(fifo_din),
    .wr_en(wr_en),
    .rd_en(rd_en),
    .dout(fifo_dout),
    .full(full_wire),
    .overflow(overflow_dummy_wire),
    .empty(empty_wire),
    .underflow(underflow_dummy_wire)
);

always @(posedge clk) begin
    if( reset ) begin
        counter_match <= 1'b0;
        overflow_error_state <= 1'b0;
        timestamp_error_state <= 1'b0;
        fifo_output[127:0] <= 128'h0;
        overflow_error_data_buffer[127:0] <= 128'h0;
        timestamp_error_data_buffer[127:0] <= 128'h0;
        counter_match <= 1'b0;
    end
    else begin
        counter_match <= timestamp_match_not_empty;
        overflow_error_state <= overflow_error_wire;
        timestamp_error_state <= timestamp_error_wire;
        if( fifo_output_en ) begin
            fifo_output[127:0] <= fifo_dout;
            counter_match <= 1'b1;
        end
        
        else begin
            counter_match <= 1'b0;
        end
        
        if( overflow_error_wire ) begin
            overflow_error_data_buffer[127:0] <= fifo_din[127:0];
        end
        
        if( timestamp_error_wire ) begin
            timestamp_error_data_buffer[127:0] <= fifo_dout[127:0];
        end
    end
end

endmodule
