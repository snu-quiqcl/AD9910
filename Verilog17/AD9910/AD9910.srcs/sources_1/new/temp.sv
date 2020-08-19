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


module rto_core_prime2(
    input wire clk,
    input wire auto_start,
    input wire reset,
    input wire write,
    input wire [31:0] wr_data,
    input wire [63:0] counter,
    input wire cs,
    input wire read,
    input wire [4:0] addr,
    input wire clk,
    input wire [15:0] dest,
    output wire counter_matched,
    output wire [127:0] rto_out,
    output wire [127:0] timestamp_error_data,
    output wire [127:0] overflow_error_data,
    output wire timestamp_error,
    output wire overflow_error,
    output wire [31:0] rd_data,
    output wire full,
    output wire empty
    );

reg counter_match;
reg [127:0] fifo_output;
reg [63:0] time_reg;
reg [127:0] overflow_error_data_buffer;
reg [127:0] timestamp_error_data_buffer;
reg overflow_error_state;
reg timestamp_error_state;

wire flush;
wire wr_en;
wire write_en;;
wire rd_en;
wire[15:0] dest_temp;
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

assign flush = ( (addr[4:0] == 5'h5 ) & cs & write ) | reset;
assign write_en = ( addr[4:0] == 5'h2 ) & cs & write;
assign dest_temp[15:0] = dest[15:0];
assign timestamp_match = ( fifo_dout[95:64] == counter[63:0] );
assign timestamp_match_not_empty = ( ~empty_wire & timestamp_match );
assign timestamp_error_wire = (fifo_output[95:32] >= fifo_dout[95:32]) & auto_start & ~empty_wire;
assign rd_en = timestamp_error_wire | timestamp_match_not_empty;
assign wr_en = write_en & ~full;
assign overflow_error_wire = full & write_en;
assign fifo_output_en = ~timestamp_error_wire & timestamp_match_not_empty;
assign rto_out[127:0] = fifo_output[127:0];
assign overflow_error = overflow_error_state;
assign timestamp_error = timestamp_error_state;

always @ ( * ) begin
    rd_data = 0;
    case(addr)
        5'd3:
        begin
            rd_data[31:0] = {30'b0, full, empty};
        end
        5'd4:
        begin
            rd_data[31:0] = fifo_dout[31:0];
        end
        5'd5:
        begin
            rd_data[31:0] = fifo_dout[63:32];
        end
        5'd6:
        begin
            rd_data[31:0] = fifo_dout[63:32];
        end
        5'd7:
        begin
            rd_data[31:0] = fifo_dout[63:32];
        end
    endcase
end

fifo_generator_1 rto_core_FIFO(
    .clk(clk),
    .rst(flush),
    .din({16'h0, dest_temp[15:0], time_reg, wr_data}),
    .wr_en(wr_en),
    .rd_en(rd_en),
    .dout(fifo_dout),
    .full(full_wire),
    .overflow(overflow_dummy_wire),
    .empty(empty_wire),
    .underflow(underflow_dummy_wire)
);

always @(posedge clk) begin
    counter_match <= timestamp_match_not_empty;
    overflow_error_state <= overflow_error_wire;
    timestamp_error_state <= timestamp_error_wire;
    if( fifo_output_en ) begin
        fifo_output[127:0] <= fifo_dout;
    end
    
    if( overflow_error_wire ) begin
        overflow_error_data_buffer[127:0] <= {16'h0, dest_temp[15:0], time_reg, wr_data};
    end
    
    if( timestamp_error_wire ) begin
        timestamp_error_data_buffer[127:0] <= fifo_dout[127:0];
    end
    
    if( addr[0] == 1'b0 ) begin
        time_reg[31:0] <= wr_data[31:0];
    end
    
    if( addr[0] == 1'b1 ) begin
        time_reg[63:32] <= wr_data[31:0];
    end
end

endmodule
