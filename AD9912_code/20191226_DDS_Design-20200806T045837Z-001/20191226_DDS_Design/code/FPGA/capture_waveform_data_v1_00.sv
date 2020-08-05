`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2018/01/05 16:32:19
// Design Name: 
// Module Name: capture_waveform_data_v1_00
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


module capture_waveform_data
#(parameter TX_WAVEFORM_BUFFER_BYTES =  8'h80, // Defined in data_sender_v1_01
  parameter TX_WAVEFORM_BUFFER_WIDTH = 8 * TX_WAVEFORM_BUFFER_BYTES,
  parameter WAVEFORM_WIDTH = 16,
  parameter WAVEFORM_MAX_DEPTH = 1024-1,
  parameter WAVEFORM_COUNTER_WIDTH = 10, 
  parameter FIFO_WIDTH = 16, // Defined in block memory generator
  parameter FIFO_DEPTH = 1024, // Corresponding 10.24us data capture. Defined in block memory generator
  parameter FIFO_ADDRESS_WIDTH = 10 // Should be the same as WAVEFORM_COUNTER_WIDTH
)

(
    input CLK100MHZ,
    input [WAVEFORM_WIDTH-1:0] waveform,
    output reg armed,
    output reg triggered,
    input arm_signal,
    input [WAVEFORM_WIDTH-1:0] trigger_mask,
    input [WAVEFORM_WIDTH-1:0] trigger_pattern,
    input [WAVEFORM_COUNTER_WIDTH-1:0] points_to_capture_after_trigger,
    input TX_FIFO_ready,
    output reg [1:TX_WAVEFORM_BUFFER_WIDTH] TX_BUFFER,
    output reg TX_waveform_buffer_ready,
    input esc_char_detected,
    input [7:0] esc_char,
    output [2:0] main_state_copy
);
    //assert ( WAVEFORM_WIDTH == FIFO_WIDTH );
    //assert (WAVEFORM_MAX_DEPTH <= FIFO_DEPTH); 
    ////////////////////////////////////////////////////////////////
    // Detect when triggered
    ////////////////////////////////////////////////////////////////

    // First collect bits where waveform is different from trigger_patttern: (waveform ^ trigger_pattern) 
    // Then collect only bits which are marked important. I.e. masked bits: (waveform ^ trigger_pattern) & trigger_mask
    // If any of the final bits are 1, the required pattern is not matched.
    wire pattern_matched;
    assign pattern_matched = ~(|((waveform ^ trigger_pattern) & trigger_mask));
    
    wire arm_signal_PosEdge, pattern_matched_PosEdge;
    reg arm_signal_delay, pattern_matched_delay;
    initial begin
        arm_signal_delay = 1'b0;
        pattern_matched_delay = 1'b0;
    end
    assign arm_signal_PosEdge = (arm_signal & ~arm_signal_delay);
    assign pattern_matched_PosEdge = (pattern_matched & ~pattern_matched_delay);

    always @ (posedge CLK100MHZ)
        begin
            arm_signal_delay <= arm_signal;
            pattern_matched_delay <= pattern_matched;
        end

    
    wire [FIFO_WIDTH-1:0] fifo_dout;
    reg [FIFO_ADDRESS_WIDTH-1:0] fifo_address_to_write;
    reg wr_en;
    
    blk_mem_gen_0 waveform_fifo(
        .clka(~CLK100MHZ),
        .addra(fifo_address_to_write),
        .dina(waveform),
        .wea(wr_en),
        .douta(fifo_dout)
    );
      
    ////////////////////////////////////////////////////////////////
    // Finite State Machine
    ////////////////////////////////////////////////////////////////
    reg [2:0] main_state;
    parameter MAIN_IDLE = 'd2;
    parameter MAIN_ARMED = 'd3;
    reg [WAVEFORM_COUNTER_WIDTH-1:0] points_to_capture;

    parameter MAIN_DATA_CAPTURING = 'd4;
    parameter MAIN_COLLECT_DATA ='d5;
    parameter MAIN_SEND_DATA = 'd6;

    parameter TX_REPEAT = TX_WAVEFORM_BUFFER_WIDTH / FIFO_WIDTH; // 128*8/16=64
    parameter TX_REPEAT_COUNTER_BITS = 7;
//    parameter TX_REPEAT_COUNTER_BITS = bits_to_represent(TX_REPEAT);
    reg [TX_REPEAT_COUNTER_BITS-1:0] tx_repeat_counter;    

    parameter NUMBER_OF_BLOCKS_TO_SEND = (FIFO_WIDTH*FIFO_DEPTH)/TX_WAVEFORM_BUFFER_WIDTH; // 16*1024/128 = 128
    parameter NUMBER_OF_BLOCKS_TO_SEND_COUNTER_WIDTH = 8;
    reg [NUMBER_OF_BLOCKS_TO_SEND_COUNTER_WIDTH-1:0] blocks_to_send_counter;
  
    reg [FIFO_ADDRESS_WIDTH-1:0] fifo_address_to_stop_reading;

    
    initial
        begin
            main_state <= MAIN_IDLE;
            armed <= 1'b0;
            triggered <= 1'b0;
            wr_en <= 1'b0;
            tx_repeat_counter <= 'd0;
//            blocks_to_send_counter <= 'd0;
            TX_waveform_buffer_ready <= 1'b0;
            fifo_address_to_write <= -'d1;
        end
        
    always @ (posedge CLK100MHZ)
        if (esc_char_detected == 1'b1) begin
            if (esc_char == "C") begin
                main_state <= MAIN_IDLE;
            end
            else if (esc_char == "A") begin
                wr_en <= 1'b1;
                main_state <= MAIN_ARMED;
            end
            else if ((esc_char == "W") && (triggered == 1'b1)) begin
//                blocks_to_send_counter <= NUMBER_OF_BLOCKS_TO_SEND;
                tx_repeat_counter <= TX_REPEAT;
                fifo_address_to_stop_reading <= fifo_address_to_write;
                main_state <= MAIN_COLLECT_DATA;
            end
        end
        else begin
            case (main_state)
                MAIN_IDLE: begin
                        TX_waveform_buffer_ready <= 1'b0;
                        if (arm_signal_PosEdge == 1'b1) begin
                            wr_en <= 1'b1;
                            main_state <= MAIN_ARMED;
                        end
                        else begin
                            wr_en <= 1'b0;
                        end
                    end
                MAIN_ARMED: begin
                        TX_waveform_buffer_ready <= 1'b0;
                        armed <= 1'b1;
                        triggered <= 1'b0;
                        fifo_address_to_write <= fifo_address_to_write + 'd1;
                        wr_en <= 1'b1;
                        if (pattern_matched_PosEdge == 1'b1) begin
                            points_to_capture <= points_to_capture_after_trigger - 'd1;
                            main_state <= MAIN_DATA_CAPTURING;
                        end
                    end
                MAIN_DATA_CAPTURING: begin
                        armed <= 1'b0;
                        triggered <= 1'b1;
                        fifo_address_to_write <= fifo_address_to_write + 'd1;
                        if (points_to_capture > 'd0) begin
                            wr_en <= 1'b1;
                        end
                        else begin
                            wr_en <= 1'b0;
                            main_state <= MAIN_IDLE;
                        end
                        points_to_capture <= points_to_capture - 'd1;
                    end
            
                MAIN_COLLECT_DATA: begin
                        armed <= 1'b0;
                        triggered <= 1'b0;
                        TX_waveform_buffer_ready <= 1'b0;
                        if (tx_repeat_counter > 'd0) begin
                            TX_BUFFER[1:TX_WAVEFORM_BUFFER_WIDTH] <= {TX_BUFFER[FIFO_WIDTH+1:TX_WAVEFORM_BUFFER_WIDTH], fifo_dout[FIFO_WIDTH-1:0]};
                            tx_repeat_counter <= tx_repeat_counter - 'd1;
                            fifo_address_to_write <= fifo_address_to_write + 'd1;
                        end
                        else begin
                            main_state <= MAIN_SEND_DATA;
                        end
                    end
            
                MAIN_SEND_DATA: begin
                        if (TX_FIFO_ready == 1'b1) begin
                            TX_waveform_buffer_ready <= 1'b1;
                            if (fifo_address_to_write == fifo_address_to_stop_reading) begin
                                main_state <= MAIN_IDLE;
                            end
                            else begin
                                tx_repeat_counter <= TX_REPEAT;
                                main_state <= MAIN_COLLECT_DATA;
//                                blocks_to_send_counter <= NUMBER_OF_BLOCKS_TO_SEND;
                            end
                        end
                        

                    end
            
                default: begin
                        main_state <= MAIN_IDLE;
                        TX_waveform_buffer_ready <= 1'b0;
                        wr_en <= 1'b0;
                        armed <= 1'b0;
                        triggered <= 1'b0;
                    end            
            endcase
        end          

    assign main_state_copy = main_state;
endmodule
