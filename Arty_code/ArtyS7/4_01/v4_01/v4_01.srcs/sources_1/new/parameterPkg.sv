package parameterPkg;
    /////////////////////////////////////////////////////////////////
    // Global setting
    /////////////////////////////////////////////////////////////////
    parameter BTF_MAX_BYTES = 9'h100;
    parameter BTF_MAX_BUFFER_WIDTH = 8 * BTF_MAX_BYTES;
    //parameter BTF_MAX_BUFFER_COUNT_WIDTH = bits_to_represent(BTF_MAX_BYTES);
    parameter BTF_MAX_BUFFER_COUNT_WIDTH = 9;
    

    // Settings related to capture waveform data
    parameter WAVEFORM_WIDTH = 16;
    parameter WAVEFORM_MAX_DEPTH = 1024-1; // So that the triggered bit will still remain in the fifo
    //parameter WAVEFORM_COUNTER_WIDTH = bits_to_represent(WAVEFORM_MAX_DEPTH);
    parameter WAVEFORM_COUNTER_WIDTH = 10;

    /////////////////////////////////////////////////////////////////
    // To receive data from PC
    /////////////////////////////////////////////////////////////////
    parameter BTF_RX_BUFFER_COUNT_WIDTH = BTF_MAX_BUFFER_COUNT_WIDTH;
    parameter CMD_RX_BUFFER_BYTES = 4'hf;
    parameter CMD_RX_BUFFER_WIDTH = 8 * CMD_RX_BUFFER_BYTES;
    
    parameter BTF_RX_BUFFER_BYTES = BTF_MAX_BYTES;
    parameter BTF_RX_BUFFER_WIDTH = BTF_MAX_BUFFER_WIDTH;



    /////////////////////////////////////////////////////////////////
    // To send data to PC
    /////////////////////////////////////////////////////////////////

    parameter TX_BUFFER1_BYTES =  4'hf;
    parameter TX_BUFFER1_WIDTH = 8 * TX_BUFFER1_BYTES;
    //parameter TX_BUFFER1_LENGTH_WIDTH = bits_to_represent(TX_BUFFER1_BYTES);
    parameter TX_BUFFER1_LENGTH_WIDTH = 4;

    parameter TX_BUFFER2_BYTES = BTF_MAX_BYTES;
    parameter TX_BUFFER2_WIDTH = BTF_MAX_BUFFER_WIDTH;
    //parameter TX_BUFFER2_LENGTH_WIDTH = BTF_MAX_BUFFER_COUNT_WIDTH;
    parameter TX_BUFFER2_LENGTH_WIDTH = 9;

    // Settings related to capture waveform data
    parameter TX_WAVEFORM_BUFFER_BYTES =  8'h80;
    parameter TX_WAVEFORM_BTF_HEADER = "#280";
    parameter TX_WAVEFORM_BUFFER_WIDTH = 8 * TX_WAVEFORM_BUFFER_BYTES;
	//parameter TX_WAVEFORM_BUFFER_LENGTH_WIDTH = bits_to_represent(TX_WAVEFORM_BUFFER_BYTES)
	parameter TX_WAVEFORM_BUFFER_LENGTH_WIDTH = 8;

	
    /////////////////////////////////////////////////////////////////
    // Parameters for output data FIFO
    /////////////////////////////////////////////////////////////////
    parameter OUTPUT_FIFO_DATA_WIDTH = 64; // Defined in fifo_generator_bram_64x1024 IP
    parameter OUTPUT_FIFO_DATA_COUNT_WIDTH = 11; // Data length is 1024

	parameter MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE = 512; //// The maximum number of data to read at once => corresponding to 4096 bytes requiring 13 bits. Consider that the maximum size of FIFO in the data_sender is (8bits x 8192)


	
    /////////////////////////////////////////////////////////////////
    // Sequencer design parameter
    /////////////////////////////////////////////////////////////////
	parameter REGISTER_ADDR_WIDTH = 5;
	parameter REGISTER_WIDTH = 16;


	
    // Sequencer instruction memory
    parameter INSTRUCTION_MEMORY_DATA_WIDTH = 64;
    parameter INSTRUCTION_MEMORY_ADDR_WIDTH = 9;

    // Sequencer output port number
	parameter OUTPUT_PORT_NUMBER = 4;
	parameter OUTPUT_PORT_ADDR_WIDTH = 2;


endpackage : parameterPkg
