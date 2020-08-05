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
function integer bits_to_represent; //https://www.beyond-circuits.com/wordpress/2008/11/constant-functions/
    input integer value;
    begin
        for (bits_to_represent=0; value>0; bits_to_represent=bits_to_represent+1)
            value = value>>1;
    end
endfunction


module main_with_capture_waveform_data(
//module main(
    input Uart_RXD,
    output Uart_TXD,
    input CLK100MHZ,
    input BTN0,
    input BTN1,
    input BTN2,
    output ja_2,
    output ja_3,
    output ja_6,
    output ja_7,
    input jb_0,
    input jb_1,
    input jb_2,
    input jb_3,
    input jb_4,
    input jb_5,
    input jb_6,
    input jb_7,
    output [5:2] led,
    output led0_r,
    output led0_g,
    output led0_b,
    output led1_r,
    output led1_g,
    output led1_b,
    output d5, d4, d3, d2, d1, d0 // For debugging purpose    
    );
    
    
    /////////////////////////////////////////////////////////////////
    // UART setting
    /////////////////////////////////////////////////////////////////
    parameter ClkFreq = 100000000;	// make sure this matches the clock frequency on your board
    parameter BaudRate = 57600;    // Baud rate

    /////////////////////////////////////////////////////////////////
    // Global setting
    /////////////////////////////////////////////////////////////////
    parameter BTF_MAX_BYTES = 9'h100;
    parameter BTF_MAX_BUFFER_WIDTH = 8 * BTF_MAX_BYTES;
    parameter BTF_MAX_BUFFER_COUNT_WIDTH = bits_to_represent(BTF_MAX_BYTES);

    parameter WAVEFORM_WIDTH = 16;
    parameter WAVEFORM_MAX_DEPTH = 1024-1; // So that the triggered bit will still remain in the fifo
    parameter WAVEFORM_COUNTER_WIDTH = bits_to_represent(WAVEFORM_MAX_DEPTH);

    /////////////////////////////////////////////////////////////////
    // To receive data from PC
    /////////////////////////////////////////////////////////////////
    parameter BTF_RX_BUFFER_BYTES = BTF_MAX_BYTES;
    parameter BTF_RX_BUFFER_WIDTH = BTF_MAX_BUFFER_WIDTH;
    parameter BTF_RX_BUFFER_COUNT_WIDTH = BTF_MAX_BUFFER_COUNT_WIDTH;
    parameter CMD_RX_BUFFER_BYTES = 4'hf;
    parameter CMD_RX_BUFFER_WIDTH = 8 * CMD_RX_BUFFER_BYTES;

    wire [BTF_RX_BUFFER_WIDTH:1] BTF_Buffer;
    wire [BTF_RX_BUFFER_COUNT_WIDTH-1:0] BTF_Length;
    
    wire [CMD_RX_BUFFER_WIDTH:1] CMD_Buffer;
    wire [3:0] CMD_Length;    
    wire CMD_Ready;
    
    wire esc_char_detected;
    wire [7:0] esc_char;

    wire wrong_format;
        
    wire [WAVEFORM_WIDTH-1:0] trigger_mask, trigger_pattern;
    wire [WAVEFORM_COUNTER_WIDTH-1:0] points_to_capture_after_trigger;
    
    data_receiver receiver(.RxD(Uart_RXD), .clk(CLK100MHZ), 
        .BTF_Buffer(BTF_Buffer), .BTF_Length(BTF_Length), 
        .CMD_Buffer(CMD_Buffer), .CMD_Length(CMD_Length), .CMD_Ready(CMD_Ready), 
        .esc_char_detected(esc_char_detected), .esc_char(esc_char), .wrong_format(wrong_format),
        .trigger_mask(trigger_mask), .trigger_pattern(trigger_pattern), .points_to_capture_after_trigger(points_to_capture_after_trigger)
    );
    defparam receiver.BTF_RX_BUFFER_COUNT_WIDTH = BTF_RX_BUFFER_COUNT_WIDTH;
    defparam receiver.BTF_RX_BUFFER_BYTES = BTF_RX_BUFFER_BYTES; // can be between 1 and 2^BTF_RX_BUFFER_COUNT_WIDTH - 1
    defparam receiver.BTF_RX_BUFFER_WIDTH = BTF_RX_BUFFER_WIDTH;
    defparam receiver.ClkFreq = ClkFreq;
    defparam receiver.BaudRate = BaudRate;
    defparam receiver.CMD_RX_BUFFER_BYTES = CMD_RX_BUFFER_BYTES;
    defparam receiver.CMD_RX_BUFFER_WIDTH = CMD_RX_BUFFER_WIDTH;
    defparam receiver.WAVEFORM_WIDTH = WAVEFORM_WIDTH;
    defparam receiver.WAVEFORM_MAX_DEPTH = WAVEFORM_MAX_DEPTH;
    defparam receiver.WAVEFORM_COUNTER_WIDTH = WAVEFORM_COUNTER_WIDTH;

    /////////////////////////////////////////////////////////////////
    // To send data to PC
    /////////////////////////////////////////////////////////////////

    parameter TX_BUFFER1_BYTES =  4'hf;
    parameter TX_BUFFER1_WIDTH = 8 * TX_BUFFER1_BYTES;
    parameter TX_BUFFER1_LENGTH_WIDTH = bits_to_represent(TX_BUFFER1_BYTES);

    parameter TX_BUFFER2_BYTES = BTF_MAX_BYTES;
    parameter TX_BUFFER2_WIDTH = BTF_MAX_BUFFER_WIDTH;
    parameter TX_BUFFER2_LENGTH_WIDTH = BTF_MAX_BUFFER_COUNT_WIDTH;

    parameter TX_WAVEFORM_BUFFER_BYTES =  8'h80;
    parameter TX_WAVEFORM_BTF_HEADER = "#280";
    parameter TX_WAVEFORM_BUFFER_WIDTH = 8 * TX_WAVEFORM_BUFFER_BYTES;

    reg [TX_BUFFER1_LENGTH_WIDTH-1:0] TX_buffer1_length;
    reg [1:TX_BUFFER1_WIDTH] TX_buffer1;
    reg TX_buffer1_ready;

    reg [TX_BUFFER2_LENGTH_WIDTH-1:0] TX_buffer2_length;
    reg [1:TX_BUFFER2_WIDTH] TX_buffer2;
    reg TX_buffer2_ready;

    wire [1:TX_WAVEFORM_BUFFER_WIDTH] TX_waveform_buffer;
    wire TX_waveform_buffer_ready;
    
    wire TX_FIFO_ready;
    
    wire [1:32] monitoring_32bits;
    wire cwd_armed, cwd_triggered;

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
    .TX_waveform_buffer(TX_waveform_buffer),
    .TX_waveform_buffer_ready(TX_waveform_buffer_ready),
    .TX_FIFO_ready(TX_FIFO_ready),
    .bits_to_send(monitoring_32bits),
    .capture_waveform_data_implemented(1'b1), // 1'b1 if capture_waveform_data is available
    .armed(cwd_armed),
    .triggered(cwd_triggered)
);

    defparam sender.ClkFreq = ClkFreq;
    defparam sender.BaudRate = BaudRate;
    defparam sender.TX_BUFFER1_LENGTH_WIDTH = TX_BUFFER1_LENGTH_WIDTH;
    defparam sender.TX_BUFFER1_BYTES =  TX_BUFFER1_BYTES;
    defparam sender.TX_BUFFER1_WIDTH = TX_BUFFER1_WIDTH;
    defparam sender.TX_BUFFER2_LENGTH_WIDTH = TX_BUFFER2_LENGTH_WIDTH;
    defparam sender.TX_BUFFER2_BYTES = TX_BUFFER2_BYTES;
    defparam sender.TX_BUFFER2_WIDTH = TX_BUFFER2_WIDTH;
    defparam sender.TX_WAVEFORM_BUFFER_BYTES =  TX_WAVEFORM_BUFFER_BYTES;
    defparam sender.TX_WAVEFORM_BTF_HEADER = TX_WAVEFORM_BTF_HEADER;
    defparam sender.TX_WAVEFORM_BUFFER_WIDTH = TX_WAVEFORM_BUFFER_WIDTH;

    /////////////////////////////////////////////////////////////////
    // Capture waveform data
    /////////////////////////////////////////////////////////////////

    reg waveform_capture_start_trigger;
    wire [WAVEFORM_WIDTH-1:0] waveform_data;

    wire [2:0] capture_waveform_data_main_state;
    
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
        .esc_char(esc_char),
        .main_state_copy(capture_waveform_data_main_state)
    );
    defparam cwd.TX_WAVEFORM_BUFFER_BYTES =  TX_WAVEFORM_BUFFER_BYTES;
    defparam cwd.TX_WAVEFORM_BUFFER_WIDTH = TX_WAVEFORM_BUFFER_WIDTH;
    defparam cwd.WAVEFORM_WIDTH = WAVEFORM_WIDTH;
    defparam cwd.WAVEFORM_MAX_DEPTH = WAVEFORM_MAX_DEPTH;
    defparam cwd.WAVEFORM_COUNTER_WIDTH = WAVEFORM_COUNTER_WIDTH;


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
    parameter IDN_REPLY = "Protocol v1_02"; // 14 characters

    
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


    /////////////////////////////////////////////////////////////////
    // Command definition to capture waveform data
    /////////////////////////////////////////////////////////////////
    parameter CMD_CAPTURE_WAVEFORM = "WAVEFORM"; // 8 characters

    reg [15:0] temp_counter_16bits;
    
    always @ (posedge CLK100MHZ) begin
        temp_counter_16bits <= temp_counter_16bits + patterns[1:2] + 'd1;
    end

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
    // Main FSM
    /////////////////////////////////////////////////////////////////
	reg [3:0] main_state;
    // State definition of FSM
    // Common state
    parameter MAIN_IDLE = 4'h0;    

    parameter MAIN_CAPTURE_WAVEFORM_END = 4'h5;

    parameter MAIN_UNKNOWN_CMD =4'h8;
    

    initial begin
        main_state <= MAIN_IDLE;
        patterns <= 'd0;
        TX_buffer1_ready <= 1'b0;
        TX_buffer2_ready <= 1'b0;
        waveform_capture_start_trigger <= 1'b0;
    end
    
    always @ (posedge CLK100MHZ)
        if (esc_char_detected == 1'b1) begin
            if (esc_char == "C") begin
                TX_buffer1_ready <= 1'b0;
                TX_buffer2_ready <= 1'b0;
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

                        else if ((CMD_Length == $bits(CMD_CAPTURE_WAVEFORM)/8) && (CMD_Buffer[$bits(CMD_CAPTURE_WAVEFORM):1] == CMD_CAPTURE_WAVEFORM)) begin
                            waveform_capture_start_trigger <= 1'b1;
                            main_state <= MAIN_CAPTURE_WAVEFORM_END;
                        end
                        else begin
                            main_state <= MAIN_UNKNOWN_CMD;
                        end
                    end
                    else begin
                        TX_buffer1_ready <= 1'b0;
                        TX_buffer2_ready <= 1'b0;
                    end
                    

                MAIN_CAPTURE_WAVEFORM_END: begin
                        waveform_capture_start_trigger <= 1'b0;
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
    assign monitoring_32bits = {patterns[1:26], cwd_armed, cwd_triggered, 1'b0, capture_waveform_data_main_state[2:0]};
    assign waveform_data[15:0] = temp_counter_16bits;

    //assign led[5:2] = main_state[3:0];
 
endmodule
