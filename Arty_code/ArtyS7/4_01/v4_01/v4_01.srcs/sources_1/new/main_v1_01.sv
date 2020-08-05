`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2017/11/23 20:28:05
// Design Name: 
// Module Name: main
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
//  The FILE_TYPE of this file is set to SystemVerilog to utilize SystemVerilog features.
//  Generally to apply SystemVerilog syntax, the file extension should be ".sv" rather than ".v"
//  If you want to choose between verilog2001 and SystemVerilog without changing the file extension, 
//  right-click on the file name in "Design Sources", choose "Source Node Properties...", and 
//  change FILE_TYPE in Properties tab.
//////////////////////////////////////////////////////////////////////////////////

//`include "parameterPkg.sv"

import parameterPkg::*;

module main(
    input Uart_RXD,
    output Uart_TXD,
    input CLK100MHZ,
    input BTN0,
    input BTN1,
    input BTN2,
    output ja_3,
    output ja_7,
    output jb_1,
    output jb_3,
    output jb_5,
    output jb_7,
    output ja_0, ja_1, ja_4, ja_5, ja_6,
    input jb_0,
    input jb_2,
    input jb_4,
    input jb_6,
    input ja_2,
    output [5:2] led,
    output led0_r,
    output led0_g,
    output led0_b,
    output led1_r,
    output led1_g,
    output led1_b,
    output d5, d4, d3, d2, d1, d0 // For debugging purpose    
    );
    function integer bits_to_represent; //https://www.beyond-circuits.com/wordpress/2008/11/constant-functions/
        input integer value;
        begin
            for (bits_to_represent=0; value>0; bits_to_represent=bits_to_represent+1)
                value = value>>1;
        end
    endfunction

    /////////////////////////////////////////////////////////////////
    // UART setting
    /////////////////////////////////////////////////////////////////
    parameter ClkFreq = 100000000;	// make sure this matches the clock frequency on your board
    parameter BaudRate = 57600;    // Baud rate

    wire [BTF_RX_BUFFER_WIDTH:1] BTF_Buffer;
    wire [BTF_RX_BUFFER_COUNT_WIDTH-1:0] BTF_Length;
    
    wire [CMD_RX_BUFFER_WIDTH:1] CMD_Buffer;
    wire [3:0] CMD_Length;    
    wire CMD_Ready;
    
    wire esc_char_detected;
    wire [7:0] esc_char;

    wire wrong_format;
        
    // Settings related to capture waveform data
    //wire [WAVEFORM_WIDTH-1:0] trigger_mask, trigger_pattern;
    //wire [WAVEFORM_COUNTER_WIDTH-1:0] points_to_capture_after_trigger;
    
    data_receiver receiver(.RxD(Uart_RXD), .clk(CLK100MHZ), 
        .BTF_Buffer(BTF_Buffer), .BTF_Length(BTF_Length), 
        .CMD_Buffer(CMD_Buffer), .CMD_Length(CMD_Length), .CMD_Ready(CMD_Ready), 
        .esc_char_detected(esc_char_detected), .esc_char(esc_char),
        // Settings related to capture waveform data
        //.trigger_mask(trigger_mask), .trigger_pattern(trigger_pattern), .points_to_capture_after_trigger(points_to_capture_after_trigger),
         .wrong_format(wrong_format)
    );
    defparam receiver.ClkFreq = ClkFreq;
    defparam receiver.BaudRate = BaudRate;

    /////////////////////////////////////////////////////////////////
    // To send data to PC
    /////////////////////////////////////////////////////////////////


    reg [TX_BUFFER1_LENGTH_WIDTH-1:0] TX_buffer1_length;
    reg [1:TX_BUFFER1_WIDTH] TX_buffer1;
    reg TX_buffer1_ready;

    reg [TX_BUFFER2_LENGTH_WIDTH-1:0] TX_buffer2_length;
    reg [1:TX_BUFFER2_WIDTH] TX_buffer2;
    reg TX_buffer2_ready;

    reg [OUTPUT_FIFO_DATA_COUNT_WIDTH-1:0] TX_port3_data_length;
    reg TX_port3_ready;
    wire data_fifo_rd_en;
    wire [OUTPUT_FIFO_DATA_WIDTH-1:0] data_fifo_dout;

    // Settings related to capture waveform data
    //wire [1:TX_WAVEFORM_BUFFER_WIDTH] TX_waveform_buffer;
    //wire TX_waveform_buffer_ready;
    //wire cwd_armed, cwd_triggered;
    
    wire TX_FIFO_ready;
    
    wire [1:32] monitoring_32bits;

    data_sender sender(
    .FSMState(),
    .clk(CLK100MHZ),
    .TxD(Uart_TXD),
    .esc_char_detected(esc_char_detected),
    .esc_char(esc_char),
    .wrong_format(wrong_format),
    .TX_buffer1_length(TX_buffer1_length),
    .TX_buffer1(TX_buffer1),
    .TX_buffer1_ready(TX_buffer1_ready),
    .TX_buffer2_length(TX_buffer2_length),
    .TX_buffer2(TX_buffer2),
    .TX_buffer2_ready(TX_buffer2_ready),
    .TX_port3_data_length(TX_port3_data_length),
    .TX_port3_ready(TX_port3_ready),
    .data_fifo_rd_en(data_fifo_rd_en),
    .data_fifo_dout(data_fifo_dout),
    // Settings related to capture waveform data
    //.TX_waveform_buffer(TX_waveform_buffer),
    //.TX_waveform_buffer_ready(TX_waveform_buffer_ready),
    //.capture_waveform_data_implemented(1'b1), // 1'b1 if capture_waveform_data is available
    //.armed(cwd_armed),
    //.triggered(cwd_triggered),
    .TX_FIFO_ready(TX_FIFO_ready),
    .bits_to_send(monitoring_32bits)
);

    defparam sender.ClkFreq = ClkFreq;
    defparam sender.BaudRate = BaudRate;

    /////////////////////////////////////////////////////////////////
    // Capture waveform data
    /////////////////////////////////////////////////////////////////
    // Settings related to capture waveform data
/*
    reg waveform_capture_start_trigger;
    initial waveform_capture_start_trigger <= 1'b0;

    wire [WAVEFORM_WIDTH-1:0] waveform_data;

    capture_waveform_data cwd(
        .CLK100MHZ(CLK100MHZ),
        .waveform(waveform_data),
        .armed(cwd_armed),
        .triggered(cwd_triggered),
        .arm_signal(waveform_capture_start_trigger),
        .trigger_mask(trigger_mask),
        .trigger_pattern(trigger_pattern),
        .points_to_capture_after_trigger(points_to_capture_after_trigger),
        .TX_FIFO_ready(TX_FIFO_ready),
        .TX_BUFFER(TX_waveform_buffer),
        .TX_waveform_buffer_ready(TX_waveform_buffer_ready),
        .esc_char_detected(esc_char_detected),
        .esc_char(esc_char)
    );
    defparam cwd.TX_WAVEFORM_BUFFER_BYTES =  TX_WAVEFORM_BUFFER_BYTES;
    defparam cwd.TX_WAVEFORM_BUFFER_WIDTH = TX_WAVEFORM_BUFFER_WIDTH;
    defparam cwd.WAVEFORM_WIDTH = WAVEFORM_WIDTH;
    defparam cwd.WAVEFORM_MAX_DEPTH = WAVEFORM_MAX_DEPTH;
    defparam cwd.WAVEFORM_COUNTER_WIDTH = WAVEFORM_COUNTER_WIDTH;
*/


    /////////////////////////////////////////////////////////////////
    // Sequencer instruction memory
    /////////////////////////////////////////////////////////////////
    reg instruction_memory_we;
    reg [INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] instruction_memory_address;
    reg [INSTRUCTION_MEMORY_DATA_WIDTH-1:0] instruction_memory_data_in;
    wire [INSTRUCTION_MEMORY_DATA_WIDTH-1:0] instruction_memory_data_out;
    wire [INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] PC;
    wire [INSTRUCTION_MEMORY_DATA_WIDTH-1:0] instr;

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
    wire [15:0] output_ports [OUTPUT_PORT_NUMBER-1:0];
    wire [15:0] trigger_out;
/////////////////////////////////////////////////////////////////    
    reg start_sequencer;
    wire stopped;
    wire [15:0] counters_13_0[13:0];
    wire [REGISTER_WIDTH-1:0] rd1, rd2, rd3;
    wire output_fifo_we; 
/////////////////////////////////////////////////////////////////    

    sequencer seq(.trigger_level_in(trigger_level_in), .clk(CLK100MHZ), .start(start_sequencer), .stopped(stopped), .pc(PC),
        .fifo_we(output_fifo_we), .rd1(rd1), .rd2(rd2), .rd3(rd3), .output_ports(output_ports), .trigger_out(trigger_out), .instr(instr), .counters_13_0(counters_13_0)
    );

    wire [OUTPUT_FIFO_DATA_COUNT_WIDTH-1:0] output_fifo_data_count;

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


    /////////////////////////////////////////////////////////////////
    // LED0 & LED1 intensity adjustment
    /////////////////////////////////////////////////////////////////

    reg [7:0] LED_intensity;
    wire red0, green0, blue0, red1, green1, blue1;
    initial begin
        LED_intensity <= 0;
    end
    
    led_intensity_adjust led_intensity_modulator(.led0_r(led0_r), .led0_g(led0_g), .led0_b(led0_b), .led1_r(led1_r), 
        .led1_g(led1_g), .led1_b(led1_b), .red0(red0), .green0(green0), .blue0(blue0), .red1(red1), .green1(green1), .blue1(blue1),
        .intensity(LED_intensity), .CLK100MHZ(CLK100MHZ) );

    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Command definitions
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




    /////////////////////////////////////////////////////////////////
    // Command definition for *IDN? command
    /////////////////////////////////////////////////////////////////
    parameter CMD_IDN = "*IDN?";
    parameter IDN_REPLY = "Sequencer v4_01"; // 15 characters



    /////////////////////////////////////////////////////////////////
    // Command definition for DNA_PORT command
    /////////////////////////////////////////////////////////////////
    parameter CMD_DNA_PORT = "*DNA_PORT?";
    wire [63:0] DNA_wire;
    device_DNA device_DNA_inst(
        .clk(CLK100MHZ),
        .DNA(DNA_wire) // If 4 MSBs == 4'h0, DNA_PORT reading is not finished. If 4 MSBs == 4'h1, DNA_PORT reading is done 
    );
    
    /////////////////////////////////////////////////////////////////
    // Command definition for Test command
    /////////////////////////////////////////////////////////////////
    parameter CMD_TEST = {8'h10, "TEST", 8'h10};


    /////////////////////////////////////////////////////////////////
    // Command definition for LED0 & LED1 intensity adjustment
    /////////////////////////////////////////////////////////////////
    parameter CMD_ADJUST_INTENSITY = "ADJ INTENSITY"; // 13 characters
    parameter CMD_READ_INTENSITY = "READ INTENSITY"; // 14 characters


    /////////////////////////////////////////////////////////////////
    // Command definition to investigate the contents in the BTF buffer
    /////////////////////////////////////////////////////////////////
    // Capturing the snapshot of BTF buffer
    parameter CMD_CAPTURE_BTF_BUFFER = "CAPTURE BTF"; // 11 characters
    reg [BTF_RX_BUFFER_WIDTH:1] BTF_capture;
    // Setting the number of bytes to read from the captured BTF buffer
    parameter CMD_SET_BTF_BUFFER_READING_COUNT = "BTF READ COUNT"; // 14 characters
    reg [BTF_RX_BUFFER_COUNT_WIDTH-1:0] BTF_read_count;
    // Read from the captured BTF buffer
    parameter CMD_READ_BTF_BUFFER = "READ BTF"; // 8 characters


/*
    // Settings related to capture waveform data
    /////////////////////////////////////////////////////////////////
    // Command definition to capture waveform data
    /////////////////////////////////////////////////////////////////
    parameter CMD_CAPTURE_WAVEFORM = "WAVEFORM"; // 8 characters

    reg [15:0] temp_counter_16bits;
    
    always @ (posedge CLK100MHZ) begin
        temp_counter_16bits <= temp_counter_16bits + patterns[1:2] + 'd1;
    end
*/

    /////////////////////////////////////////////////////////////////
    // Command definition for bit patterns manipulation
    /////////////////////////////////////////////////////////////////
    // This command uses the first PATTERN_WIDTH bits as mask bits to update and update those bits with the following PATTERN_WIDTH bits
    parameter CMD_UPDATE_BIT_PATTERNS = "UPDATE BITS"; // 11 characters
    parameter PATTERN_BYTES = 4;
    parameter PATTERN_WIDTH = PATTERN_BYTES * 8; 
    reg [1:PATTERN_WIDTH] patterns;
    wire [1:PATTERN_WIDTH] pattern_masks;
    wire [1:PATTERN_WIDTH] pattern_data;
    
    assign pattern_masks = BTF_Buffer[2*PATTERN_WIDTH:PATTERN_WIDTH+1];
    assign pattern_data = BTF_Buffer[PATTERN_WIDTH:1];
    
    // This command reads the 32-bit patterns
    parameter CMD_READ_BIT_PATTERNS = "READ BITS"; // 9 characters


    /////////////////////////////////////////////////////////////////
    // Command definition for Sequencer
    /////////////////////////////////////////////////////////////////
    parameter CMD_START_SEQUENCER   = "START SEQUENCER";    // 15 characters
    parameter CMD_MANUAL_MODE       = "MANUAL MODE";        // 11 characters
    parameter CMD_AUTO_MODE         = "AUTO MODE";          // 9 characters
    parameter CMD_LOAD_PROG         = "LOAD PROG";          // 9 characters
    parameter CMD_READ_PROG         = "READ PROG";          // 9 characters
    parameter CMD_READ_FIFO_DATA_LENGTH  = "DATA LENGTH";   // 11 characters
    parameter CMD_READ_FIFO_DATA    = "READ DATA";          // 9 characters
    

    reg manual_control_on;
    initial begin
        manual_control_on <= 1'b1;
        start_sequencer <= 1'b0;
    end


    /////////////////////////////////////////////////////////////////
    // Main FSM
    /////////////////////////////////////////////////////////////////
	reg [3:0] main_state;
    // State definition of FSM
    // Common state
    parameter MAIN_IDLE = 4'h0;    

    // Settings related to capture waveform data
    //parameter MAIN_CAPTURE_WAVEFORM_END = 4'h5;

    parameter MAIN_START_SEQ = 4'h1;  
    parameter MAIN_LOAD_PROG = 4'h2;
    parameter MAIN_READ_PROG = 4'h3;

    parameter MAIN_UNKNOWN_CMD =4'h8;
    

    initial begin
        main_state <= MAIN_IDLE;
        patterns <= 'd0;
        TX_buffer1_ready <= 1'b0;
        TX_buffer2_ready <= 1'b0;
        TX_port3_ready <= 1'b0;
    end
    
    always @ (posedge CLK100MHZ)
        if (esc_char_detected == 1'b1) begin
            if (esc_char == "C") begin
                TX_buffer1_ready <= 1'b0;
                TX_buffer2_ready <= 1'b0;
                TX_port3_ready <= 1'b0;
                main_state <= MAIN_IDLE;
            end
        end
        else begin
            case (main_state)
                MAIN_IDLE:
                    if (CMD_Ready == 1'b1) begin

                        if ((CMD_Length == $bits(CMD_IDN)/8) && (CMD_Buffer[$bits(CMD_IDN):1] == CMD_IDN)) begin
                            TX_buffer1[1:$bits(IDN_REPLY)] <= IDN_REPLY;
                            TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= $bits(IDN_REPLY)/8;
                            TX_buffer1_ready <= 1'b1;
                        end

                        else if ((CMD_Length == $bits(CMD_DNA_PORT)/8) && (CMD_Buffer[$bits(CMD_DNA_PORT):1] == CMD_DNA_PORT)) begin
                            TX_buffer1[1:64] <= DNA_wire;
                            TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= 8;
                            TX_buffer1_ready <= 1'b1;
                            main_state <= MAIN_IDLE;
                        end

                        else if ((CMD_Length == $bits(CMD_TEST)/8) && (CMD_Buffer[$bits(CMD_TEST):1] == CMD_TEST)) begin
                            TX_buffer1[1:10*8] <= "Test rec'd";
                            TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= 'd10;
                            TX_buffer1_ready <= 1'b1;
                        end

                        else if ((CMD_Length == $bits(CMD_ADJUST_INTENSITY)/8) && (CMD_Buffer[$bits(CMD_ADJUST_INTENSITY):1] == CMD_ADJUST_INTENSITY)) begin
                            LED_intensity[7:0] <= BTF_Buffer[8:1];
                        end

                        else if ((CMD_Length == $bits(CMD_READ_INTENSITY)/8) && (CMD_Buffer[$bits(CMD_READ_INTENSITY):1] == CMD_READ_INTENSITY)) begin
                            TX_buffer1[1:8] <= LED_intensity;
                            TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= 'd1;
                            TX_buffer1_ready <= 1'b1;
                            main_state <= MAIN_IDLE;
                        end

                        else if ((CMD_Length == $bits(CMD_CAPTURE_BTF_BUFFER)/8) && (CMD_Buffer[$bits(CMD_CAPTURE_BTF_BUFFER):1] == CMD_CAPTURE_BTF_BUFFER)) begin
                            BTF_capture[BTF_RX_BUFFER_WIDTH:1] <= BTF_Buffer[BTF_RX_BUFFER_WIDTH:1];
                            main_state <= MAIN_IDLE;
                        end


                        else if ((CMD_Length == $bits(CMD_SET_BTF_BUFFER_READING_COUNT)/8) && (CMD_Buffer[$bits(CMD_SET_BTF_BUFFER_READING_COUNT):1] == CMD_SET_BTF_BUFFER_READING_COUNT)) begin
                            BTF_read_count[BTF_RX_BUFFER_COUNT_WIDTH-1:0] <= BTF_Buffer[BTF_RX_BUFFER_COUNT_WIDTH:1];
                            main_state <= MAIN_IDLE;
                        end

                        else if ((CMD_Length == $bits(CMD_READ_BTF_BUFFER)/8) && (CMD_Buffer[$bits(CMD_READ_BTF_BUFFER):1] == CMD_READ_BTF_BUFFER)) begin
                            TX_buffer2[1:TX_BUFFER2_WIDTH] <= BTF_capture[BTF_RX_BUFFER_WIDTH:1];
                            TX_buffer2_length[TX_BUFFER2_LENGTH_WIDTH-1:0] <= BTF_read_count[BTF_RX_BUFFER_COUNT_WIDTH-1:0];
                            TX_buffer2_ready <= 1'b1;
                            main_state <= MAIN_IDLE;
                        end

                        else if ((CMD_Length == $bits(CMD_UPDATE_BIT_PATTERNS)/8) && (CMD_Buffer[$bits(CMD_UPDATE_BIT_PATTERNS):1] == CMD_UPDATE_BIT_PATTERNS)) begin
                            patterns <= (patterns & ~pattern_masks) | (pattern_masks & pattern_data);
                        end

                        else if ((CMD_Length == $bits(CMD_READ_BIT_PATTERNS)/8) && (CMD_Buffer[$bits(CMD_READ_BIT_PATTERNS):1] == CMD_READ_BIT_PATTERNS)) begin
                            TX_buffer1[1:PATTERN_WIDTH] <= patterns;
                            TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= PATTERN_WIDTH/8;
                            TX_buffer1_ready <= 1'b1;
                            main_state <= MAIN_IDLE;
                        end

/*                      // Settings related to capture waveform data
                        else if ((CMD_Length == $bits(CMD_CAPTURE_WAVEFORM)/8) && (CMD_Buffer[$bits(CMD_CAPTURE_WAVEFORM):1] == CMD_CAPTURE_WAVEFORM)) begin
                            waveform_capture_start_trigger <= 1'b1;
                            main_state <= MAIN_CAPTURE_WAVEFORM_END;
                        end
*/
                        else if ((CMD_Length == $bits(CMD_MANUAL_MODE)/8) && (CMD_Buffer[$bits(CMD_MANUAL_MODE):1] == CMD_MANUAL_MODE)) begin
                            manual_control_on <= 1'b1;
                        end
                        else if ((CMD_Length == $bits(CMD_AUTO_MODE)/8) && (CMD_Buffer[$bits(CMD_AUTO_MODE):1] == CMD_AUTO_MODE)) begin
                            manual_control_on <= 1'b0;
                        end
                        else if ((CMD_Length == $bits(CMD_START_SEQUENCER)/8) && (CMD_Buffer[$bits(CMD_START_SEQUENCER):1] == CMD_START_SEQUENCER)) begin
                            start_sequencer <= 1'b1;
                             main_state <= MAIN_START_SEQ;
                        end
                        else if ((CMD_Length == $bits(CMD_LOAD_PROG)/8) && (CMD_Buffer[$bits(CMD_LOAD_PROG):1] == CMD_LOAD_PROG)) begin
                            instruction_memory_address[INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] <= BTF_Buffer[INSTRUCTION_MEMORY_DATA_WIDTH+INSTRUCTION_MEMORY_ADDR_WIDTH:INSTRUCTION_MEMORY_DATA_WIDTH+1];
                            instruction_memory_data_in[INSTRUCTION_MEMORY_DATA_WIDTH-1:0] <= BTF_Buffer[INSTRUCTION_MEMORY_DATA_WIDTH:1];
                            instruction_memory_we <= 1'b1;
                            main_state <= MAIN_LOAD_PROG;
                        end

                        else if ((CMD_Length == $bits(CMD_READ_PROG)/8) && (CMD_Buffer[$bits(CMD_READ_PROG):1] == CMD_READ_PROG)) begin
                            instruction_memory_address[INSTRUCTION_MEMORY_ADDR_WIDTH-1:0] <= BTF_Buffer[INSTRUCTION_MEMORY_ADDR_WIDTH:1];
                            main_state <= MAIN_READ_PROG;
                        end

                        else if ((CMD_Length == $bits(CMD_READ_FIFO_DATA_LENGTH)/8) && (CMD_Buffer[$bits(CMD_READ_FIFO_DATA_LENGTH):1] == CMD_READ_FIFO_DATA_LENGTH)) begin
                            TX_buffer2[1:16] <= {{(16-OUTPUT_FIFO_DATA_COUNT_WIDTH){1'b0}},output_fifo_data_count}; 
                            TX_buffer2_length[TX_BUFFER2_LENGTH_WIDTH-1:0] <= 16/8;
                            TX_buffer2_ready <= 1'b1;
                            main_state <= MAIN_IDLE;
                        end


                        else if ((CMD_Length == $bits(CMD_READ_FIFO_DATA)/8) && (CMD_Buffer[$bits(CMD_READ_FIFO_DATA):1] == CMD_READ_FIFO_DATA)) begin
                            if (output_fifo_data_count > MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE) begin 
                                if (BTF_Buffer[OUTPUT_FIFO_DATA_COUNT_WIDTH:1] > MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE) // The maximum number of data to read at once => corresponding to 4096 bytes requiring 13 bits 
                                    TX_port3_data_length <= MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE;
                                else
                                    TX_port3_data_length <= BTF_Buffer[OUTPUT_FIFO_DATA_COUNT_WIDTH:1];
                            end
                            else begin
                                if (BTF_Buffer[OUTPUT_FIFO_DATA_COUNT_WIDTH:1] > output_fifo_data_count) 
                                    TX_port3_data_length <= output_fifo_data_count;
                                else
                                    TX_port3_data_length <= BTF_Buffer[OUTPUT_FIFO_DATA_COUNT_WIDTH:1];
                            end
                            TX_port3_ready <= 1'b1;
                            main_state <= MAIN_IDLE;
                        end 
                        
                        else begin
                            main_state <= MAIN_UNKNOWN_CMD;
                        end
                    end
                    else begin
                        TX_buffer1_ready <= 1'b0;
                        TX_buffer2_ready <= 1'b0;
                        TX_port3_ready <= 1'b0;
                    end
                    

/*              // Settings related to capture waveform data
                MAIN_CAPTURE_WAVEFORM_END: begin
                        waveform_capture_start_trigger <= 1'b0;
                        main_state <= MAIN_IDLE;
                    end
*/
                MAIN_START_SEQ: begin
                        start_sequencer <= 1'b0;
                        main_state <= MAIN_IDLE;
                    end
                    
                MAIN_LOAD_PROG: begin
                        instruction_memory_we <= 1'b0;
                        main_state <= MAIN_IDLE;
                    end

                MAIN_READ_PROG: begin
                        TX_buffer2[1:INSTRUCTION_MEMORY_DATA_WIDTH] <= instruction_memory_data_out[INSTRUCTION_MEMORY_DATA_WIDTH-1:0];
                        TX_buffer2_length[TX_BUFFER2_LENGTH_WIDTH-1:0] <= INSTRUCTION_MEMORY_DATA_WIDTH/8;
                        TX_buffer2_ready <= 1'b1;
                        main_state <= MAIN_IDLE;
                    end
 
                
                MAIN_UNKNOWN_CMD:
                    begin
                        TX_buffer1[1:11*8] <= "Unknown CMD";
                        TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= 'd11;
                        TX_buffer1_ready <= 1'b1;

                        //led1_b <= ~led1_b;
                        main_state <= MAIN_IDLE;
                    end
                    
                default:
                    main_state <= MAIN_IDLE;
            endcase
        end            
                    








	////////////////////////////////////////////////////////////////
	// Detect when BTN0 is pressed
	////////////////////////////////////////////////////////////////
    wire BTN0EdgeDetect;
    reg BTN0Delay;
    initial BTN0Delay = 1'b0;
    always @ (posedge CLK100MHZ) begin
        BTN0Delay <= BTN0;
    end
    assign BTN0EdgeDetect = (BTN0 & !BTN0Delay);



/*
    initial begin
        $display("$bits(CMD_MEASURE_PMT2_INTERVAL)/8=%h, $bits(CMD_MEASURE_PMT2_INTERVAL)=%h\n", $bits(CMD_MEASURE_PMT2_INTERVAL)/8, $bits(CMD_MEASURE_PMT2_INTERVAL));
        $display("'d1 + $ceil(PMT_INTERVAL_COUNTER_LENGTH_WIDTH/8)=%h\n", 'd1 + $ceil(PMT_INTERVAL_COUNTER_LENGTH_WIDTH/8));
        $display("PMT_INTERVAL_COUNTER_LENGTH_WIDTH/8=%h, $ceil(1)=%h, $ceil(1.0)=%h\n", PMT_INTERVAL_COUNTER_LENGTH_WIDTH/8, $ceil(1), $ceil(1.0));
    end
*/

    assign {d0, d1, d2, d3, d4, d5} = 6'h00;
    assign {led, red1, green1, blue1, red0, green0, blue0} = patterns[1:10];
    //assign monitoring_32bits = {patterns[1:31], manual_control_on};

    wire [15:0] external_output;
    mux2 #(16) external_control(.d0(output_ports[0]), .d1(patterns[17:32]), .select(manual_control_on), .y(external_output));

    assign monitoring_32bits = {external_output, stopped, manual_control_on, {(14-INSTRUCTION_MEMORY_ADDR_WIDTH){1'b0}}, PC[INSTRUCTION_MEMORY_ADDR_WIDTH-1:0]};




    /////////////////////////////////////////////////////////////////
    // Counter connections
    /////////////////////////////////////////////////////////////////
    wire jb_0_counter_clock_enable, jb_2_counter_clock_enable, jb_4_counter_clock_enable, jb_6_counter_clock_enable; 
    wire jb_0_counter_reset, jb_2_counter_reset, jb_4_counter_reset, jb_6_counter_reset;
    wire [15:0] jb_0_counter_output, jb_2_counter_output, jb_4_counter_output, jb_6_counter_output;
    
    counter jb_0_counter(.clock(jb_0), .clockEnable(jb_0_counter_clock_enable), .reset(jb_0_counter_reset), .q(jb_0_counter_output) );
    counter jb_2_counter(.clock(jb_2), .clockEnable(jb_2_counter_clock_enable), .reset(jb_2_counter_reset), .q(jb_2_counter_output) );
    counter jb_4_counter(.clock(jb_4), .clockEnable(jb_4_counter_clock_enable), .reset(jb_4_counter_reset), .q(jb_4_counter_output) );
    counter jb_6_counter(.clock(jb_6), .clockEnable(jb_6_counter_clock_enable), .reset(jb_6_counter_reset), .q(jb_6_counter_output) );

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
    wire jb_0_stopwatch_start, jb_2_stopwatch_start, jb_4_stopwatch_start, jb_6_stopwatch_start, ja_2_stopwatch_start;
    wire jb_0_stopwatch_reset, jb_2_stopwatch_reset, jb_4_stopwatch_reset, jb_6_stopwatch_reset, ja_2_stopwatch_reset;
    wire [15:0] jb_0_stopwatch_output, jb_2_stopwatch_output, jb_4_stopwatch_output, jb_6_stopwatch_output, ja_2_stopwatch_output;
    wire jb_0_stopwatch_stopped, jb_2_stopwatch_stopped, jb_4_stopwatch_stopped, jb_6_stopwatch_stopped, ja_2_stopwatch_stopped;
    
    stop_watch jb_0_stopwatch(.clk_800MHz(clk_800MHz_out1), .start(jb_0_stopwatch_start), .stop(jb_0), .reset(jb_0_stopwatch_reset),
    .interval(jb_0_stopwatch_output), .stopped(jb_0_stopwatch_stopped) );

//    wire debug0, debug1, debug2, debug3;
    stop_watch jb_2_stopwatch(.clk_800MHz(clk_800MHz_out2), .start(jb_2_stopwatch_start), .stop(jb_2), .reset(jb_2_stopwatch_reset),
    .interval(jb_2_stopwatch_output), .stopped(jb_2_stopwatch_stopped) );
/*    .interval(jb_2_stopwatch_output), .stopped(jb_2_stopwatch_stopped), 
    .debug_started(debug0),
    .debug_stop_signal_captured_at_start_posedge(debug1),
    .debug_stop_negedge_detected_after_start(debug2),
    .debug_stop_signal_mask(debug3)
    );
*/
    stop_watch jb_4_stopwatch(.clk_800MHz(clk_800MHz_out3), .start(jb_4_stopwatch_start), .stop(jb_4), .reset(jb_4_stopwatch_reset),
    .interval(jb_4_stopwatch_output), .stopped(jb_4_stopwatch_stopped) );

    stop_watch jb_6_stopwatch(.clk_800MHz(clk_800MHz_out4), .start(jb_6_stopwatch_start), .stop(jb_6), .reset(jb_6_stopwatch_reset),
    .interval(jb_6_stopwatch_output), .stopped(jb_6_stopwatch_stopped) );

    stop_watch ja_2_stopwatch(.clk_800MHz(clk_800MHz_out5), .start(ja_2_stopwatch_start), .stop(ja_2), .reset(ja_2_stopwatch_reset),
    .interval(ja_2_stopwatch_output), .stopped(ja_2_stopwatch_stopped) );


    /////////////////////////////////////////////////////////////////
    // Input connections to sequencer
    /////////////////////////////////////////////////////////////////
    
    assign counters_13_0[0] = jb_0_counter_output;
    assign counters_13_0[1] = jb_2_counter_output;
    assign counters_13_0[2] = jb_4_counter_output;
    assign counters_13_0[3] = jb_6_counter_output;
    assign counters_13_0[4] = 'd0;
    assign counters_13_0[5] = 'd0;
    assign counters_13_0[6] = jb_0_stopwatch_output;
    assign counters_13_0[7] = jb_2_stopwatch_output;
    assign counters_13_0[8] = jb_4_stopwatch_output;
    assign counters_13_0[9] = jb_6_stopwatch_output;
    assign counters_13_0[10] = ja_2_stopwatch_output;
    assign counters_13_0[11] = 'd0;
    assign counters_13_0[12] = 'd0;
    assign counters_13_0[13] = patterns[1:16];


    assign trigger_level_in[15] = jb_0_stopwatch_stopped;
    assign trigger_level_in[14] = jb_2_stopwatch_stopped;
    assign trigger_level_in[13] = jb_4_stopwatch_stopped;
    assign trigger_level_in[12] = jb_6_stopwatch_stopped;
    assign trigger_level_in[11] = ja_2_stopwatch_stopped;
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
    
    assign jb_0_counter_reset = trigger_out[15];
    assign jb_2_counter_reset = trigger_out[14];
    assign jb_4_counter_reset = trigger_out[13];
    assign jb_6_counter_reset = trigger_out[12];
    
    assign jb_0_stopwatch_start = trigger_out[11];
    assign jb_2_stopwatch_start = trigger_out[10];
    assign jb_4_stopwatch_start = trigger_out[9];
    assign jb_6_stopwatch_start = trigger_out[8];
    assign ja_2_stopwatch_start = trigger_out[7];
    
    assign jb_0_stopwatch_reset = trigger_out[6];
    assign jb_2_stopwatch_reset = trigger_out[5];
    assign jb_4_stopwatch_reset = trigger_out[4];
    assign jb_6_stopwatch_reset = trigger_out[3];
    assign ja_2_stopwatch_reset = trigger_out[2];


    
    assign ja_3 = external_output[15]; // output_ports[0][15] or patterns[17]
    assign ja_7 = external_output[14]; // output_ports[0][14] or patterns[18]
    assign jb_1 = external_output[13]; // output_ports[0][13] or patterns[19]
    assign jb_3 = external_output[12]; // output_ports[0][12] or patterns[20]
    assign jb_5 = external_output[11]; // output_ports[0][11] or patterns[21]
    assign jb_7 = external_output[10]; // output_ports[0][10] or patterns[22]
    assign ja_0 = external_output[9]; // output_ports[0][9] or patterns[23]
    assign ja_1 = external_output[8]; // output_ports[0][8] or patterns[24]
    assign ja_4 = external_output[7]; // output_ports[0][7] or patterns[25]
    assign ja_5 = external_output[6]; // output_ports[0][6] or patterns[26]
    assign ja_6 = external_output[5]; // output_ports[0][5] or patterns[27]




    wire [15:0] output_ports_1;
    assign output_ports_1 = output_ports[1];
    assign jb_0_counter_clock_enable = output_ports_1[15];
    assign jb_2_counter_clock_enable = output_ports_1[14];
    assign jb_4_counter_clock_enable = output_ports_1[13];
    assign jb_6_counter_clock_enable = output_ports_1[12];

    wire [15:0] output_ports_2;
    assign output_ports_2 = output_ports[2];

    wire [15:0] output_ports_3;
    assign output_ports_3 = output_ports[3];
    // Temporary connection for debugging
    //assign {jb_4_in, jb_3_in} = output_ports_3[15:14];
    
    /*    
    genvar i;
    generate
    for (i=1; i<14; i=i+1) begin
        assign counters_13_0[i] = 16'd0;
    end
    endgenerate
    */

    // Settings related to capture waveform data
    //assign monitoring_32bits = {patterns[1:26], cwd_armed, cwd_triggered, 1'b0, capture_waveform_data_main_state[2:0]};
    //assign waveform_data[15:0] = temp_counter_16bits;

    //assign led[5:2] = main_state[3:0];
 
endmodule
