`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/12 10:49:42
// Design Name: 
// Module Name: dds_parallel_write
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


module dds_parallel_write
#(
    parameter PARALLEL_LENGTH = 18,
    parameter COUNTER_LENGTH = 64,
    parameter FIFO_DEPTH = 1024
)
(
    input clk,
    input pdclk,
    input[PARALLEL_LENGTH - 1:0] force_value_input,
    input force_select,
    input fifo_flush,
    input reset_counter,
    input fifo_write,
    input[PARALLEL_LENGTH + COUNTER_LENGTH + 1:0] fifo_input,
    output [PARALLEL_LENGTH - 1:0] parallel_output
    );

reg[PARALLEL_LENGTH - 1:0]out_buffer1;
reg[PARALLEL_LENGTH - 1:0]out_buffer2;
wire[COUNTER_LENGTH - 1:0] fifo_timestamp;
wire [PARALLEL_LENGTH + COUNTER_LENGTH + 1:0] fifo_data_out;
wire check_timestamp_counter;
wire [PARALLEL_LENGTH + COUNTER_LENGTH + 1:0] fifo_data_in;
wire [COUNTER_LENGTH - 1:0] counter_out;  
wire empty_fifo;  
wire full_fifo;
wire write_fifo;

reg[PARALLEL_LENGTH - 1:0] force_value;
reg select;

initial begin
    force_value <= 0;
    select <= 0;
end

assign check_timestamp_counter = ( counter_out == fifo_timestamp );
assign fifo_timestamp = fifo_data_out[PARALLEL_LENGTH + COUNTER_LENGTH + 1:PARALLEL_LENGTH + 2];

always @(posedge clk) begin
    if(check_timestamp_counter == 1'b1) begin
        select <= 0;
    end
    
    else if( force_select == 1'b1) begin
        select <= 1;
    end
    
    else begin
        select <= select;
    end
end

always @(posedge clk) begin
    if( force_select == 1'b1) begin
        force_value <= force_value_input;
    end
    
    else begin
        force_value <= force_value;
    end
end

always @ (negedge pdclk) begin
    if( flush == 1'b1 ) begin
        out_buffer1 <= force_value;
    end
    
    else if( select == 1'b0 & check_timestamp_counter == 1'b0) begin
        out_buffer1 <= out_buffer1;
    end
    
    else if( select == 1'b1 & ~( check_timestamp_counter == 1'b1 ) ) begin
        out_buffer1 <= force_value;
    end
    
    else begin
        out_buffer1 <= fifo_data_out[PARALLEL_LENGTH - 1:0];
    end
    out_buffer2 <= out_buffer1;
end

fifo_sync #(
    .FIFO_DEPTH(FIFO_DEPTH)
) 
dds_parallel_fifo1
(
    .clk(CLK100MHZ),
    .read(check_timestamp_counte & ~empty_fifo),
    .write(write_fifo & ~full),
    .data_in(fifo_data_in),
    .reset(flush),
    .empty(empty_fifo),
    .full(full_fifo),
    .data_out(fifo_data_out)
);
endmodule
