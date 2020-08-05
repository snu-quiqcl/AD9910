`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2017/12/13 15:41:48
// Design Name: 
// Module Name: data_sender
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

module data_sender
#(parameter BaudRate = 57600,    // Baud rate. Maximum allowed Baud rate of FTDI chip is 3000000 which means that transmission of 1 Byte takes at least 2.6 us. In usual Baud rate is much less than the maximum, so transmission of each character takes much longer than 2.6 us. 
  parameter ClkFreq = 100000000,    // make sure this matches the clock frequency on your board. If master clock is 100MHz, even in the worst case (Baud rate is 3M), we have roughly 260 clocks of interval between two characters.

  parameter TX_PORT3_FIFO_DATA_COUNT_WIDTH = 11, // Currently we will use maximum of 512, but I need to keep this the same as OUTPUT_FIFO_DATA_COUNT_WIDTH defined in main
  parameter DATA_FIFO_DATA_WIDTH = 64 // Defined in fifo_generator_bram_64x1024 IP
) // https://groups.google.com/forum/#!topic/comp.lang.verilog/6xZxOLUcNYI
(
    output [3:0] FSMState,
    input clk,
    output TxD,
    input esc_char_detected,
    input [7:0] esc_char,
    input wrong_format,
    input [TX_BUFFER1_LENGTH_WIDTH-1:0] TX_buffer1_length,
    input [1:TX_BUFFER1_WIDTH] TX_buffer1,
    input TX_buffer1_ready,
    input [TX_BUFFER2_LENGTH_WIDTH-1:0] TX_buffer2_length,
    input [1:TX_BUFFER2_WIDTH] TX_buffer2,
    input TX_buffer2_ready,
    
    input [TX_PORT3_FIFO_DATA_COUNT_WIDTH-1:0] TX_port3_data_length,
    input TX_port3_ready,
    output reg data_fifo_rd_en,
    input [DATA_FIFO_DATA_WIDTH-1:0] data_fifo_dout,
    
    input [1:TX_WAVEFORM_BUFFER_WIDTH] TX_waveform_buffer,
    input TX_waveform_buffer_ready, // 1'b1 if capture_waveform_data is available
    output TX_FIFO_ready,
    input [1:32] bits_to_send,
    input capture_waveform_data_implemented,
    input armed, 
    input triggered
);
    wire [7:0] TX_buffer1_length_ascii;
    hex2ascii buffer1_length_ascii(.hex_input(TX_buffer1_length), .ascii_output(TX_buffer1_length_ascii));

    wire [3*8-1:0] TX_buffer2_length_ascii;
    hex2ascii buffer2_0_length_ascii(.hex_input(TX_buffer2_length[3:0]), .ascii_output(TX_buffer2_length_ascii[1*8-1:0*8]));
    hex2ascii buffer2_1_length_ascii(.hex_input(TX_buffer2_length[7:4]), .ascii_output(TX_buffer2_length_ascii[2*8-1:1*8]));
    hex2ascii buffer2_2_length_ascii(.hex_input({3'b000, TX_buffer2_length[8]}), .ascii_output(TX_buffer2_length_ascii[3*8-1:2*8]));

    wire [4*8-1:0] TX_port3_length_ascii;
    hex2ascii port3_0_length_ascii(.hex_input({TX_port3_data_length[0], 3'b000}), .ascii_output(TX_port3_length_ascii[1*8-1:0*8]));
    hex2ascii port3_1_length_ascii(.hex_input(TX_port3_data_length[4:1]), .ascii_output(TX_port3_length_ascii[2*8-1:1*8]));
    hex2ascii port3_2_length_ascii(.hex_input(TX_port3_data_length[8:5]), .ascii_output(TX_port3_length_ascii[3*8-1:2*8]));
    hex2ascii port3_3_length_ascii(.hex_input({2'b00, TX_port3_data_length[10:9]}), .ascii_output(TX_port3_length_ascii[4*8-1:3*8]));

	////////////////////////////////////////////////////////////////
	// Detect when triggered
	////////////////////////////////////////////////////////////////
	wire TX_buffer1_PosEdge;
	reg TX_buffer1_ready_delay;
	initial TX_buffer1_ready_delay = 1'b0;
	assign TX_buffer1_PosEdge = (TX_buffer1_ready & ~TX_buffer1_ready_delay);

	wire TX_buffer2_PosEdge;
	reg TX_buffer2_ready_delay;
	initial TX_buffer2_ready_delay = 1'b0;
	assign TX_buffer2_PosEdge = (TX_buffer2_ready & ~TX_buffer2_ready_delay);

	wire TX_port3_PosEdge;
	reg TX_port3_ready_delay;
	initial TX_port3_ready_delay = 1'b0;
	assign TX_port3_PosEdge = (TX_port3_ready & ~TX_port3_ready_delay);

	wire TX_waveform_buffer_PosEdge;
	reg TX_waveform_buffer_ready_delay;
	initial TX_waveform_buffer_ready_delay = 1'b0;
	assign TX_waveform_buffer_PosEdge = (TX_waveform_buffer_ready & ~TX_waveform_buffer_ready_delay);


    always @ (posedge clk)
        begin
            TX_buffer1_ready_delay <= TX_buffer1_ready;
            TX_buffer2_ready_delay <= TX_buffer2_ready;
            TX_port3_ready_delay <= TX_port3_ready;
            TX_waveform_buffer_ready_delay <= TX_waveform_buffer_ready;
        end


	////////////////////////////////////////////////////////////////
	// Write FIFO
	////////////////////////////////////////////////////////////////
    reg reset_FIFO;
    reg [7:0] FIFO_din;
    reg FIFO_wr_en;
    reg FIFO_rd_en;
    
    wire [7:0] FIFO_dout;
    wire FIFO_full;
    wire FIFO_overflow;
    wire FIFO_empty;
    wire FIFO_underflow;

    fifo_generator_0 transmitter_FIFO(
    .clk(clk),
    .rst(reset_FIFO),
    .din(FIFO_din),
    .wr_en(FIFO_wr_en),
    .rd_en(FIFO_rd_en),
    .dout(FIFO_dout),
    .full(FIFO_full),
    .overflow(FIFO_overflow),
    .empty(FIFO_empty),
    .underflow(FIFO_underflow)
  );



	////////////////////////////////////////////////////////////////
	// Terminating string
	////////////////////////////////////////////////////////////////
	reg [7:0] TERMINATOR_CURRENT_CHAR;
    parameter TERMINATOR_LENGTH = 'd2;
    reg [1:0] TERMINATOR_CURRENT_CHAR_POINTER;
    initial TERMINATOR_CURRENT_CHAR_POINTER = 'd0;

    always @(TERMINATOR_CURRENT_CHAR_POINTER)
        case(TERMINATOR_CURRENT_CHAR_POINTER)
            'd0: TERMINATOR_CURRENT_CHAR = "\r";
            'd1: TERMINATOR_CURRENT_CHAR = "\n"; // (TERMINATOR_LENGTH - 1)
            default: TERMINATOR_CURRENT_CHAR = 'd0;
        endcase

	////////////////////////////////////////////////////////////////
	// Finite State Machine
	////////////////////////////////////////////////////////////////
	reg [5:0] main_state;
	assign FSMState = main_state;
	
	parameter MAIN_FIFO_INITIALIZE = 'd0;
	parameter MAIN_FIFO_INITIALIZE_WAIT = 'd1;
	
	parameter MAIN_IDLE = 'd4;
    parameter MAIN_ESC_CHAR_SEND = 'd5;
    parameter MAIN_SEND_FINISH = 'd6;
    reg [7:0] esc_char_latch;
	
	parameter MAIN_BUFFER1_SEND = 'd8;
    reg [1+TX_BUFFER1_LENGTH_WIDTH-1:0] TX_full_buffer1_length;
    parameter TX_FULL_BUFFER1_WIDTH = 2*8+TX_BUFFER1_WIDTH; 
    reg [1:TX_FULL_BUFFER1_WIDTH] TX_full_buffer1;
    reg esc_already_encountered;

    
	parameter MAIN_BUFFER2_SEND = 'd10;    
    reg [1+TX_BUFFER2_LENGTH_WIDTH-1:0] TX_full_buffer2_length;
    parameter TX_FULL_BUFFER2_WIDTH = 5*8+TX_BUFFER2_WIDTH; 
    reg [1:TX_FULL_BUFFER2_WIDTH] TX_full_buffer2;




    parameter MAIN_PORT3_SEND_HEADER = 'd12;
    reg [2:0] TX_port3_header_length;
    parameter TX_PORT3_HEADER_WIDTH = 6*8;
    reg [1:TX_PORT3_HEADER_WIDTH] TX_port3_header;
    parameter MAIN_PORT3_READ_DATA_FIFO = 'd13;
    reg [TX_PORT3_FIFO_DATA_COUNT_WIDTH-1:0] data_count_to_read_from_FIFO;
    reg [1:DATA_FIFO_DATA_WIDTH] next_data_from_FIFO;
    parameter MAIN_PORT3_SEND_DATA = 'd14;
    reg [3:0] port3_data_count_to_send;



	parameter MAIN_WAVEFORM_BUFFER_SEND = 'd16;
    reg [1+TX_WAVEFORM_BUFFER_LENGTH_WIDTH-1:0] TX_full_waveform_buffer_length;
    parameter TX_FULL_WAVEFORM_BUFFER_WIDTH = $bits(TX_WAVEFORM_BTF_HEADER)+TX_WAVEFORM_BUFFER_WIDTH;
    reg [1:TX_FULL_WAVEFORM_BUFFER_WIDTH] TX_full_waveform_buffer;

	
	parameter MAIN_SEND_TERMINATOR = 'd20;
	
    parameter MAIN_ESC_DETECTED = 'd21;

    parameter FIFO_RESET_WAIT_COUNTER_WIDTH = 4;
    parameter FIFO_RESET_WAIT_INTERVAL = 2 ** FIFO_RESET_WAIT_COUNTER_WIDTH - 1;
    reg [FIFO_RESET_WAIT_COUNTER_WIDTH-1:0] FIFO_reset_wait_counter; // According to page 133 of https://www.xilinx.com/support/documentation/ip_documentation/fifo_generator/v13_2/pg057-fifo-generator.pdf, FIFO reset seems to be held asserted for 5 clock cycles. But according to my experience, I should wait for a few clock cycles after FIFO reset is de-asserted, so I'm waiting for 15 clock cycles. 


    reg TX_FIFO_busy;
    initial
        begin
            main_state <= MAIN_FIFO_INITIALIZE;
            esc_char_latch <= 'd0;
            TX_FIFO_busy <= 1'b0;
            FIFO_reset_wait_counter <= FIFO_RESET_WAIT_INTERVAL;
            esc_already_encountered <= 1'b0;
            data_fifo_rd_en <= 1'b0;
        end
        
    always @ (posedge clk)
        if (esc_char_detected == 1'b1) begin
            if ((esc_char == "C") || (esc_char == "R") || (esc_char == "W")) begin
                reset_FIFO <= 1'b1;
                FIFO_wr_en <= 1'b0;
                esc_char_latch <= esc_char;
                main_state <= MAIN_ESC_DETECTED;
                FIFO_reset_wait_counter <= FIFO_RESET_WAIT_INTERVAL;
            end
        end
        else begin
            case (main_state)
                MAIN_FIFO_INITIALIZE: begin
                        main_state <= MAIN_FIFO_INITIALIZE_WAIT;
                        reset_FIFO <= 1'b1;
                        FIFO_wr_en <= 1'b0;
                        FIFO_reset_wait_counter <= FIFO_RESET_WAIT_INTERVAL;
                        TX_FIFO_busy <= 1'b1;
                    end

                MAIN_FIFO_INITIALIZE_WAIT: begin
                        reset_FIFO <= 1'b0;
                        if (FIFO_reset_wait_counter == 'd0) begin
                            main_state <= MAIN_IDLE;
                            TX_FIFO_busy <= 1'b0;
                        end
                        else begin
                            FIFO_reset_wait_counter <= FIFO_reset_wait_counter - 'd1;
                        end
                    end
                
                MAIN_IDLE:
                    if (wrong_format == 1'b1) begin
                        main_state <= MAIN_BUFFER1_SEND;
                        TX_FIFO_busy <= 1'b1;
                        TX_full_buffer1_length <= 'd2 + 'd12;
                        TX_full_buffer1[1:14*8] <= {"!", "C", "Wrong format"};
                    end
                    
                    else if (TX_buffer1_PosEdge == 1'b1) begin
                        main_state <= MAIN_BUFFER1_SEND;
                        TX_FIFO_busy <= 1'b1;
                        TX_full_buffer1_length <= 'd2 + {1'b0, TX_buffer1_length};
                        TX_full_buffer1[1:TX_FULL_BUFFER1_WIDTH] <= {"!", TX_buffer1_length_ascii[7:0], TX_buffer1[1:TX_BUFFER1_WIDTH]};
                    end
                    
                    else if (TX_buffer2_PosEdge == 1'b1) begin
                        main_state <= MAIN_BUFFER2_SEND;
                        TX_FIFO_busy <= 1'b1;
                        TX_full_buffer2_length <= 'd2 +'d3 + {1'b0, TX_buffer2_length};
                        TX_full_buffer2[1:TX_FULL_BUFFER2_WIDTH] <= {"#3", TX_buffer2_length_ascii[3*8-1:0], TX_buffer2[1:TX_BUFFER2_WIDTH]};
                        esc_already_encountered <= 1'b0;
                    end

                    else if (TX_port3_PosEdge == 1'b1) begin
                        main_state <= MAIN_PORT3_SEND_HEADER;
                        TX_FIFO_busy <= 1'b1;
                        TX_port3_header_length[2:0] <= 'd6;
                        TX_port3_header[1:TX_PORT3_HEADER_WIDTH] <= {"#4", TX_port3_length_ascii[4*8-1:0]};
                        data_count_to_read_from_FIFO <= TX_port3_data_length;
                        esc_already_encountered <= 1'b0;
                    end

                    else if (TX_waveform_buffer_PosEdge == 1'b1) begin
                        main_state <= MAIN_WAVEFORM_BUFFER_SEND;
                        TX_FIFO_busy <= 1'b1;
                        TX_full_waveform_buffer_length <= $bits(TX_WAVEFORM_BTF_HEADER)/8 + TX_WAVEFORM_BUFFER_BYTES;
                        TX_full_waveform_buffer[1:TX_FULL_WAVEFORM_BUFFER_WIDTH] <= {TX_WAVEFORM_BTF_HEADER, TX_waveform_buffer[1:TX_WAVEFORM_BUFFER_WIDTH]};
                        esc_already_encountered <= 1'b0;
                    end
                    
                    else begin
                        TX_FIFO_busy <= 1'b0;
                        data_fifo_rd_en <= 1'b0;
                    end

                    

                MAIN_PORT3_SEND_HEADER: begin
                        if (TX_port3_header_length[2:0] > 0) begin
                            FIFO_din <= TX_port3_header[1:8];
                            FIFO_wr_en <= 1'b1;
                            TX_port3_header_length <= TX_port3_header_length - 'd1;
                            TX_port3_header[1:TX_PORT3_HEADER_WIDTH] <= {TX_port3_header[9:TX_PORT3_HEADER_WIDTH], 8'h00};
                        end
                        else begin
                            TERMINATOR_CURRENT_CHAR_POINTER <= 'd0;
                            main_state <= MAIN_PORT3_READ_DATA_FIFO;
                            FIFO_wr_en <= 1'b0;
                        end
                    end
                    
                MAIN_PORT3_READ_DATA_FIFO: begin
                        if (data_count_to_read_from_FIFO > 0) begin
                            next_data_from_FIFO <= data_fifo_dout;
                            port3_data_count_to_send <= 8;
                            data_fifo_rd_en <= 1'b1; // Remove one data from data FIFO
                            data_count_to_read_from_FIFO <= data_count_to_read_from_FIFO - 'd1;
                            esc_already_encountered <= 1'b0;
                            main_state <= MAIN_PORT3_SEND_DATA;
                        end
                        else begin
                            FIFO_din <= TERMINATOR_CURRENT_CHAR;
                            data_fifo_rd_en <= 1'b0;
                            FIFO_wr_en <= 1'b1;
                            TERMINATOR_CURRENT_CHAR_POINTER <= TERMINATOR_CURRENT_CHAR_POINTER + 'd1;
                            main_state <= MAIN_SEND_TERMINATOR;
                        end
                    end



                MAIN_PORT3_SEND_DATA: begin
                        data_fifo_rd_en <= 1'b0;
                        if (port3_data_count_to_send > 0) begin
                            FIFO_din <= next_data_from_FIFO[1:8];
                            FIFO_wr_en <= 1'b1;
                            if ((next_data_from_FIFO[1:8] == 8'h10) && (esc_already_encountered == 1'b0)) begin // The '\x10' is encountered first time
                                esc_already_encountered <= 1'b1;
                            end
                            else begin
                                esc_already_encountered <= 1'b0;
                                port3_data_count_to_send <= port3_data_count_to_send - 'd1;
                                next_data_from_FIFO[1:DATA_FIFO_DATA_WIDTH] <= {next_data_from_FIFO[9:DATA_FIFO_DATA_WIDTH], 8'h00};
                            end
                        end
                        else begin
                            main_state <= MAIN_PORT3_READ_DATA_FIFO;
                            FIFO_wr_en <= 1'b0;
                        end
                    end

                
                
                
                
                MAIN_ESC_DETECTED: begin
                        reset_FIFO <= 1'b0;
                        if (FIFO_reset_wait_counter == 'd0) begin
                            main_state <= MAIN_ESC_CHAR_SEND;
                            TX_FIFO_busy <= 1'b1;
                            FIFO_din <= 8'h10;
                            FIFO_wr_en <= 1'b1;
                        end
                        else begin
                            FIFO_reset_wait_counter <= FIFO_reset_wait_counter - 'd1;
                        end
                    end
                    
                MAIN_ESC_CHAR_SEND: begin
                        TX_FIFO_busy <= 1'b1;
                        FIFO_din <= esc_char_latch;
                        FIFO_wr_en <= 1'b1;
                        if (esc_char_latch == "R") begin
                            main_state <= MAIN_BUFFER1_SEND;
                            TX_full_buffer1_length <= 'd5;
                            TX_full_buffer1[1:5*8] <= {bits_to_send, {5{1'b0}}, capture_waveform_data_implemented, armed, triggered };
                            TERMINATOR_CURRENT_CHAR_POINTER <= 'd0;
                        end
                        else begin // "\x10C", "\x10W"
                            main_state <= MAIN_SEND_FINISH;
                        end
                    end

                MAIN_SEND_FINISH: begin
                        main_state <= MAIN_IDLE;
                        TX_FIFO_busy <= 1'b0;
                        FIFO_wr_en <= 1'b0;
                    end
                
                MAIN_BUFFER1_SEND:
                    if (TX_full_buffer1_length > 0) begin
                        FIFO_din <= TX_full_buffer1[1:8];
                        FIFO_wr_en <= 1'b1;
                        TERMINATOR_CURRENT_CHAR_POINTER <= 'd0;
                        if ((TX_full_buffer1[1:8] == 8'h10) && (esc_already_encountered == 1'b0)) begin // The '\x10' is encountered first time
                            esc_already_encountered <= 1'b1;
                        end
                        else begin
                            esc_already_encountered <= 1'b0;
                            TX_full_buffer1_length <= TX_full_buffer1_length - 'd1;
                            TX_full_buffer1[1:TX_FULL_BUFFER1_WIDTH] <= {TX_full_buffer1[9:TX_FULL_BUFFER1_WIDTH], 8'h00};
                        end
                    end
                    else begin
                        main_state <= MAIN_SEND_TERMINATOR;
                        FIFO_din <= TERMINATOR_CURRENT_CHAR;
                        FIFO_wr_en <= 1'b1;
                        TERMINATOR_CURRENT_CHAR_POINTER <= TERMINATOR_CURRENT_CHAR_POINTER + 'd1;
                    end
                    
                MAIN_SEND_TERMINATOR:
                    if (TERMINATOR_CURRENT_CHAR_POINTER == TERMINATOR_LENGTH) begin
                        main_state <= MAIN_IDLE;
                        FIFO_din <= TERMINATOR_CURRENT_CHAR;
                        FIFO_wr_en <= 1'b0;
                        TX_FIFO_busy <= 1'b0;
                        TERMINATOR_CURRENT_CHAR_POINTER <= 'd0;
                    end
                    else begin
                        FIFO_din <= TERMINATOR_CURRENT_CHAR;
                        FIFO_wr_en <= 1'b1;
                        TERMINATOR_CURRENT_CHAR_POINTER <= TERMINATOR_CURRENT_CHAR_POINTER + 'd1;
                    end


                    
                MAIN_BUFFER2_SEND:
                        if (TX_full_buffer2_length > 0) begin
                            FIFO_din <= TX_full_buffer2[1:8];
                            FIFO_wr_en <= 1'b1;
                            TERMINATOR_CURRENT_CHAR_POINTER <= 'd0;
                            if ((TX_full_buffer2[1:8] == 8'h10) && (esc_already_encountered == 1'b0)) begin // The '\x10' is encountered first time
                                esc_already_encountered <= 1'b1;
                            end
                            else begin
                                esc_already_encountered <= 1'b0;
                                TX_full_buffer2_length <= TX_full_buffer2_length - 'd1;
                                TX_full_buffer2[1:TX_FULL_BUFFER2_WIDTH] <= {TX_full_buffer2[9:TX_FULL_BUFFER2_WIDTH], 8'h00};
                            end
                        end
                        else begin
                            main_state <= MAIN_SEND_TERMINATOR;
                            FIFO_din <= TERMINATOR_CURRENT_CHAR;
                            FIFO_wr_en <= 1'b1;
                            TERMINATOR_CURRENT_CHAR_POINTER <= TERMINATOR_CURRENT_CHAR_POINTER + 'd1;
                        end
                        







                MAIN_WAVEFORM_BUFFER_SEND:
                        if (TX_full_waveform_buffer_length > 0) begin
                            FIFO_din <= TX_full_waveform_buffer[1:8];
                            FIFO_wr_en <= 1'b1;
                            TERMINATOR_CURRENT_CHAR_POINTER <= 'd0;
                            if ((TX_full_waveform_buffer[1:8] == 8'h10) && (esc_already_encountered == 1'b0)) begin // The '\x10' is encountered first time
                                esc_already_encountered <= 1'b1;
                            end
                            else begin
                                esc_already_encountered <= 1'b0;
                                TX_full_waveform_buffer_length <= TX_full_waveform_buffer_length - 'd1;
                                TX_full_waveform_buffer[1:TX_FULL_WAVEFORM_BUFFER_WIDTH] <= {TX_full_waveform_buffer[9:TX_FULL_WAVEFORM_BUFFER_WIDTH], 8'h00};
                            end
                        end
                        else begin
                            main_state <= MAIN_SEND_TERMINATOR;
                            FIFO_din <= TERMINATOR_CURRENT_CHAR;
                            FIFO_wr_en <= 1'b1;
                            TERMINATOR_CURRENT_CHAR_POINTER <= TERMINATOR_CURRENT_CHAR_POINTER + 'd1;
                        end

                
                default:
                    main_state <= MAIN_IDLE;

		endcase
	end


    assign TX_FIFO_ready = ~(TX_FIFO_busy | FIFO_full); 




	////////////////////////////////////////////////////////////////
	// async_transmitter is designed to 8-bits data, 2 stop bits, no-parity
	wire TxD_busy;
	reg TxD_start;
	
	async_transmitter TXUSB(.clk(clk), .TxD(TxD), .TxD_busy(TxD_busy), .TxD_start(TxD_start),
									.TxD_data(FIFO_dout));
	defparam TXUSB.ClkFrequency = ClkFreq;
	defparam TXUSB.Baud         = BaudRate;


	////////////////////////////////////////////////////////////////
	// Finite State Machine
	////////////////////////////////////////////////////////////////
	reg [3:0] transmitter_state;
	parameter TX_IDLE = 4'h0;
	parameter TX_WAIT1 = 4'h1;
	parameter TX_WAIT2 = 4'h2;

	initial
	begin
		transmitter_state <= TX_IDLE;
		TxD_start <= 1'b0;
	end
	
    always @ (posedge clk)
        case (transmitter_state)
            TX_IDLE:
                if (FIFO_empty != 1'b1) begin
                    TxD_start <= 1'b1;
                    transmitter_state <= TX_WAIT1;
                end
                else begin
                    TxD_start <= 1'b0;
                end
                
            TX_WAIT1: // This state is added to let TxD_busy have enough time to go up
                begin
                    TxD_start <= 1'b0;
                    FIFO_rd_en <= 1'b1;
                    transmitter_state <= TX_WAIT2;
                end
                
            TX_WAIT2:
                begin
                    FIFO_rd_en <= 1'b0;
                    if (TxD_busy == 1'b0) // Transmission of one byte is over
                    transmitter_state <= TX_IDLE;
                end
                
            default:
                transmitter_state <= TX_IDLE;
                
		endcase



endmodule
