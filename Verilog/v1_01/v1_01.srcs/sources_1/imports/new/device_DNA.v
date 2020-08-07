`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2018/07/06 12:14:21
// Design Name: 
// Module Name: device_DNA
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


module device_DNA(
    input clk,
    output [63:0] DNA // If 4 MSBs == 4'h0, DNA_PORT reading is not finished. If 4 MSBs == 4'h1, DNA_PORT reading is done 
    );
    
    reg DNA_PORT_read, DNA_PORT_shift;
    reg [63:0] DNA_PORT_value;
    assign DNA = DNA_PORT_value;
    
    wire DNA_PORT_out;
    reg [5:0] DNA_PORT_counter;
    
    
    
    // Example from DNA_PORT" section in ug953-vivado-7series-libraries.pdf
    //
    // DNA_PORT: Device DNA Access Port
    // 7 Series
    // Xilinx HDL Language Template, version 2017.3
    DNA_PORT #(
    .SIM_DNA_VALUE(57'h000000000000000) // Specifies a sample 57-bit DNA value for simulation
    )
    DNA_PORT_inst (
    .DOUT(DNA_PORT_out), // 1-bit output: DNA output data.
    .CLK(clk), // 1-bit input: Clock input.
    .DIN(1'b0), // 1-bit input: User data input pin.
    .READ(DNA_PORT_read), // 1-bit input: Active high load DNA, active low read input.
    .SHIFT(DNA_PORT_shift) // 1-bit input: Active high shift enable input.
    );
    // End of DNA_PORT_inst instantiation


    reg [3:0] state;
    parameter START = 4'h0;    
    parameter DNA_PORT_READ = 4'h1;
    parameter DNA_PORT_SHIFT = 4'h2;
    parameter DNA_PORT_FINISHED = 4'h3;

    initial begin
        state <= START;
        DNA_PORT_counter <= 6'b111111; // Initial count to wait
        DNA_PORT_read <= 1'b0;
        DNA_PORT_shift <= 1'b0;
    end


    always @ (negedge clk)
        case (state)
            START: // Wait for 31 clocks before reading DNA_PORT just to make sure that the FPGA is stable enough
                begin
                    if (DNA_PORT_counter == 6'd0) begin
                        state <= DNA_PORT_READ;
                        DNA_PORT_value <= 64'd0;
                        DNA_PORT_counter <= 6'd56; // This will read total 57 bits

                    end
                    else DNA_PORT_counter <= DNA_PORT_counter - 6'd1;
                end
                
            DNA_PORT_READ:
                begin
                    DNA_PORT_read <= 1'b1;
                    state <= DNA_PORT_SHIFT;
                end
                
            DNA_PORT_SHIFT:
                begin
                    {DNA_PORT_read, DNA_PORT_shift} <= 2'b01;
                    DNA_PORT_value[63-4:0] <= {DNA_PORT_value[62-4:0], DNA_PORT_out};
                    if (DNA_PORT_counter == 6'd0) begin
                        state <= DNA_PORT_FINISHED;
                    end
                    DNA_PORT_counter <= DNA_PORT_counter - 6'd1;
                end
                        
            DNA_PORT_FINISHED:
                begin
                    {DNA_PORT_read, DNA_PORT_shift} <= 2'b00;
                    DNA_PORT_value[63:60] <= 4'h1;
                end
                    
                            
            default:
                state <= START;
        endcase
                            

endmodule
