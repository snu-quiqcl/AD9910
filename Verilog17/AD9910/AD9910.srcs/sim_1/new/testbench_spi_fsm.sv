`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/17 21:45:24
// Design Name: 
// Module Name: testbench_spi_fsm
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


module testbench_spi_fsm;

logic CLK100MHZ;
logic[31:0] spi_config_in;
logic spi_config_selected;
logic[31:0] spi_data_in;
logic spi_data_selected;
logic busy;
logic [31:0] spi_data_out;
logic data_write;
logic sdi;
logic sdo;
logic cpha;
logic cpol;
logic cspol;
logic slave_en;
logic cs_next;
logic off_spi;
logic sck_next;
logic cs;

spi_fsm_module
#(
    .NUM_CS(1)
)
spi_fsm_module_0
(
    .CLK100MHZ(CLK100MHZ),
    .spi_config_in(spi_config_in),
    .spi_config_selected(spi_config_selected),
    .spi_data_in(spi_data_in),
    .spi_data_selected(spi_data_selected),
    .busy(busy),
    .spi_data_out(spi_data_out),
    .data_write(data_write),
    .sdi(sdi),
    .sdo(sdo),
    .cpha(cpha),
    .cpol(cpol),
    .cspol(cspol),
    .slave_en(slave_en),
    .cs_next(cs_next),
    .off_spi(off_spi),
    .sck_next(sck_next),
    .cs(cs)
);

always begin
    #5
    CLK100MHZ = ~CLK100MHZ;
end

initial begin
    CLK100MHZ = 0;
    spi_config_in = 0;
    spi_config_selected = 0;
    spi_data_in = 0;
    spi_data_selected = 0;
    #15
    spi_config_in = 32'd1 << 28 |  32'd1 << 16 |  32'd32 << 11 | 32'd8;
    spi_config_selected = 1'b1;
    #10
    spi_config_selected = 1'b0;
    #20
    spi_data_in = 32'b1111001101;
    spi_data_selected = 1'b1;
    #10
    spi_data_selected = 1'b0;
end

endmodule
