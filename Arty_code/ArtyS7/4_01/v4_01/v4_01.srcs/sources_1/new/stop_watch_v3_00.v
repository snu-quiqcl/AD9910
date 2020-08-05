`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2017/12/14 14:06:34
// Design Name: 
// Module Name: stop_watch
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 3.00 - Re-designed stopwatch
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

module flag(input set, input reset, output reg q);
    always@(posedge set, posedge reset)
        if (reset) q <= 1'd0;
        else if (set) q <= 1'd1;
endmodule

module stop_watch
#(parameter COUNTER_LENGTH_BITS = 'd16 // This value is determined by binary_counter IP setting
//  parameter COUNTING_WAITING_MAX = {(COUNTER_LENGTH_BITS-3){1'b1}}
) // https://groups.google.com/forum/#!topic/comp.lang.verilog/6xZxOLUcNYI
(
    input clk_800MHz,
    input start,
    input stop,
    input reset,
    output [COUNTER_LENGTH_BITS-1:0] interval,
    output stopped /*,
    output debug_started,
    output debug_stop_signal_captured_at_start_posedge,
    output debug_stop_negedge_detected_after_start,
    output debug_stop_signal_mask*/
    );

/*    
	////////////////////////////////////////////////////////////////
    // Shortening reset pulse
    ////////////////////////////////////////////////////////////////
    // There was a racing condition that start signal might arrive before reset will be off, and in some stopwatches,
    // there should be a pause (nop operation) between reset and start signal. The shortening of the reset signal can 
    // resolve such kind of problem.
    wire reset_shortened;
    reg [10:1] reset_10delays;
    initial begin
       reset_10delays = 'd0;
    end

    always @ (posedge clk_800MHz)
            begin
                reset_10delays[10:1] <= {reset_10delays[9:1], reset};
            end
    
    assign reset_shortened = reset & ~reset_10delays[4]; // 4 x 1.25ns width
*/
    wire reset_shortened;
    assign reset_shortened = reset; // Decided not to shorten it
	////////////////////////////////////////////////////////////////
    // Making sure that stopped signal will be registered after started
    ////////////////////////////////////////////////////////////////

    wire started;
    flag started_flag(.set(start), .reset(reset_shortened), .q(started));

    // There can be a race condition that the stop signal is already 1 when the start posedge is detected.
    // In this case, there is a chance that stopped_flag will be set immediately after start posedge is detected, if the started flag is AND'ed with stop.
    // In the following, I capture the stop signal at start posedge and does not allow any stopped_flag until stop signal's negedge is detected. 
    reg stop_signal_captured_at_start_posedge;
    initial stop_signal_captured_at_start_posedge <= 'd0;
    always@(posedge start)
        stop_signal_captured_at_start_posedge <= stop;
        
    wire stop_negedge_detected_after_start;
    flag stop_negedge_detected_after_start_flag(.set(started & ~stop), .reset(reset_shortened), .q(stop_negedge_detected_after_start));
    
    wire stop_signal_mask;
    assign stop_signal_mask = (stop_signal_captured_at_start_posedge) ? ( (stop_negedge_detected_after_start) ? started : 1'b0  ): started;
    flag stopped_flag(.set(stop & stop_signal_mask), .reset(reset_shortened), .q(stopped));

    /*
    assign debug_started = started;
    assign debug_stop_signal_captured_at_start_posedge = stop_signal_captured_at_start_posedge;
    assign debug_stop_negedge_detected_after_start = stop_negedge_detected_after_start;
    assign debug_stop_signal_mask = stop_signal_mask;
    */

	////////////////////////////////////////////////////////////////
	// Counter
	////////////////////////////////////////////////////////////////
    wire [COUNTER_LENGTH_BITS-1:0] counter_output;
    assign interval = counter_output;
        
    c_counter_binary_16bits counter(
        .CLK(clk_800MHz),
        .CE(started & ~stopped),
        .SCLR(reset_shortened),
        .Q(counter_output)
    );
    
endmodule
