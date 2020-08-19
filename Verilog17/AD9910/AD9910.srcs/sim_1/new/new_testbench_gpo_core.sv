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
    //override
    CLK100MHZ = 0;
    override_en = 1;
    selected_en = 0;
    override_value = 48'h500000;
    counter_matched = 0;
    gpo_in = 112'h0;
    busy = 1'b0;
    
    //update using gpo_in
    #10
    override_en = 0;
    selected_en = 0;
    override_value = 48'h700000 | 48'h0007 << 32;
    counter_matched = 1'b1;
    gpo_in = 112'h900000 | 112'h0005 << 96;
    busy = 1'b0;
    
    //make counter_matched low
    #10
    counter_matched = 1'b0;
    
    //gpo_in with different channel
    #30
    override_en = 0;
    selected_en = 0;
    override_value = 48'h800000 | 48'h0008 << 32;
    counter_matched = 1'b1;
    gpo_in = 112'h900000 | 112'h0004 << 96;
    
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
    override_value = 48'h700000 | 48'h0007 << 32;
    counter_matched = 1'b1;
    gpo_in = 112'h900000 | 112'h0005 << 96;
    
    //make counter_matched low
    #10
    counter_matched = 1'b0;
    
    #10
    override_en = 1'b1;
    selected_en = 1'b0;
    override_value = 48'h800000 | 48'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 112'h900000 | 112'h0005 << 96;
    
    #10
    
    #10
    override_en = 1'b1;
    selected_en = 1'b1;
    override_value = 48'h900000 | 48'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 112'h900000 | 112'h0005 << 96;
    
    #10
    override_en = 1'b0;
    selected_en = 1'b0;
    
    #30
    busy = 1'b0;
    
    #10;
    override_en = 1'b1;
    selected_en = 1'b1;
    override_value = 48'h200000 | 48'h0005 << 32;
    counter_matched = 1'b1;
    gpo_in = 112'h100000 | 112'h0005 << 96;
    
    #10
    override_en = 1'b1;
    selected_en = 1'b0;
    override_value = 48'h200000 | 48'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 112'h100000 | 112'h0005 << 96;
    
    #30
    override_en = 1'b1;
    selected_en = 1'b0;
    override_value = 48'h400000 | 48'h0005 << 32;
    counter_matched = 1'b1;
    gpo_in = 112'h300000 | 112'h0005 << 96;
    
    #10
    override_en = 1'b0;
    selected_en = 1'b0;
    override_value = 48'h600000 | 48'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 112'h500000 | 112'h0005 << 96;
    
    #10
    busy = 1'b1;
    
    #10
    override_en = 1'b1;
    selected_en = 1'b0;
    override_value = 48'h800000 | 48'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 112'h700000 | 112'h0005 << 96;
    
    #10
    override_en = 1'b1;
    selected_en = 1'b1;
    override_value = 48'h200000 | 48'h0005 << 32;
    counter_matched = 1'b1;
    gpo_in = 112'h100000 | 112'h0005 << 96;
    
    #10
    override_en = 1'b1;
    selected_en = 1'b1;
    override_value = 48'h400000 | 48'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 112'h300000 | 112'h0005 << 96;
    #10
    override_en = 1'b0;
    selected_en = 1'b0;
    override_value = 48'h600000 | 48'h0005 << 32;
    counter_matched = 1'b1;
    gpo_in = 112'h500000 | 112'h0006 << 96;
    
    #10
    counter_matched = 1'b0;
    busy = 1'b0;
    
    #30
    override_en = 1'b1;
    selected_en = 1'b1;
    override_value = 48'h400000 | 48'h0005 << 32;
    counter_matched = 1'b0;
    gpo_in = 112'h300000 | 112'h0005 << 96;
    
    #10
    override_en = 1'b0;
    selected_en = 1'b0;
    override_value = 48'h400000 | 48'h0005 << 32;
    counter_matched = 1'b1;
    gpo_in = 112'h300000 | 112'h0005 << 96;
    
    #10
    counter_matched = 1'b0;
end

endmodule
