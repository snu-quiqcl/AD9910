`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/18 22:38:33
// Design Name: 
// Module Name: new_testbench_gpo_core
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


module new_testbench_gpo_core;


logic CLK100MHZ;
logic override_en;
logic selected_en;
logic [63:0] override_value;
logic counter_matched;
logic [127:0] gpo_in;
logic busy;
logic reset;
/*
wire selected;
wire [111:0] error_data;
wire overrided;
wire busy_error;
wire[47:0] gpo_out;
*/
logic selected;
logic [127:0] error_data;
logic overrided;
logic busy_error;
logic [63:0] gpo_out;

gpo_core_prime
#(
    .DEST_VAL(15'h5),
    .CHANNEL_LENGTH(12)
)
gpo_core_0
(
    .CLK100MHZ(CLK100MHZ),
    .reset(reset),
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
    reset = 1'b1;
    #30
    reset = 1'b0;
    #10
    
    //override
    override_en = 1;
    selected_en = 0;
    override_value = 64'h500000;
    counter_matched = 0;
    gpo_in = 128'h0;
    busy = 1'b0;
    
    //update using gpo_in
    #10
    override_en = 0;
    selected_en = 0;
    override_value = 64'h700000 | 64'h0007 << 32;
    counter_matched = 1'b1;
    gpo_in = 128'h900000 | 128'h0005 << 96;
    busy = 1'b0;
    
    //make counter_matched low
    #10
    counter_matched = 1'b0;
    
    //gpo_in with different channel
    #30
    override_en = 0;
    selected_en = 0;
    override_value = 64'h800000 | 64'h0008 << 32;
    counter_matched = 1'b1;
    gpo_in = 128'h900000 | 128'h0004 << 96;
    
    //make counter_matched low
    #10
    counter_matched = 1'b0;
    
    //make busy high
    #10
    busy = 1'b1;
    
    //gpo_in
    #10
    override_en = 0;
    selected_en = 0;
    override_value = 64'h700000 | 64'h0007 << 32;
    counter_matched = 1'b1;
    gpo_in = 128'h900000 | 128'h0005 << 96;
    
    //make counter_matched low
    #10
    counter_matched = 1'b0;
    
    #10
    override_en = 1'b1;
    selected_en = 1'b0;
    override_value = 64'h800000 | 64'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 128'h900000 | 128'h0005 << 96;
    
    #10
    
    #10
    override_en = 1'b1;
    selected_en = 1'b1;
    override_value = 64'h900000 | 64'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 128'h900000 | 128'h0005 << 96;
    
    #10
    override_en = 1'b0;
    selected_en = 1'b0;
    
    #30
    busy = 1'b0;
    
    #10;
    override_en = 1'b1;
    selected_en = 1'b1;
    override_value = 64'h200000 | 64'h0005 << 32;
    counter_matched = 1'b1;
    gpo_in = 128'h100000 | 128'h0005 << 96;
    
    #10
    override_en = 1'b1;
    selected_en = 1'b0;
    override_value = 64'h200000 | 64'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 128'h100000 | 128'h0005 << 96;
    
    #30
    override_en = 1'b1;
    selected_en = 1'b0;
    override_value = 64'h400000 | 64'h0005 << 32;
    counter_matched = 1'b1;
    gpo_in = 128'h300000 | 128'h0005 << 96;
    
    #10
    override_en = 1'b0;
    selected_en = 1'b0;
    override_value = 64'h600000 | 64'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 128'h500000 | 128'h0005 << 96;
    
    #10
    busy = 1'b1;
    
    #10
    override_en = 1'b1;
    selected_en = 1'b0;
    override_value = 64'h800000 | 64'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 128'h700000 | 128'h0005 << 96;
    
    #10
    override_en = 1'b1;
    selected_en = 1'b1;
    override_value = 64'h200000 | 64'h0005 << 32;
    counter_matched = 1'b1;
    gpo_in = 128'h100000 | 128'h0005 << 96;
    
    #10
    override_en = 1'b1;
    selected_en = 1'b1;
    override_value = 64'h400000 | 64'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 128'h300000 | 128'h0005 << 96;
    #10
    override_en = 1'b0;
    selected_en = 1'b0;
    override_value = 64'h600000 | 64'h0005 << 32;
    counter_matched = 1'b1;
    gpo_in = 128'h500000 | 128'h0006 << 96;
    
    #10
    counter_matched = 1'b0;
    busy = 1'b0;
    
    #30
    override_en = 1'b1;
    selected_en = 1'b1;
    override_value = 64'h400000 | 64'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 128'h300000 | 128'h0005 << 96;
    
    #10
    override_en = 1'b0;
    selected_en = 1'b0;
    override_value = 64'h400000 | 64'h0005 << 32;
    counter_matched = 1'b1;
    gpo_in = 128'h300000 | 128'h0005 << 96;
    
    #10
    counter_matched = 1'b0;
    
end

endmodule
