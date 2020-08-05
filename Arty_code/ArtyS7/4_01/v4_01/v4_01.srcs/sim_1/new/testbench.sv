`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2018/01/25 19:39:02
// Design Name: 
// Module Name: testbench
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

import parameterPkg::*;

module testbench(

    );
    parameter REGISTER_ADDR_WIDTH = 5;
    parameter REGISTER_WIDTH = 16;

    parameter OUTPUT_FIFO_DATA_WIDTH = 64; // Defined in fifo_generator_bram_64x1024 IP
    parameter OUTPUT_FIFO_DATA_COUNT_WIDTH = 11; // Data length is 1024

    
    reg CLK100MHZ;
    initial
    begin
        CLK100MHZ = 1;
    end
    
    always
        #5 CLK100MHZ = ! CLK100MHZ;
        
    
    /////////////////////////////////////////////////////////////////
    // Sequencer instruction memory
    /////////////////////////////////////////////////////////////////
    parameter INSTRUCTION_MEMORY_DATA_WIDTH = 64;
    parameter INSTRUCTION_MEMORY_ADDR_WIDTH = 9;
    reg instruction_memory_we;
    reg [INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] instruction_memory_address;
    reg [INSTRUCTION_MEMORY_DATA_WIDTH-1:0] instruction_memory_data_in;
    wire [INSTRUCTION_MEMORY_DATA_WIDTH-1:0] instruction_memory_data_out;
    wire [INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] PC;
    wire [INSTRUCTION_MEMORY_DATA_WIDTH-1:0] instr;

    initial begin
        instruction_memory_we = 0;
        instruction_memory_address = 0;
        instruction_memory_data_in = 0;
    end
    
    dual_port_ram instruction_memory(
        .clk(~CLK100MHZ),
        .addr_a(instruction_memory_address),
        .dout_a(instruction_memory_data_out),
        .we_a(instruction_memory_we),
        .din_a(instruction_memory_data_in),
        .addr_b(PC),
        .dout_b(instr)
    );

    /////////////////////////////////////////////////////////////////
    // Main sequencer
    /////////////////////////////////////////////////////////////////

    wire [15:0] trigger_level_in;
    wire [15:0] output_ports[OUTPUT_PORT_NUMBER-1:0];
    wire [15:0] trigger_out;
/////////////////////////////////////////////////////////////////    
    reg start_sequencer;
    wire stopped;
    wire [15:0] counters_13_0[13:0];
    wire [REGISTER_WIDTH-1:0] rd1, rd2, rd3;
    wire output_fifo_we; 
    
    initial begin
//        trigger_level_in = 0;
        #0 start_sequencer = 0;
        #350 start_sequencer = 1;
        #10 start_sequencer = 0;
    end

    
/////////////////////////////////////////////////////////////////    

    sequencer seq(.trigger_level_in(trigger_level_in), .clk(CLK100MHZ), .start(start_sequencer), .stopped(stopped), .pc(PC),
        .fifo_we(output_fifo_we), .rd1(rd1), .rd2(rd2), .rd3(rd3), 
        .output_ports(output_ports), 
        .trigger_out(trigger_out), .instr(instr),
        .counters_13_0(counters_13_0)
    );

    wire [OUTPUT_FIFO_DATA_COUNT_WIDTH-1:0] output_fifo_data_count;

    reg data_fifo_rd_en;
    wire [OUTPUT_FIFO_DATA_WIDTH-1:0] data_fifo_dout;
    
    initial data_fifo_rd_en = 0;
    
    fifo_generator_bram_64x1024 output_fifo(
        .clk(CLK100MHZ),
        .srst(1'b0),
        .din({rd1, rd2, rd3, instr[31:16]}),
        .wr_en(output_fifo_we),
        .rd_en(data_fifo_rd_en),
        .dout(data_fifo_dout),
        .full(),
        .empty(),
        .data_count(output_fifo_data_count)
    );



    reg [1:32] patterns;
    initial patterns = {32{1'b0}};
    
    // External output pins
    wire  ja_2, ja_3, ja_6, ja_7, jb_0, jb_1;

    // External input pins    
    wire jb_2, jb_3, jb_4, jb_5, jb_6, jb_7;
    
    // The following connection is only for testing purpose
    assign {jb_4, jb_5, jb_6, jb_7, jb_3} = {ja_2, ja_3, ja_7, jb_0, jb_1}; // ja_6 is currently assumed to be used for AOM_200MHz and not connected back to sequencer
    assign jb_2 = 1'b0;

    wire [15:0] external_output;
    // In main, external_output is connected to output_port[0] through mux, but here we assume that it is directly connected to output_port[0] 
    //mux2 #(16) external_control(.d0(output_ports[0]), .d1(patterns[17:32]), .select(manual_control_on), .y(external_output));
    assign external_output = output_ports[0];
   
    
    
    /////////////////////////////////////////////////////////////////
    // Counter connections
    /////////////////////////////////////////////////////////////////
    wire jb_4_counter_clock_enable, jb_5_counter_clock_enable, jb_6_counter_clock_enable, jb_7_counter_clock_enable; 
    wire jb_4_counter_reset, jb_5_counter_reset, jb_6_counter_reset, jb_7_counter_reset;
    wire [15:0] jb_4_counter_output, jb_5_counter_output, jb_6_counter_output, jb_7_counter_output;
    
    counter jb_4_counter(.clock(jb_4), .clockEnable(jb_4_counter_clock_enable), .reset(jb_4_counter_reset), .q(jb_4_counter_output) );
    counter jb_5_counter(.clock(jb_5), .clockEnable(jb_5_counter_clock_enable), .reset(jb_5_counter_reset), .q(jb_5_counter_output) );
    counter jb_6_counter(.clock(jb_6), .clockEnable(jb_6_counter_clock_enable), .reset(jb_6_counter_reset), .q(jb_6_counter_output) );
    counter jb_7_counter(.clock(jb_7), .clockEnable(jb_7_counter_clock_enable), .reset(jb_7_counter_reset), .q(jb_7_counter_output) );

    ////////////////////////////////////////////////////////////////
    // MMCM
    ////////////////////////////////////////////////////////////////
    wire clk_800MHz_out1, clk_800MHz_out2, clk_800MHz_out3, clk_800MHz_out4, clk_800MHz_out5, clk_800MHz_locked;
    clk_800MHz clockGenerator
    (
      // Clock out ports
      .clk_800MHz_out1(clk_800MHz_out1),
      .clk_800MHz_out2(clk_800MHz_out2),
      .clk_800MHz_out3(clk_800MHz_out3),
      .clk_800MHz_out4(clk_800MHz_out4),
      .clk_800MHz_out5(clk_800MHz_out5),
      .clk_800MHz_out6(),
      .clk_800MHz_out7(),
      // Status and control signals
      .reset(1'b0), // default is active-high
      .locked(clk_800MHz_locked),
     // Clock in ports
      .clk_in1(CLK100MHZ)
    );

    /////////////////////////////////////////////////////////////////
    // Stopwatch connections
    /////////////////////////////////////////////////////////////////
    wire jb_4_stopwatch_start, jb_5_stopwatch_start, jb_6_stopwatch_start, jb_7_stopwatch_start, jb_3_stopwatch_start;
    wire jb_4_stopwatch_reset, jb_5_stopwatch_reset, jb_6_stopwatch_reset, jb_7_stopwatch_reset, jb_3_stopwatch_reset;
    wire [15:0] jb_4_stopwatch_output, jb_5_stopwatch_output, jb_6_stopwatch_output, jb_7_stopwatch_output, jb_3_stopwatch_output;
    wire jb_4_stopwatch_stopped, jb_5_stopwatch_stopped, jb_6_stopwatch_stopped, jb_7_stopwatch_stopped, jb_3_stopwatch_stopped;
    
    stop_watch jb_4_stopwatch(.clk_800MHz(clk_800MHz_out1), .start(jb_4_stopwatch_start), .stop(jb_4), .reset(jb_4_stopwatch_reset),
    .interval(jb_4_stopwatch_output), .stopped(jb_4_stopwatch_stopped) );

//    wire debug0, debug1, debug2, debug3;
    stop_watch jb_5_stopwatch(.clk_800MHz(clk_800MHz_out2), .start(jb_5_stopwatch_start), .stop(jb_5), .reset(jb_5_stopwatch_reset),
    .interval(jb_5_stopwatch_output), .stopped(jb_5_stopwatch_stopped) );
/*    .interval(jb_5_stopwatch_output), .stopped(jb_5_stopwatch_stopped), 
    .debug_started(debug0),
    .debug_stop_signal_captured_at_start_posedge(debug1),
    .debug_stop_negedge_detected_after_start(debug2),
    .debug_stop_signal_mask(debug3)
    );
*/
    stop_watch jb_6_stopwatch(.clk_800MHz(clk_800MHz_out3), .start(jb_6_stopwatch_start), .stop(jb_6), .reset(jb_6_stopwatch_reset),
    .interval(jb_6_stopwatch_output), .stopped(jb_6_stopwatch_stopped) );

    stop_watch jb_7_stopwatch(.clk_800MHz(clk_800MHz_out4), .start(jb_7_stopwatch_start), .stop(jb_7), .reset(jb_7_stopwatch_reset),
    .interval(jb_7_stopwatch_output), .stopped(jb_7_stopwatch_stopped) );

    stop_watch jb_3_stopwatch(.clk_800MHz(clk_800MHz_out5), .start(jb_3_stopwatch_start), .stop(jb_3), .reset(jb_3_stopwatch_reset),
    .interval(jb_3_stopwatch_output), .stopped(jb_3_stopwatch_stopped) );


    /////////////////////////////////////////////////////////////////
    // Input connections to sequencer
    /////////////////////////////////////////////////////////////////
    
    assign counters_13_0[0] = jb_4_counter_output;
    assign counters_13_0[1] = jb_5_counter_output;
    assign counters_13_0[2] = jb_6_counter_output;
    assign counters_13_0[3] = jb_7_counter_output;
    assign counters_13_0[4] = 'd0;
    assign counters_13_0[5] = 'd0;
    assign counters_13_0[6] = jb_4_stopwatch_output;
    assign counters_13_0[7] = jb_5_stopwatch_output;
    assign counters_13_0[8] = jb_6_stopwatch_output;
    assign counters_13_0[9] = jb_7_stopwatch_output;
    assign counters_13_0[10] = jb_3_stopwatch_output;
    assign counters_13_0[11] = 'd0;
    assign counters_13_0[12] = 'd0;
    assign counters_13_0[13] = patterns[1:16];


    assign trigger_level_in[15] = jb_4_stopwatch_stopped;
    assign trigger_level_in[14] = jb_5_stopwatch_stopped;
    assign trigger_level_in[13] = jb_6_stopwatch_stopped;
    assign trigger_level_in[12] = jb_7_stopwatch_stopped;
    assign trigger_level_in[11] = jb_3_stopwatch_stopped;
    assign trigger_level_in[10:0] = 'd0;
/*    assign trigger_level_in[10:4] = 'd0;
    assign trigger_level_in[3] = debug3;
    assign trigger_level_in[2] = debug2;
    assign trigger_level_in[1] = debug1;
    assign trigger_level_in[0] = debug0;
*/    


    /////////////////////////////////////////////////////////////////
    // Output connections from sequencer
    /////////////////////////////////////////////////////////////////
    
    assign jb_4_counter_reset = trigger_out[15];
    assign jb_5_counter_reset = trigger_out[14];
    assign jb_6_counter_reset = trigger_out[13];
    assign jb_7_counter_reset = trigger_out[12];
    
    assign jb_4_stopwatch_start = trigger_out[11];
    assign jb_5_stopwatch_start = trigger_out[10];
    assign jb_6_stopwatch_start = trigger_out[9];
    assign jb_7_stopwatch_start = trigger_out[8];
    assign jb_3_stopwatch_start = trigger_out[7];
    
    assign jb_4_stopwatch_reset = trigger_out[6];
    assign jb_5_stopwatch_reset = trigger_out[5];
    assign jb_6_stopwatch_reset = trigger_out[4];
    assign jb_7_stopwatch_reset = trigger_out[3];
    assign jb_3_stopwatch_reset = trigger_out[2];


    
    assign ja_2 = external_output[15]; // output_ports[0][15] or patterns[17]
    assign ja_3 = external_output[14]; // output_ports[0][14] or patterns[18]
    assign ja_6 = external_output[13]; // output_ports[0][13] or patterns[19]
    assign ja_7 = external_output[12]; // output_ports[0][12] or patterns[20]
    assign jb_0 = external_output[11]; // output_ports[0][11] or patterns[21]
    assign jb_1 = external_output[10]; // output_ports[0][10] or patterns[22]




    wire [15:0] output_ports_1;
    assign output_ports_1 = output_ports[1];
    assign jb_4_counter_clock_enable = output_ports_1[15];
    assign jb_5_counter_clock_enable = output_ports_1[14];
    assign jb_6_counter_clock_enable = output_ports_1[13];
    assign jb_7_counter_clock_enable = output_ports_1[12];

    wire [15:0] output_ports_2;
    assign output_ports_2 = output_ports[2];

    wire [15:0] output_ports_3;
    assign output_ports_3 = output_ports[3];
    
endmodule
