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

module main(
    input Uart_RXD,
    output Uart_TXD,
    input CLK100MHZ,
    input BTN0,
    input BTN1,
    input BTN2,
    output ck_io_39, ck_io_38, ck_io_37, // DAC0 
    output ck_io_36, ck_io_35, ck_io_34, // DAC1
    output ck_io_6, // LDAC

    output ja_7, //powerdown -> dds1 ioupdate
    inout ja_6, //sdio -> dds1 sdio
    output ja_5, //csb -> dds1 csb
    input ja_4, //reset -> 
    output ja_3, // sclk -> dds1 sclk
    output ja_2, // powerdown2 -> dds1 profile0
    output ja_1, //sdio2 -> dds1 profile1
    output ja_0, // csb2 -> dds1 profile2
    ////
    //****input, output changeded for AD9910****
    ////
    output jb_0,
    output jb_1,
    output jb_2,
    output jb_3,
    output jb_4,
    output jb_5,
    inout jb_6,
    output jb_7,
    output jc_0,
    output jc_1,
    output jc_2,
    output jc_3,
    output jc_4,
    output jc_5,
    output jc_6,
    output jc_7,
    output jd_0,
    output jd_1,
    output jd_2,
    output jd_3,
    output jd_4,
    output jd_5,
    output jd_6,
    output jd_7,
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
        
    
    data_receiver receiver(.RxD(Uart_RXD), .clk(CLK100MHZ), 
        .BTF_Buffer(BTF_Buffer), .BTF_Length(BTF_Length), 
        .CMD_Buffer(CMD_Buffer), .CMD_Length(CMD_Length), .CMD_Ready(CMD_Ready), 
        .esc_char_detected(esc_char_detected), .esc_char(esc_char),
         .wrong_format(wrong_format)
    );
    defparam receiver.BTF_RX_BUFFER_COUNT_WIDTH = BTF_RX_BUFFER_COUNT_WIDTH;
    defparam receiver.BTF_RX_BUFFER_BYTES = BTF_RX_BUFFER_BYTES; // can be between 1 and 2^BTF_RX_BUFFER_COUNT_WIDTH - 1
    defparam receiver.BTF_RX_BUFFER_WIDTH = BTF_RX_BUFFER_WIDTH;
    defparam receiver.ClkFreq = ClkFreq;
    defparam receiver.BaudRate = BaudRate;
    defparam receiver.CMD_RX_BUFFER_BYTES = CMD_RX_BUFFER_BYTES;
    defparam receiver.CMD_RX_BUFFER_WIDTH = CMD_RX_BUFFER_WIDTH;

    /////////////////////////////////////////////////////////////////
    // To send data to PC
    /////////////////////////////////////////////////////////////////

    parameter TX_BUFFER1_BYTES =  4'hf;
    parameter TX_BUFFER1_WIDTH = 8 * TX_BUFFER1_BYTES;
    parameter TX_BUFFER1_LENGTH_WIDTH = bits_to_represent(TX_BUFFER1_BYTES);

    parameter TX_BUFFER2_BYTES = BTF_MAX_BYTES;
    parameter TX_BUFFER2_WIDTH = BTF_MAX_BUFFER_WIDTH;
    parameter TX_BUFFER2_LENGTH_WIDTH = BTF_MAX_BUFFER_COUNT_WIDTH;


    reg [TX_BUFFER1_LENGTH_WIDTH-1:0] TX_buffer1_length;
    reg [1:TX_BUFFER1_WIDTH] TX_buffer1;
    reg TX_buffer1_ready;

    reg [TX_BUFFER2_LENGTH_WIDTH-1:0] TX_buffer2_length;
    reg [1:TX_BUFFER2_WIDTH] TX_buffer2;
    reg TX_buffer2_ready;

    
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
    .TX_FIFO_ready(TX_FIFO_ready),
    .bits_to_send(monitoring_32bits)
);

    defparam sender.ClkFreq = ClkFreq;
    defparam sender.BaudRate = BaudRate;
    defparam sender.TX_BUFFER1_LENGTH_WIDTH = TX_BUFFER1_LENGTH_WIDTH;
    defparam sender.TX_BUFFER1_BYTES =  TX_BUFFER1_BYTES;
    defparam sender.TX_BUFFER1_WIDTH = TX_BUFFER1_WIDTH;
    defparam sender.TX_BUFFER2_LENGTH_WIDTH = TX_BUFFER2_LENGTH_WIDTH;
    defparam sender.TX_BUFFER2_BYTES = TX_BUFFER2_BYTES;
    defparam sender.TX_BUFFER2_WIDTH = TX_BUFFER2_WIDTH;




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
    parameter IDN_REPLY = "DDS_DAC v1_01"; // 13 characters


    /////////////////////////////////////////////////////////////////
    // Command definition for DDS
    /////////////////////////////////////////////////////////////////
    parameter CMD_WRITE_DDS_REG = "WRITE DDS REG"; // 13 characters
    ////
    //****parameter added for AD9910****
    ////
    parameter CMD_IOUPDATE_DDS_REG = "DDS IO UPDATE"; // 13 characters. this was added for IO UPDATE 
    
    ////
    //****parameter added for AD9910 parallel mode****
    ////
    parameter CMD_DDS_PROFILE_WRITE = "WRITE DDS PRO"; // 13 characters. this writes in FIFO
    
    parameter CMD_DDS_PROFILE_FORCE = "FORCE DDS PRO"; // 11 characters. this sets DDS profile
    
    parameter CMD_DDS_COUNTER = "RESET DDS COUNTER";// 14 characters. this reset FIFO and counter to 0
    
    reg[2:0]DDS1_profile_input;
    reg[2:0]DDS2_profile_input;
    wire[2:0]DDS1_profile_buffer;
    wire[2:0]DDS2_profile_buffer;
    initial begin
        DDS1_profile_input <= 0;
        DDS2_profile_input <= 0;
    end
    
    assign DDS1_profile_buffer = BTF_Buffer[2:0];
    assign DDS2_profile_buffer = BTF_Buffer[6:4];
        
    parameter CMD_DDS_PARALLEL_WRITE = "WRITE DDS PAR"; // 13 characters. this writes in Parallel FIFO
    
    parameter CMD_DDS_PARALLEL_FORCE = "FORCE DDS PAR"; // 13 characters. this supply parallel value directly
    
    parameter CMD_DDS_FIFO_FLUSH = "FLUSH DDS PAR"; // 13 characters. this flush Parallel FIFO
    
    parameter PARALLEL_LENGTH = 18;
    parameter COUNTER_LENGTH = 64;
    parameter FIFO_DEPTH = 1024;
        
    
    reg [PARALLEL_LENGTH + COUNTER_LENGTH + 1:0]fifo_input;
    reg[PARALLEL_LENGTH - 1:0] force_value_input;
    reg[PARALLEL_LENGTH - 1:0] force_select;
    reg reset_parallel, fifo_flush, fifo_write;
    wire[PARALLEL_LENGTH - 1:0] parallel_output;
    wire DDS1_pdclk;
    
    initial begin
        fifo_input <= 0;
        reset_parallel <= 0;
        fifo_flush <= 0;
        fifo_write <= 0;
        force_value_input <= 0;
        force_select <= 0;
    end
    
    assign DDS1_pdclk = ja_4;
    
    dds_parallel_write
    #(
        .PARALLEL_LENGTH(PARALLEL_LENGTH),
        .COUNTER_LENGTH(COUNTER_LENGTH),
        .FIFO_DEPTH(FIFO_DEPTH)
    )
    (
        .clk(CLK100MHZ),
        .pdclk(DDS1_pdclk),
        .force_value_input(force_value_input),
        .force_select(force_select),
        .fifo_flush(fifo_flush),
        .reset(reset_parallel),
        .fifo_write(fifo_write),
        .fifo_input(fifo_input),
        .parallel_output(parallel_output)
        );

    ////
    //****parameter changeded for AD9910****
    ////
    parameter DDS_MAX_LENGTH = 9;
    parameter DDS_WIDTH = DDS_MAX_LENGTH * 8;
    
    reg dds_data_ready_1, dds_data_ready_2;
    initial begin
        dds_data_ready_1 <= 1'b0;
        dds_data_ready_2 <= 1'b0;
    end

    reg [DDS_WIDTH+8:1] DDS_buffer; // Buffer to capture BTF_Buffer
    wire DDS1_update, DDS2_update;
    assign {DDS1_update, DDS2_update} = BTF_Buffer[DDS_WIDTH+6:DDS_WIDTH+5]; // This wire should probe BTF_Buffer directly because until BTF_Buffer will be captured, the data won't be correct
    
    wire [3:0] data_length;
    assign data_length = DDS_buffer[DDS_WIDTH+4:DDS_WIDTH+1];
    wire [DDS_WIDTH-1:0] DDS_data;
    assign DDS_data = DDS_buffer[DDS_WIDTH:1];
        
    reg [3:0] DDS_slow_clock;
    initial DDS_slow_clock <= 'd0;
    
    always @ (posedge CLK100MHZ) DDS_slow_clock <= DDS_slow_clock + 'd1;
    wire DDS_clock;
    assign DDS_clock = DDS_slow_clock[3];
    
    wire DDS_busy_1, DDS_busy_2;
    wire rcsbar_1, rcsbar_2;
    wire rsdio_1, rsdio_2;
    wire rsclk;
    assign rsclk = DDS_clock & (~rcsbar_1 | ~rcsbar_2);

    WriteToRegister WTR1(.DDS_clock(DDS_clock), .dataLength(data_length[3:0]), .registerData(DDS_data), .registerDataReady(dds_data_ready_1), .busy(DDS_busy_1),
                                .wr_rcsbar(rcsbar_1), /*.rsclk(rsclk00),*/ .rsdio(rsdio_1) ); //, .extendedDataReady(extendedDataReady00));   //, .countmonitor(monitor00), .registerDataReadymonitor(RDataReadymonitor00)
                                //);

    WriteToRegister WTR2(.DDS_clock(DDS_clock), .dataLength(data_length[3:0]), .registerData(DDS_data), .registerDataReady(dds_data_ready_2), .busy(DDS_busy_2),
                                .wr_rcsbar(rcsbar_2), /*.rsclk(rsclk00),*/ .rsdio(rsdio_2) ); //, .extendedDataReady(extendedDataReady00));   //, .countmonitor(monitor00), .registerDataReadymonitor(RDataReadymonitor00)
                                //);
                                   
    reg DDS1_ioupdate, DDS2_ioupdate, DDS_reset;    // powerdown pins were replaced to IO UPDATE pin becuase powerdoen was not used
    parameter IO_UPDATE_COUNT_LENGTH = 3;
    parameter IO_UPDATE_BTF_LENGTH = 1;
    reg[IO_UPDATE_COUNT_LENGTH-1:0] io_update_count;   // to make io update duration sufficienlt long
    
    initial {DDS1_ioupdate, DDS2_ioupdate, DDS_reset} <= 3'h0;
                                      
    assign {ja_7, ja_6, ja_5, ja_3, ja_2, ja_1, ja_0}  = {DDS1_ioupdate, rsdio_1, rcsbar_1, rsclk, DDS2_profile[0], DDS2_profile[1], DDS2_profile[2]};
    assign {jb_7, jb_6, jb_5, jb_4, jb_3, jb_2, jb_1, jb_0}  = {DDS2_ioupdate, rsdio_2, rcsbar_2, parallel_output[PARALLEL_LENGTH-1], parallel_output[PARALLEL_LENGTH-2], DDS1_profile[0], DDS1_profile[1], DDS1_profile[2]};
    
    /////////////////////////////////////////////////////////////////
    // Command definition for DAC
    /////////////////////////////////////////////////////////////////
    parameter CMD_WRITE_DAC_REG = "WRITE DAC REG"; // 13 characters
    parameter DAC_DATA_WIDTH = 24;
    

    reg [7:0] DAC_start;
    initial DAC_start[7:0] <= 8'd0;

    reg [DAC_DATA_WIDTH+8:1] DAC_buffer;
    
    wire [7:0] DAC_update;
    assign DAC_update[7:0] = BTF_Buffer[DAC_DATA_WIDTH+8:DAC_DATA_WIDTH+1];
    wire [DAC_DATA_WIDTH:1] DAC_data;
    assign DAC_data = DAC_buffer[DAC_DATA_WIDTH:1];
    
    reg [1:0] DAC_slow_clock;
    initial DAC_slow_clock <= 'd0;
    always @ (posedge CLK100MHZ) DAC_slow_clock <= DAC_slow_clock + 'd1;
    wire DAC_clock;
    assign DAC_clock = DAC_slow_clock[0]; // DAC_slow_clock[1]: 25MHz, DAC_slow_clock[0]: 50MHz

    wire [1:0] DAC_busy, DAC_sclk, DAC_cs_bar, DAC_sdi; 

    genvar i;
    generate
        for (i=0; i<2; i=i+1) begin
            DAC8734 dac(.clock(DAC_clock), .start_trigger(DAC_start[i]), 	.data(DAC_data),
                .sclk(DAC_sclk[i]), .cs_bar(DAC_cs_bar[i]), .sdi(DAC_sdi[i]), .busy(DAC_busy[i]) );
        end
    endgenerate

    reg ldac_bar; // Minimum 15ns for 3.6V < DV_DD ¡Â 5.5V, 2.7V ¡Â IOV_DD ¡Â DV_DD
    initial ldac_bar = 1'b1;
    assign ck_io_6 = ldac_bar;
    
    assign {ck_io_39, ck_io_38, ck_io_37} = {DAC_cs_bar[0], DAC_sclk[0], DAC_sdi[0]};
    assign {ck_io_36, ck_io_35, ck_io_34} = {DAC_cs_bar[1], DAC_sclk[1], DAC_sdi[1]};


    parameter CMD_LDAC = "LDAC"; // 4 characters
    parameter CMD_UPDATE_LDAC_LENGTH = "LDAC LENGTH"; // 1 characters

    reg [7:0] ldac_length;
    initial ldac_length <= 40;
    reg [7:0] ldac_pause_count; // (LDAC_length+2)*10ns. LDAC signal is distributed to 8 chips, so for the output to swing down enough, pulse should be longer than 200ns when 2 chips were populated   




    /////////////////////////////////////////////////////////////////
    // Command definition for DNA_PORT command
    /////////////////////////////////////////////////////////////////
    parameter CMD_DNA_PORT = "DNA_PORT";
    wire [63:0] DNA_wire;
    device_DNA device_DNA_inst(
        .clk(CLK100MHZ),
        .DNA(DNA_wire) // If 4 MSBs == 4'h0, DNA_PORT reading is not finished. If 4 MSBs == 4'h1, DNA_PORT reading is done 
    );
    
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
    parameter MAIN_DDS_WAIT_FOR_BUSY_ON = 4'h1;
    parameter MAIN_DDS_WAIT_FOR_BUSY_OFF = 4'h2;
    
    parameter MAIN_DAC_WAIT_FOR_BUSY_ON = 4'h3;
    parameter MAIN_DAC_WAIT_FOR_BUSY_OFF = 4'h4;
    parameter MAIN_DAC_LDAC_PAUSE = 4'h5;
    parameter MAIN_DAC_LDAC_OFF = 4'h6;
   
    ////
    //****parameter added for AD9910**** this if statement is for IO UPDATE of AD9910
    ////
    parameter MAIN_DDS_IOUPDATE_OUT = 4'h7;
    parameter MAIN_DDS_PARALLEL_WRITE = 4'h8; // 13 characters. this writes in FIFO
    parameter MAIN_DDS_PARALLEL_FORCE = 4'h9;
    parameter MAIN_DDS_FIFO_FLUSH = 4'h10; // 14 characters. this flush FIFO
    parameter MAIN_DDS_PARALLEL_RESET = 4'h11;// 14 characters. this reset FIFO and counter to 0


    parameter MAIN_UNKNOWN_CMD =4'hf;
    

    initial begin
        main_state <= MAIN_IDLE;
        patterns <= 'd0;
        TX_buffer1_ready <= 1'b0;
        TX_buffer2_ready <= 1'b0;
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


                        else if ((CMD_Length == $bits(CMD_WRITE_DDS_REG)/8) && (CMD_Buffer[$bits(CMD_WRITE_DDS_REG):1] == CMD_WRITE_DDS_REG)) begin
                            if (BTF_Length != (DDS_MAX_LENGTH+1)) begin
                                TX_buffer1[1:13*8] <= {"Wrong length", BTF_Length[7:0]}; // Assuming that BTF_Length is less than 256
                                TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= 'd13;
                                TX_buffer1_ready <= 1'b1;
                            end
                            else if ((DDS1_update != 0) || (DDS2_update != 0)) begin
                                DDS_buffer <=  BTF_Buffer[DDS_WIDTH+8:1]; // Buffer to capture BTF_Buffer
                                main_state <= MAIN_DDS_WAIT_FOR_BUSY_ON;
                                dds_data_ready_1 <= DDS1_update;
                                dds_data_ready_2 <= DDS2_update;
                            end
                        end
                        
                        ////
                        //****code added for AD9910**** this if statement is for IO UPDATE of AD9910
                        ////
                        else if ((CMD_Length == $bits(CMD_IOUPDATE_DDS_REG)/8) && (CMD_Buffer[$bits(CMD_IOUPDATE_DDS_REG):1] == CMD_IOUPDATE_DDS_REG)) begin
                            if (BTF_Length != (DDS_MAX_LENGTH+1)) begin
                                TX_buffer1[1:13*8] <= {"Wrong length", BTF_Length[7:0]}; // Assuming that BTF_Length is less than 256
                                TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= 'd13;
                                TX_buffer1_ready <= 1'b1;
                            end
                            else if ((DDS1_update != 0) || (DDS2_update != 0)) begin
                                main_state <= MAIN_DDS_IOUPDATE_OUT;
                                io_update_count <= 'd5;
                                DDS1_ioupdate <= DDS1_update;
                                DDS2_ioupdate <= DDS2_update;
                            end
                        end
                        
                        else if ((CMD_Length == $bits(CMD_DDS_PROFILE_SET)/8) && (CMD_Buffer[$bits(CMD_DDS_PROFILE_SET):1] == CMD_DDS_PROFILE_SET)) begin
                            if (BTF_Length != (DDS_MAX_LENGTH+1)) begin
                                TX_buffer1[1:13*8] <= {"Wrong length", BTF_Length[7:0]}; // Assuming that BTF_Length is less than 256
                                TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= 'd13;
                                TX_buffer1_ready <= 1'b1;
                            end
                            else if ((DDS1_update != 0) || (DDS2_update != 0)) begin
                                main_state <= MAIN_IDLE;
                                if( DDS1_update == 1'b1 ) begin
                                    DDS1_profile <= DDS1_profile_buffer;
                                end
                                
                                if( DDS2_update == 1'b1 ) begin
                                    DDS2_profile <= DDS2_profile_buffer;
                                end
                            end
                        end



                        else if ((CMD_Length == $bits(CMD_WRITE_DAC_REG)/8) && (CMD_Buffer[$bits(CMD_WRITE_DAC_REG):1] == CMD_WRITE_DAC_REG)) begin
                            if (BTF_Length != ((DAC_DATA_WIDTH+8)/8)) begin
                                TX_buffer1[1:13*8] <= {"Wrong length", BTF_Length[7:0]}; // Assuming that BTF_Length is less than 256
                                TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= 'd13;
                                TX_buffer1_ready <= 1'b1;
                            end
                            else if (DAC_update != 'd0) begin
                                DAC_buffer <= BTF_Buffer[DAC_DATA_WIDTH+8:1];
                                main_state <= MAIN_DAC_WAIT_FOR_BUSY_ON;
                                DAC_start[7:0] <= DAC_update[7:0];
                            end
                        
                        end

                        else if ((CMD_Length == $bits(CMD_LDAC)/8) && (CMD_Buffer[$bits(CMD_LDAC):1] == CMD_LDAC)) begin
                            ldac_bar <= 1'b0;
                            ldac_pause_count <= ldac_length;
                            main_state <= MAIN_DAC_LDAC_PAUSE;
                        end

                        else if ((CMD_Length == $bits(CMD_UPDATE_LDAC_LENGTH)/8) && (CMD_Buffer[$bits(CMD_UPDATE_LDAC_LENGTH):1] == CMD_UPDATE_LDAC_LENGTH)) begin
                            ldac_length[7:0] <= BTF_Buffer[8:1];
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

                        else if ((CMD_Length == $bits(CMD_DNA_PORT)/8) && (CMD_Buffer[$bits(CMD_DNA_PORT):1] == CMD_DNA_PORT)) begin
                            TX_buffer1[1:64] <= DNA_wire;
                            TX_buffer1_length[TX_BUFFER1_LENGTH_WIDTH-1:0] <= 8;
                            TX_buffer1_ready <= 1'b1;
                            main_state <= MAIN_IDLE;
                        end
                        
                        else if ((CMD_Length == $bits(CMD_DDS_PARALLEL_FORCE)/8) && (CMD_Buffer[$bits(CMD_DDS_PARALLEL_FORCE):1] == CMD_DDS_PARALLEL_FORCE)) begin
                            main_state <= MAIN_DDS_PARALLEL_FORCE;
                            force_select <= 1;
                        end
                            
                        


                        else begin
                            main_state <= MAIN_UNKNOWN_CMD;
                        end
                    end
                    else begin
                        TX_buffer1_ready <= 1'b0;
                        TX_buffer2_ready <= 1'b0;
                    end
                    



                MAIN_DDS_WAIT_FOR_BUSY_ON: begin
                        if ((DDS_busy_1 | DDS_busy_2) == 1) begin
                            main_state <= MAIN_DDS_WAIT_FOR_BUSY_OFF;
                            dds_data_ready_1 <= 1'b0;
                            dds_data_ready_2 <= 1'b0;
                        end
                    end

                MAIN_DDS_WAIT_FOR_BUSY_OFF: begin
                        if ((DDS_busy_1 & DDS_busy_2) == 0) main_state <= MAIN_IDLE;
                    end


                MAIN_DAC_WAIT_FOR_BUSY_ON: begin
                        if (DAC_busy != 'd0) begin
                            main_state <= MAIN_DAC_WAIT_FOR_BUSY_OFF;
                            DAC_start[7:0] <= 8'd0;
                        end
                    end


                MAIN_DAC_WAIT_FOR_BUSY_OFF: begin
                        if (DAC_busy == 'd0) main_state <= MAIN_IDLE;
                    end

                MAIN_DAC_LDAC_PAUSE: begin // ldac should be low for at least 15ns
                        if (ldac_pause_count == 0) main_state <= MAIN_DAC_LDAC_OFF;
                        ldac_pause_count <= ldac_pause_count - 'd1;
                    end

                MAIN_DAC_LDAC_OFF: begin
                        ldac_bar <= 1'b1;
                        main_state <= MAIN_IDLE;
                    end
                ////
                //****code added for AD9910**** this if statement is for IO UPDATE of AD9910
                ////
                MAIN_DDS_IOUPDATE_OUT: begin
                    DDS1_ioupdate <= DDS1_ioupdate;
                    DDS2_ioupdate <= DDS2_ioupdate;
                    io_update_count <= io_update_count - 'd1;
                    if( io_update_count == 0 ) begin
                        DDS1_ioupdate <= 1'b0;
                        DDS2_ioupdate <= 1'b0;
                        main_state <= MAIN_IDLE;
                        end
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




    assign {d0, d1, d2, d3, d4, d5} = 6'h00;
    assign {led, red1, green1, blue1, red0, green0, blue0} = patterns[1:10];
    assign monitoring_32bits = patterns[1:32];

    //assign led[5:2] = main_state[3:0];
 
endmodule
