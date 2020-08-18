`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/18 19:57:58
// Design Name: 
// Module Name: spi_single_output
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


module spi_single_output
#(
    parameter NUM_CS = 1
)
(
    input wire CLK100MHZ,
    input wire cpol,
    input wire cspol,
    input wire slave_en,
    input wire cs_next,
    input wire sdo,
    input wire sck_next,
    input wire [NUM_CS - 1:0]cs_val,
    output wire sdi,
    inout wire io,
    output wire sck,
    output wire [NUM_CS - 1:0] cs
);

IOBUF #(
    .DRIVE(12), // Specify the output drive strength
    .IBUF_LOW_PWR("FALSE"),             // Low Power - "TRUE", High Performance = "FALSE"
    .IOSTANDARD("DEFAULT"),           // Specify the I/O standard
    .SLEW("SLOW")                      // Specify the output slew rate
) IOBUF_inst (
    .O(sdi),                            // Buffer output
    .IO(io),                            // Buffer inout port (connect directly to top-level port)
    .I(sdo),                            // Buffer input
    .T(slave_en)                        // 3-state enable input, high=input, low=output
);

reg sck_buffer;
reg[NUM_CS -1 :0] cs_buffer;

assign sck = sck_buffer;
assign cs[NUM_CS-1:0] = cs_buffer[NUM_CS-1:0];

always @(posedge CLK100MHZ) begin
    sck_buffer <= sck_next ^ cpol;
end


genvar i;
generate
    for( i = 0; i <= NUM_CS - 1; i++ ) begin
        always @(posedge CLK100MHZ) begin
            cs_buffer[i] <= cs_next ^ cs_val[i];
        end
    end
endgenerate


endmodule
