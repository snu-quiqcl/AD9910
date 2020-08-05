`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2018/01/12 17:20:09
// Design Name: 
// Module Name: sequencer
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
//`include "parameterPkg.sv"

import parameterPkg::*;


parameter cmd_nop = 'h00; 

parameter cmd_add = 'h02;
parameter cmd_addi = 'h03;
parameter cmd_sub = 'h04;
parameter cmd_subi = 'h05;

parameter cmd_loadi = 'h06;
parameter cmd_read = 'h07;
parameter cmd_set = 'h08;
parameter cmd_write = 'h09;

parameter cmd_branch_if_less_than = 'h0a;
parameter cmd_branch_if_less_than_imm = 'h0b;
parameter cmd_branch_if_equal = 'h0c;
parameter cmd_branch_if_equal_imm = 'h0d;

parameter cmd_jump = 'h0e;
parameter cmd_stop = 'h0f;

parameter cmd_load_word = 'h11; 
parameter cmd_store_word = 'h12; 
parameter cmd_trigger_out = 'h13;

parameter cmd_wait = 'h14;
parameter cmd_waiti = 'h15;

module sequencer(
    input [15:0] trigger_level_in,
    input clk,
    input start,
    output stopped,
    output fifo_we,
    output [INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] pc,
    output [REGISTER_WIDTH-1:0] rd1, rd2, rd3,
    output [15:0] output_ports[OUTPUT_PORT_NUMBER-1:0],
    output [15:0] trigger_out,
    input [INSTRUCTION_MEMORY_DATA_WIDTH-1:0] instr,
    input [15:0] counters_13_0[13:0]
    );
    wire [15:0] remaining_counts;
    wire PC_clk_enable, reset_PC;
    wire rdA_lt_rdB;
    wire rdA_eq_rdB;
    wire [1:0] run_jump_wait, ALU_src, write_source;
    wire reg_write, ALU_control, update_masked_pattern, pulse_enable, mem_write;
    
    assign stopped = ~PC_clk_enable;
    controller c(.clk(clk), .start(start), .trigger_level_in(trigger_level_in), .remaining_counts(remaining_counts), 
        .PC_clk_enable(PC_clk_enable), .reset_PC(reset_PC), .opcode(instr[63:56]), .imm3(instr[47:32]), .imm1(instr[31:16]), .imm2(instr[15:0]), 
        .rd1(rd1), .rdA_lt_rdB(rdA_lt_rdB), .rdA_eq_rdB(rdA_eq_rdB), .run_jump_wait(run_jump_wait), .write_source(write_source),
        .reg_write(reg_write), .ALU_control(ALU_control), .ALU_src(ALU_src), .fifo_we(fifo_we), .update_masked_pattern(update_masked_pattern),
        .pulse_enable(pulse_enable), .mem_write(mem_write)
    );


    wire [15:0] sixteen_counters[15:0];
    wire [15:0] counters14, counters15;
    assign counters14 = trigger_level_in;
    assign counters15 = remaining_counts;
    assign sixteen_counters = {counters15, counters14, counters_13_0};

    
    datapath dp(.clk(clk), .instr(instr), .counters(sixteen_counters), .PC_clk_enable(PC_clk_enable), .reset_PC(reset_PC), .run_jump_wait(run_jump_wait),
        .write_source(write_source), .reg_write(reg_write), .ALU_control(ALU_control), .ALU_src(ALU_src), .update_masked_pattern(update_masked_pattern),
        .rdA_lt_rdB(rdA_lt_rdB), .rdA_eq_rdB(rdA_eq_rdB), .pc(pc), .rd1(rd1), .rd2(rd2), .rd3(rd3), .output_ports(output_ports), .trigger_out(trigger_out),
        .pulse_enable(pulse_enable), .mem_write(mem_write)
    );
endmodule

module flopr #(parameter WIDTH=9)
    (
    input clk, reset,
    input [WIDTH-1:0] d,
    output reg [WIDTH-1:0] q
    );
    always@(posedge clk, posedge reset)
        if (reset) q <= 0;
        else       q <= d;    
endmodule

module mux4 #(parameter WIDTH=16)
    (
    input [WIDTH-1:0] d0, d1, d2, d3,
    input [1:0] select,
    output logic [WIDTH-1:0] y
    );
    always_comb
        case(select)
            0: y=d0;
            1: y=d1;
            2: y=d2;
            3: y=d3;
        endcase
endmodule

module mux16 #(parameter WIDTH=16)
    (
    input [WIDTH-1:0] din[15:0],
    input [3:0] select,
    output [WIDTH-1:0] y
    );
    assign y = din[select];
endmodule

module compare_only_masked_bits(
    input [15:0] d1, d2,
    input [15:0] mask,
    output d1_eq_d2_for_all_masked_bits
    );
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Trigger of masked bit pattern
    // First collect bits where d1 and d2 are different: (d1 ^ d2)
    // Then collect only bits which are marked important. I.e. masked bits: (d1 ^ d2) & mask
    // If any of the final bits are 1, the required pattern is not matched.
    // If all masks are 0, it is considered not matched.
    assign d1_eq_d2_for_all_masked_bits = (mask == 'd0) ? 1'b0 : ~(|((d1 ^ d2) & mask));
endmodule

module ALU(
    input [REGISTER_WIDTH-1:0] rdA, rdB, mask,
    input ALU_control,
    output [REGISTER_WIDTH-1:0] ALU_out,
    output rdA_lt_rdB,
    output rdA_eq_rdB
    );
    assign ALU_out = (ALU_control == 1'b0) ? (rdA+rdB) : (rdA-rdB);
    assign rdA_lt_rdB = (rdA < rdB) ? 1'b1 : 1'b0;
    compare_only_masked_bits compare_only_masked_bits(.d1(rdA), .d2(rdB), .mask(mask), .d1_eq_d2_for_all_masked_bits(rdA_eq_rdB));

endmodule


module output_masked_pattern(
    input clk, we,
    input [OUTPUT_PORT_ADDR_WIDTH-1:0] addr,
    input [15:0] data, mask,
    output reg [15:0] output_ports [OUTPUT_PORT_NUMBER-1:0]
    );
    genvar i;
    generate
    for (i=0; i<OUTPUT_PORT_NUMBER; i=i+1) begin
        initial output_ports[i] <= 'd0;
    end
    endgenerate
    
    always@(posedge clk)
        if (we) output_ports[addr] <= (~mask & output_ports[addr]) | (mask & data);
endmodule

module datapath(
    input clk,
    input [INSTRUCTION_MEMORY_DATA_WIDTH-1:0] instr,
    input [15:0] counters[15:0],
    input PC_clk_enable,
    input reset_PC,
    input [1:0] run_jump_wait, ALU_src, write_source,
    input reg_write, ALU_control, update_masked_pattern,
    output rdA_lt_rdB,
    output rdA_eq_rdB,
    output [INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] pc,
    output [REGISTER_WIDTH-1:0] rd1, rd2, rd3,
    output [15:0] output_ports [OUTPUT_PORT_NUMBER-1:0], 
    output [15:0] trigger_out,
    input pulse_enable, mem_write
    );
    
    wire [7:0] r1, r2, r3;
    assign r1 = instr[55:48];
    assign r2 = instr[47:40];
    assign r3 = instr[39:32];
    
    wire [15:0] imm3, imm1, imm2;
    assign imm3 = instr[47:32];
    assign imm1 = instr[31:16];
    assign imm2 = instr[15:0];

    wire [15:0] result_MUX_output;

    regfile rf(.clk(clk), .we3(reg_write), .a1(r1[REGISTER_ADDR_WIDTH-1:0]), .a2(r2[REGISTER_ADDR_WIDTH-1:0]), .a3(r3[REGISTER_ADDR_WIDTH-1:0]),
        .wd3(result_MUX_output), .rd1(rd1), .rd2(rd2), .rd3(rd3)
        );
    
    wire [INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] next_pc;
    wire [INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] pc_jump, pc_run;
    wire [INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] internal_pc;
    assign pc_run = (internal_pc + 'd1);
    assign pc_jump = imm2;

    assign pc = internal_pc;
    
    flopr #(9) PC(.clk(clk & PC_clk_enable), .reset(reset_PC), .d(next_pc), .q(internal_pc));

    mux4 #(INSTRUCTION_MEMORY_ADDR_WIDTH) PC_MUX(.d0(pc_run), .d1(pc_jump),.d2(internal_pc), .d3('d0), .select(run_jump_wait), .y(next_pc));

    wire [REGISTER_WIDTH-1:0] rdB, ALU_out;
    
    mux4 #(16) ALU_rdB_source(.d0(rd2), .d1(imm1), .d2(imm3), .d3('d0), .select(ALU_src), .y(rdB));
    ALU alu(.rdA(rd1), .rdB(rdB), .mask(imm1), .ALU_control(ALU_control), .ALU_out(ALU_out), .rdA_lt_rdB(rdA_lt_rdB), .rdA_eq_rdB(rdA_eq_rdB));
    
    parameter DATA_MEMORY_DATA_WIDTH = 16;
    parameter DATA_MEMORY_ADDR_WIDTH = 10;    
    wire [DATA_MEMORY_DATA_WIDTH-1:0] dm_d_out;
    wire [15:0] counter_MUX_output;
    
    mux4 #(16) result_MUX(.d0(counter_MUX_output), .d1(ALU_out), .d2(imm1), .d3(dm_d_out), .select(write_source), .y(result_MUX_output));

    mux16 #(16) counter_MUX(.din(counters), .select(imm1[3:0]), .y(counter_MUX_output));
    
    
    output_masked_pattern omp(.clk(clk), .addr(r3[OUTPUT_PORT_ADDR_WIDTH-1:0]), .we(update_masked_pattern), .data(imm1), .mask(imm2), .output_ports(output_ports));

    assign trigger_out = (pulse_enable) ? imm1 : 'd0;

    data_memory dm( .clk(clk), .we(mem_write), .addr(rd1[DATA_MEMORY_ADDR_WIDTH -1:0]), .d_in(rd3), .d_out(dm_d_out));


    
endmodule



module controller(
    input clk,
    input start,
    input [15:0] trigger_level_in,
    output reg PC_clk_enable, reset_PC,
    output [15:0] remaining_counts,
    input [7:0] opcode,
    input [15:0] imm3,
    input [15:0] imm1,
    input [15:0] imm2,
    input [REGISTER_WIDTH-1:0] rd1,
    input rdA_lt_rdB,
    input rdA_eq_rdB,
    output [1:0] run_jump_wait, write_source,
    output reg_write, ALU_control, 
    output [1:0] ALU_src,
    output fifo_we, update_masked_pattern, pulse_enable, mem_write
    );
    
    wire sequencer_active, internal_fifo_we, internal_update_masked_pattern, internal_pulse_enable, internal_mem_write, internal_reg_write;
    assign sequencer_active = PC_clk_enable & ~reset_PC;

    assign fifo_we = sequencer_active & internal_fifo_we;
    assign update_masked_pattern = sequencer_active & internal_update_masked_pattern;
    assign pulse_enable = sequencer_active & internal_pulse_enable; 
    assign mem_write = sequencer_active & internal_mem_write;
    assign reg_write = sequencer_active & internal_reg_write;

    assign internal_fifo_we = (opcode == cmd_write) ? 1'b1 : 1'b0;
    assign internal_update_masked_pattern = (opcode == cmd_set) ? 1'b1 : 1'b0;
    assign internal_pulse_enable = (opcode == cmd_trigger_out) ? 1'b1 : 1'b0;
    assign internal_mem_write = (opcode == cmd_store_word) ? 1'b1 : 1'b0;
    
    wire [1:0] internal_run_jump_wait;
    logic [7:0] controls;
    assign {internal_run_jump_wait[1:0], internal_reg_write, ALU_control, ALU_src[1:0], write_source[1:0]} = controls;
    
    always_comb
        case(opcode)
            cmd_nop:        controls = 8'b00000000;
            cmd_add:        controls = 8'b00100001;
            cmd_addi:       controls = 8'b00100101;
            cmd_sub:        controls = 8'b00110001;
            cmd_subi:       controls = 8'b00110101;
            cmd_loadi:      controls = 8'b00100010;
            cmd_read:       controls = 8'b00100000;
            cmd_set:        controls = 8'b00000000;
            cmd_write:      controls = 8'b00000000;
            cmd_branch_if_less_than: 
                if (rdA_lt_rdB == 1'b1) controls = 8'b01000000;
                else controls = 8'b00000000;
            cmd_branch_if_less_than_imm: 
                if (rdA_lt_rdB == 1'b1) controls = 8'b01001000;
                else controls = 8'b00001000;
            cmd_branch_if_equal:
                if (rdA_eq_rdB == 1'b1) controls = 8'b01000000;
                else controls = 8'b00000000;
            cmd_branch_if_equal_imm:
                if (rdA_eq_rdB == 1'b1) controls = 8'b01001000;
                else controls = 8'b00001000;
            cmd_jump:       controls = 8'b01000000;
            cmd_stop:       controls = 8'b10000000;
            cmd_load_word:  controls = 8'b00100011;
            cmd_store_word: controls = 8'b00000000; 
            cmd_trigger_out:controls = 8'b00000000;
            cmd_wait:       controls = 8'b10000000;
            cmd_waiti:      controls = 8'b10000000;
            default:        controls = 8'bxxxxxxxx; // illegal opcode
        endcase

        
    wire pattern_matched;
    compare_only_masked_bits trigger_match(.d1(trigger_level_in), .d2(imm1), .mask(imm2), .d1_eq_d2_for_all_masked_bits(pattern_matched));

    
    parameter SEQ_IDLE = 'd0;
    parameter SEQ_RUN = 'd1;
    parameter SEQ_WAIT = 'd2;
    parameter SEQ_RETURN_TO_RUN = 'd3;
    reg [1:0] seq_state;
    reg force_run;
    assign run_jump_wait = (force_run) ? 2'b00 : internal_run_jump_wait[1:0];
    reg [REGISTER_WIDTH-1:0] wait_counter;
    assign remaining_counts = wait_counter;
    initial begin
        seq_state <= SEQ_IDLE;
        force_run <= 1'b0;
        reset_PC <= 1'b0;
        PC_clk_enable <= 1'b0;
        wait_counter <= 'd0;
    end
    
    always@(posedge clk)
        case(seq_state)
            SEQ_IDLE: begin
                    force_run <= 1'b0;
                    if (start == 1'b1) begin
                        seq_state <= SEQ_RUN;
                        reset_PC <= 1'b1;
                        PC_clk_enable <= 1'b1;
                    end
                end
            SEQ_RUN: begin
                    force_run <= 1'b0;
                    reset_PC <= 1'b0;
                    if (opcode == cmd_stop) begin
                        PC_clk_enable <= 1'b0;
                        seq_state <= SEQ_IDLE;
                    end
                    else if (opcode == cmd_wait) begin
                        wait_counter <= rd1;
                        seq_state <= SEQ_WAIT;
                    end
                    else if (opcode == cmd_waiti) begin
                        wait_counter <= imm3;
                        seq_state <= SEQ_WAIT;
                    end
                end
            SEQ_WAIT: begin
                    if (wait_counter == 'd0) begin
                        force_run <= 1'b1;
                        seq_state <= SEQ_RETURN_TO_RUN;
                    end
                    else if (pattern_matched == 1'b1) begin
                        force_run <= 1'b1;
                        seq_state <= SEQ_RETURN_TO_RUN;
                    end
                    else begin
                        wait_counter <= wait_counter - 'd1;
                    end
                end
    
            SEQ_RETURN_TO_RUN: begin
                    force_run <= 1'b0;
                    seq_state <= SEQ_RUN;
                end
               
            default: seq_state <= SEQ_IDLE;
        endcase
                    
                    
endmodule    
    
// Modified from HDL Example 7.6 of "Digital Design and Computer Architecture" 2nd ed.
module regfile(
    input clk,
    input we3,
    input [REGISTER_ADDR_WIDTH-1:0] a1, a2, a3,
    input [REGISTER_WIDTH-1:0] wd3,
    output [REGISTER_WIDTH-1:0] rd1, rd2, rd3
    );
    reg [REGISTER_WIDTH-1:0] rf[(1<<REGISTER_ADDR_WIDTH)-1:0];
    
    
    always@(posedge clk)
        if (we3) rf[a3] <= wd3;
        
    assign rd1 = rf[a1];
    assign rd2 = rf[a2];
    assign rd3 = rf[a3];
endmodule

