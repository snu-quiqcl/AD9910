`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/18 22:07:32
// Design Name: 
// Module Name: test_bench_gpo_core
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


module test_bench_gpo_core;

logic CLK100MHZ;
logic override_en;
logic selected_en;
logic [47:0] override_value;
logic counter_matched;
logic [111:0] gpo_in;
logic busy;
/*
wire selected;
wire [111:0] error_data;
wire overrided;
wire busy_error;
wire[47:0] gpo_out;
*/
logic selected;
logic [111:0] error_data;
logic overrided;
logic busy_error;
logic [47:0] gpo_out;

gpo_core
#(
    .DEST_VAL(15'h5),
    .CHANNEL_LENGTH(12)
)
gpo_core_0
(
    .CLK100MHZ(CLK100MHZ),
    .override_en(override_en),
    .selected_en(selected_en),
    .override_value(override_value),
    .counter_matched(counter_matched),
    .gpo_in(gpo_in),
    .busy(busy),
    .selected(selected),
    .error_data(error_data),
    .overrided(overrided),
    .busy_error(busy_error),
    .gpo_out(gpo_out)
    );
always begin
    #5
    CLK100MHZ = ~CLK100MHZ;
end

initial begin
    CLK100MHZ = 0;
    override_en = 1;
    selected_en = 0;
    override_value = 48'h500000;
    counter_matched = 0;
    gpo_in = 112'h0;
    busy = 1'b0;
    #10
    override_en = 1;
    selected_en = 1;
    override_value = 48'h500000;
    counter_matched = 0;
    gpo_in = 112'h0;
    busy = 1'b1;
end

endmodule
