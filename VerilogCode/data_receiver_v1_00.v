`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2017/12/08 22:24:10
// Design Name: 
// Module Name: data_receiver
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



module data_receiver
    #(
    ////
    //*****BTF_RX_BUFFER_COUNT_WIDTH should be changed to 10?
    ////
      parameter BTF_RX_BUFFER_COUNT_WIDTH = 9,
      parameter BTF_RX_BUFFER_BYTES = 9'h100, // can be between 1 and 2^BTF_RX_BUFFER_COUNT_WIDTH - 1
      parameter BTF_RX_BUFFER_WIDTH = 8 * BTF_RX_BUFFER_BYTES,
      parameter BaudRate = 57600,    // Baud rate. Maximum allowed Baud rate of FTDI chip is 3000000 which means that transmission of 1 Byte takes at least 2.6 us. In usual Baud rate is much less than the maximum, so transmission of each character takes much longer than 2.6 us. 
      parameter ClkFreq = 100000000,	// make sure this matches the clock frequency on your board. If master clock is 100MHz, even in the worst case (Baud rate is 3M), we have roughly 260 clocks of interval between two characters. 
      parameter CMD_RX_BUFFER_BYTES = 4'hf,
      parameter CMD_RX_BUFFER_WIDTH = 8 * CMD_RX_BUFFER_BYTES,
      parameter WAVEFORM_WIDTH = 16,
      parameter WAVEFORM_MAX_DEPTH = 1024-1,
      parameter WAVEFORM_COUNTER_WIDTH = 10
      //parameter WAVEFORM_COUNTER_WIDTH = bits_to_represent(WAVEFORM_MAX_DEPTH)
    //  parameter WAVEFORM_COUNTER_WIDTH = bits_to_represent(WAVEFORM_MAX_DEPTH),
      ) // https://groups.google.com/forum/#!topic/comp.lang.verilog/6xZxOLUcNYI
      
    (
    input RxD,
    input clk,
    output reg [BTF_RX_BUFFER_WIDTH-1:0] BTF_Buffer,
    output reg [BTF_RX_BUFFER_COUNT_WIDTH-1:0] BTF_Length,
    output reg [CMD_RX_BUFFER_WIDTH-1:0] CMD_Buffer,
    output reg [3:0] CMD_Length,
    output reg CMD_Ready,
    output reg BTF_Ready,
    output reg esc_char_detected,
    output reg [7:0] esc_char,
    output reg wrong_format,
    output reg [WAVEFORM_WIDTH-1:0] trigger_mask,
    output reg [WAVEFORM_WIDTH-1:0] trigger_pattern,
    output reg [WAVEFORM_COUNTER_WIDTH-1:0] points_to_capture_after_trigger,
     // outputs below this line are for debugging purpose
    output [3:0] FSMState,
    output reg debug1,
    output reg debug2,
    output reg debug3    
    );
    initial debug1 = 1'b0;
    
	/////////////////////////////////////////////////////////////////
	// To receive data from PC
	/////////////////////////////////////////////////////////////////
	wire [7:0] usbdata ;
	wire usbready ;

	async_receiver RXUSB(.clk(clk), .RxD(RxD), .RxD_data_ready(usbready), .RxD_data(usbdata));
	defparam RXUSB.ClkFrequency = ClkFreq;
	defparam RXUSB.Baud         = BaudRate;
	
	wire [3:0] hexadecimal_value;
	wire non_hexadecimal;
	ascii2hex ascii2hex_moudule(.ascii_input(usbdata), .hex_output(hexadecimal_value), .error(non_hexadecimal));

	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// Protocol
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	//
	// '\x10'+'C': This is a special escape sequence to clear the input buffer. '\x10' is DLE (Data Link Escape) charater in ASCII table.
    //              This special sequence can be recognized even in the middle of the above command.
    //              If this command is encountered, the transmitter buffer will be also cleared and send '\x10'+'C' back to PC and 
    //              FSM will reset to the IDLE state. To send '\x10' corresponding to decimal value 16, '\x10\x10' should be sent.   
    //
	// '\x10'+'R': This is a special escape sequence to read the current status of 32 bits. '\x10' is DLE (Data Link Escape) charater in ASCII table.
    //              This special sequence can be recognized even in the middle of the above command.
    //              If this command is encountered, the transmitter buffer will be also cleared and send '\x10'+'R' + <32 bits> + '\r\n' and 
    //              FSM will reset to the IDLE state. To send '\x10' corresponding to decimal value 16, '\x10\x10' should be sent.   
    //
	// '\x10'+'T': This is a special escape sequence to set trigger setting. '\x10' is DLE (Data Link Escape) charater in ASCII table.
    //
	// '\x10'+'A': This is a special escape sequence to arm trigger. '\x10' is DLE (Data Link Escape) charater in ASCII table.
    //
	// '\x10'+'W': This is a special escape sequence to read the captured waveform date. '\x10' is DLE (Data Link Escape) charater in ASCII table.
    //              This special sequence can be recognized even in the middle of the above command.
    //              If this command is encountered, the transmitter buffer will be also cleared and send '\x10'+'W' and 
    //              FSM will reset to the IDLE state. To send '\x10' corresponding to decimal value 16, '\x10\x10' should be sent.   
    //
	// '!' <byte_count> <ASCII_string> '\r' '\n' : Command format. 1 <= (command length) <= 15
	//             <byte_count> is a "single" hexadecimal ASCII. E.g. 'b" means 11 characters excluding terminators(<cr><nl>)
	//             If <ASCII_string> contains a byte corresponding to decimal value 16 ('\x10'), '\x10\x10' should be sent, 
    //             and '\x10\x10' sequence is counted as one byte.
    //             The received command becomes available through CMD_Buffer, CMD_Length, and CMD_Ready signal is triggered.
	//             <examples>
	//             - !3RUN<cr><nl> is "RUN" command
	//             - "!5TEST\x10\x10\r\n" is {"TEST", 8'h10} command which has no meaning
	//
	// '#' <num_digits> <byte_count> <raw_data> '\r' '\n': Modified Binary Transfer Format (IEEE 488.2 # format)
    //             http://na.support.keysight.com/pna/help/latest/Programming/Learning_about_GPIB/Getting_Data_from_the_Analyzer.htm#block
    //             <num_digits> is a "single" hexadecial ASCII. E.g. 'a' means that following ten characters will represent block length
    //             <byte_count> is hexadecimal number written in ASCII. E.g. '15' means that the block size is 21 bytes. This length excludes terminators(<cr><nl>)
    //             The received binary block becomes available through BTF_Buffer, BTF_Length outputs, and triggers BTF_Ready, 
    //              but generally BTF is used by the following CMD rather than by itself.
    //             If <raw_data> contains a byte corresponding to decimal value 16 ('\x10'), '\x10\x10' should be sent, 
    //             and '\x10\x10' sequence is counted as one byte.
    //             <examples>
    //              - #20aABCDE+WXYZ<cr><nl> means block length is 10 and block data is "ABCDE+WXYZ"
    //              - #14A\x10\x10\x00B<cr><nl> means block length is 4 and the block data is {"A", 8'h10, 8'h00, "B"}
    // 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// Finite State Machine to detect escape sequence such as '\x10'+'C' 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	reg [3:0] escape_state;
	// State definition of FSM
	parameter ESC_IDLE = 4'h0;
    parameter ESC_DETECT = 4'h1;
    parameter ESC_C_FOUND = 4'h2;
    parameter ESC_R_FOUND = 4'h3;
    parameter ESC_W_FOUND = 4'h4;
    parameter ESC_A_FOUND = 4'h5;

    initial begin
        escape_state <= ESC_IDLE;
        esc_char_detected <= 1'b0;
        trigger_mask <= 16'hffff; // default trigger mask pattern
        trigger_pattern <= 16'h0001; // default trigger pattern
        points_to_capture_after_trigger <= WAVEFORM_MAX_DEPTH-'d32;
    end
    
    always @ (posedge clk)
        case (escape_state)
            ESC_IDLE: begin
                    esc_char_detected <= 1'b0;
                    if (usbready == 1) begin
                        if (usbdata[7:0] == 8'h10) begin
                            escape_state <= ESC_DETECT;
                        end
                    end
                end
                
            ESC_DETECT:
                if (usbready == 1) begin
                    if (usbdata[7:0] == 8'h10) begin // '\x10\x10' means decimal value 16 is transmitted
                        escape_state <= ESC_IDLE;
                    end
                    else if (usbdata[7:0] == "C") begin
                        escape_state <= ESC_C_FOUND;
                        esc_char_detected <= 1'b1;
                        esc_char <= "C";
                    end
                    else if (usbdata[7:0] == "R") begin
                        escape_state <= ESC_R_FOUND;
                        esc_char_detected <= 1'b1;
                        esc_char <= "R";
                     end
                    else if (usbdata[7:0] == "T") begin // Set trigger condition of waveform data capturing
                        trigger_mask <= BTF_Buffer[2*WAVEFORM_WIDTH+16-1:WAVEFORM_WIDTH+16];
                        trigger_pattern <= BTF_Buffer[WAVEFORM_WIDTH+16-1:16];
                        points_to_capture_after_trigger <= BTF_Buffer[16-1:0];
                        escape_state <= ESC_IDLE;
                       end
                    else if (usbdata[7:0] == "A") begin // Arm trigger
                             escape_state <= ESC_A_FOUND;
                             esc_char_detected <= 1'b1;
                             esc_char <= "A";
                          end
                    else if (usbdata[7:0] == "W") begin // read waveform data
                         escape_state <= ESC_W_FOUND;
                         esc_char_detected <= 1'b1;
                         esc_char <= "W";
                      end
                    else begin // This case should be reported as error
                        escape_state <= ESC_IDLE;
                    end
                end
                    
            ESC_C_FOUND: begin
                    escape_state <= ESC_IDLE;
                    esc_char_detected = 1'b0;
                end // I can add more action if necessary

            ESC_R_FOUND: begin
                    escape_state <= ESC_IDLE;
                    esc_char_detected = 1'b0;
                end // I can add more action if necessary

            ESC_A_FOUND: begin
                    escape_state <= ESC_IDLE;
                    esc_char_detected = 1'b0;
                end // I can add more action if necessary


            ESC_W_FOUND: begin
                    escape_state <= ESC_IDLE;
                    esc_char_detected = 1'b0;
                end // I can add more action if necessary
            
            default: // This case should be reported as error
                escape_state <= ESC_IDLE;

        endcase // End of "case (escape_state)"




	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// Finite State Machine
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	reg [3:0] main_state;
	assign FSMState = main_state;
	
	// State definition of FSM
	// Common state
	parameter MAIN_IDLE = 4'h0;

	// '#' '<num_digits>' <byte_count> <raw_data> '\r' '\n': Binary Transfer Format (IEEE 488.2 # format)
	parameter MAIN_BTF_READ_NUM_DIGITS = 4'h1;
	reg [3:0] btf_num_digits;
	parameter MAIN_BTF_READ_BYTE_COUNT = 4'h2;
	reg [BTF_RX_BUFFER_COUNT_WIDTH-1:0] btf_byte_count;
	reg [BTF_RX_BUFFER_COUNT_WIDTH-1:0] btf_actual_byte_count;
	parameter MAIN_BTF_READ_RAW_DATA = 4'h3;
    reg [BTF_RX_BUFFER_WIDTH-1:0] BTF_RXBuffer;
    parameter MAIN_BTF_READ_RAW_DATA_ESC_DETECTED = 4'h4;
	parameter MAIN_BTF_CHECK_TERMINATOR = 4'h5;
	parameter MAIN_BTF_EXECUTION = 4'h6;  

	// '!' '<byte_count> <ASCII_string> '\r' '\n' : Command format. 1 <= (command length) <= 15
    parameter MAIN_CMD_READ_BYTE_COUNT = 4'h7;
    reg [3:0] cmd_byte_count;
    reg [3:0] cmd_actual_byte_count;
    parameter MAIN_CMD_READ_ASCII_STRING = 4'h8;
    reg [CMD_RX_BUFFER_WIDTH-1:0] CMD_RXBuffer;
    parameter MAIN_CMD_READ_ASCII_STRING_ESC_DETECTED = 4'h9;
	parameter MAIN_CMD_CHECK_TERMINATOR = 4'ha;
	parameter MAIN_CMD_EXECUTION = 4'hb;

    // *CLS<cr><nl>
    parameter MAIN_ESC_CHAR_DETECTED = 4'hc;

    // Error
    parameter MAIN_WRONG_FORMAT = 4'hd;
    
    parameter MAIN_IDLE_FIRST_ESC_DETECTED = 4'he;
    
    reg [7:0] TERMINATOR_CURRENT_CHAR;
    parameter TERMINATOR_LENGTH = 'd2;
    reg TERMINATOR_CURRENT_CHAR_POINTER;
    initial TERMINATOR_CURRENT_CHAR_POINTER = 1'h0;

    always @(TERMINATOR_CURRENT_CHAR_POINTER)
        case(TERMINATOR_CURRENT_CHAR_POINTER)
            //0: TERMINATOR_CURRENT_CHAR = "\r";
            //1: TERMINATOR_CURRENT_CHAR = "\n"; // (TERMINATOR_LENGTH - 1)
            ////
            //****changed im AD9910 SIM
            ////
            0: TERMINATOR_CURRENT_CHAR = 13;
            1: TERMINATOR_CURRENT_CHAR = 10; // (TERMINATOR_LENGTH - 1)
            default: TERMINATOR_CURRENT_CHAR = 'd0;
        endcase
        


    // Main FSM
    initial begin
        main_state <= MAIN_IDLE;
        CMD_Ready <= 1'b0;
        BTF_Ready <= 1'b0;
        wrong_format <= 1'b0;
        BTF_RXBuffer <= 0;
    end
    always @ (posedge clk)
        if (esc_char_detected == 1'b1) begin
            main_state <= MAIN_ESC_CHAR_DETECTED;
            CMD_Ready <= 1'b0;
            BTF_Ready <= 1'b0;
            wrong_format <= 1'b0;
        end
        else begin  
            case (main_state)
                MAIN_IDLE: begin//0
                        CMD_Ready <= 1'b0;
                        BTF_Ready <= 1'b0;
                        wrong_format <= 1'b0;
                        if (usbready == 1) begin
                            if (usbdata[7:0] == "#") begin
                                main_state <= MAIN_BTF_READ_NUM_DIGITS;
                            end
                            else if (usbdata[7:0] == "!") begin
                                main_state <=  MAIN_CMD_READ_BYTE_COUNT;
                            end
                            else if (usbdata[7:0] == 8'h10) begin // If I don't treat this as special case, the first character of "!CWrong format" (i.e. "!") is sent before {8'h10, escape character} will be sent by the escape sequence handler.
                                main_state <=  MAIN_IDLE_FIRST_ESC_DETECTED;
                            end
                            else begin
                                main_state <= MAIN_WRONG_FORMAT;
                            end
                        end
                    end
                    
                MAIN_IDLE_FIRST_ESC_DETECTED:
                    if (usbready == 1) begin
                        if ((usbdata[7:0] != "C") && (usbdata[7:0] != "R") && (usbdata[7:0] != "T") &&
                            (usbdata[7:0] != "A") && (usbdata[7:0] != "W")) begin
                            main_state <= MAIN_WRONG_FORMAT;
                        end
                        else begin
                            main_state <= MAIN_IDLE;
                        end
                    end

                MAIN_BTF_READ_NUM_DIGITS://1
                    if (usbready == 1) begin
                        if (non_hexadecimal == 0) begin
                            btf_num_digits[3:0] <= hexadecimal_value[3:0];
                            main_state <= MAIN_BTF_READ_BYTE_COUNT;
                            btf_byte_count[BTF_RX_BUFFER_COUNT_WIDTH-1:0] <= 0;
                        end
                        else begin
                            main_state <= MAIN_WRONG_FORMAT;
                        end
                    end

                MAIN_BTF_READ_BYTE_COUNT://2
                    if  (usbready == 1) begin
                        if (non_hexadecimal == 0) begin
                            btf_byte_count[BTF_RX_BUFFER_COUNT_WIDTH-1:0] <= {btf_byte_count[BTF_RX_BUFFER_COUNT_WIDTH-1-4:0], hexadecimal_value[3:0]};
                            btf_num_digits[3:0] <= btf_num_digits[3:0] - 'h1;
                            if (btf_num_digits[3:0] == 'h1) begin
                                main_state <= MAIN_BTF_READ_RAW_DATA;
                                btf_actual_byte_count <= 'h0;
                            end
                        end
                        else begin
                            main_state <= MAIN_WRONG_FORMAT;
                        end
                    end
                
                MAIN_BTF_READ_RAW_DATA://3
                    if  (usbready == 1) begin
                        BTF_RXBuffer[BTF_RX_BUFFER_WIDTH-1:0] <= {BTF_RXBuffer[BTF_RX_BUFFER_WIDTH-1-8:0], usbdata[7:0]};
                        btf_byte_count[BTF_RX_BUFFER_COUNT_WIDTH-1:0] <= btf_byte_count[BTF_RX_BUFFER_COUNT_WIDTH-1:0] - 'h1;
                        btf_actual_byte_count[BTF_RX_BUFFER_COUNT_WIDTH-1:0] <= btf_actual_byte_count[BTF_RX_BUFFER_COUNT_WIDTH-1:0] + 'h1;
                        if (usbdata[7:0] == 8'h10) begin // The first '\x10' is detected
                            main_state <= MAIN_BTF_READ_RAW_DATA_ESC_DETECTED;
                        end
                        else if (btf_byte_count[BTF_RX_BUFFER_COUNT_WIDTH-1:0] == 'h1) begin
                            main_state <= MAIN_BTF_CHECK_TERMINATOR;
                            TERMINATOR_CURRENT_CHAR_POINTER <= 'h0;
                        end
                    end

                MAIN_BTF_READ_RAW_DATA_ESC_DETECTED://4
                    if  (usbready == 1) begin
                        if (usbdata[7:0] == 8'h10) begin // The second '\x10' is detected
                            if (btf_byte_count[BTF_RX_BUFFER_COUNT_WIDTH-1:0] == 'h0) begin // In case '\x10\x10' sequence is the last byte 
                                main_state <= MAIN_BTF_CHECK_TERMINATOR;
                                TERMINATOR_CURRENT_CHAR_POINTER <= 'h0;
                            end
                            else begin
                                main_state <= MAIN_BTF_READ_RAW_DATA;
                            end
                        end
                        else begin
                            main_state <= MAIN_WRONG_FORMAT;
                        end
                    end


                MAIN_BTF_CHECK_TERMINATOR://5
                    if  (usbready == 1) begin
                        if (usbdata[7:0] == TERMINATOR_CURRENT_CHAR) begin
                            if (TERMINATOR_CURRENT_CHAR_POINTER == (TERMINATOR_LENGTH - 1)) begin
                                main_state <= MAIN_BTF_EXECUTION;
                                TERMINATOR_CURRENT_CHAR_POINTER <= 'd0;
                                BTF_Buffer <= BTF_RXBuffer;
                                BTF_Length <= btf_actual_byte_count;
                                BTF_Ready <= 1'b1;
                            end
                            else begin
                                TERMINATOR_CURRENT_CHAR_POINTER <= TERMINATOR_CURRENT_CHAR_POINTER + 'd1;
                            end
                        end
                        else begin
                            main_state <= MAIN_WRONG_FORMAT;
                        end
                    end


                MAIN_BTF_EXECUTION://6
                    begin
                        main_state <= MAIN_IDLE;
                        BTF_Ready <= 1'b0;
                        debug2 <= ~debug2;
                    end

                MAIN_CMD_READ_BYTE_COUNT:
                    if  (usbready == 1'b1) begin
                        if (non_hexadecimal == 1'b0) begin
                            cmd_byte_count[3:0] <= hexadecimal_value[3:0];
                            main_state <= MAIN_CMD_READ_ASCII_STRING;
                            cmd_actual_byte_count[3:0] <= 'd0;
                        end
                        else begin
                            main_state <= MAIN_WRONG_FORMAT;
                        end
                    end
                
                MAIN_CMD_READ_ASCII_STRING:
                    if  (usbready == 1) begin
                        CMD_RXBuffer[CMD_RX_BUFFER_WIDTH-1:0] <= {CMD_RXBuffer[CMD_RX_BUFFER_WIDTH-1-8:0], usbdata[7:0]};
                        cmd_byte_count[3:0] <= cmd_byte_count[3:0] - 'd1;
                        cmd_actual_byte_count[3:0] <= cmd_actual_byte_count[3:0] + 'd1;
                        if (usbdata[7:0] == 8'h10) begin // The first '\x10' is detected
                            main_state <= MAIN_CMD_READ_ASCII_STRING_ESC_DETECTED;
                        end
                        else if (cmd_byte_count[3:0] == 'd1) begin  
                            main_state <= MAIN_CMD_CHECK_TERMINATOR;
                            TERMINATOR_CURRENT_CHAR_POINTER <= 'h0;
                        end
                    end
                MAIN_CMD_READ_ASCII_STRING_ESC_DETECTED:
                    if  (usbready == 1) begin
                        if (usbdata[7:0] == 8'h10) begin // The second '\x10' is detected
                            if (cmd_byte_count[3:0] == 'd0) begin// In case '\x10\x10' sequence is the last byte 
                                main_state <= MAIN_CMD_CHECK_TERMINATOR;
                                TERMINATOR_CURRENT_CHAR_POINTER <= 'h0;
                            end
                            else begin
                                main_state <= MAIN_CMD_READ_ASCII_STRING;
                            end
                        end
                        else begin
                            main_state <= MAIN_WRONG_FORMAT;
                        end
                    end
                
                MAIN_CMD_CHECK_TERMINATOR:
                    if  (usbready == 1) begin
                        if (usbdata[7:0] == TERMINATOR_CURRENT_CHAR) begin
                            if (TERMINATOR_CURRENT_CHAR_POINTER == (TERMINATOR_LENGTH - 1)) begin
                                main_state <= MAIN_CMD_EXECUTION;
                                TERMINATOR_CURRENT_CHAR_POINTER <= 'd0;
                                CMD_Buffer <= CMD_RXBuffer;
                                CMD_Length <= cmd_actual_byte_count;
                                CMD_Ready <= 1'b1;
                            end
                            else begin
                                TERMINATOR_CURRENT_CHAR_POINTER <= TERMINATOR_CURRENT_CHAR_POINTER + 'd1;
                            end
                        end
                        else begin
                            main_state <= MAIN_WRONG_FORMAT;
                        end
                    end

            
                MAIN_CMD_EXECUTION: begin
                        CMD_Ready <= 1'b0;
                        main_state <= MAIN_IDLE;
                        debug3 <= ~debug3;
                    end
                    
                MAIN_ESC_CHAR_DETECTED: begin
                        debug1 <= ~debug1;
                        main_state <= MAIN_IDLE;
                    end
                
                MAIN_WRONG_FORMAT: begin
                        wrong_format <= 1'b1;
                        main_state <= MAIN_IDLE;
                    end
                
                default: 
                    main_state <= MAIN_IDLE;
            endcase // End of case (main_state)
        end
    
endmodule
