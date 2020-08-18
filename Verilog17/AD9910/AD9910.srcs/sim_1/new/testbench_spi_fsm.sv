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
wire sdi;
wire sdo;
wire cpha;
wire cpol;
wire cspol;
wire slave_en;
wire cs_next;
wire sck_next;
wire[0:0] cs_val;
wire io;
wire sck;
wire [0:0] cs;
logic io_val;

assign io = (~slave_en)? 1'bz:io_val;

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
    //.off_spi(off_spi),
    .sck_next(sck_next),
    .cs_val(cs_val)
);

spi_single_output
#(
    .NUM_CS(1)
)
spi_single_output_0
(
    .CLK100MHZ(CLK100MHZ),
    .cpol(cpol),
    .cspol(cspol),
    .slave_en(slave_en),
    .cs_next(cs_next),
    .sdo(sdo),
    .sck_next(sck_next),
    .cs_val(cs_val),
    .sdi(sdi),
    .io(io),
    .sck(sck),
    .cs(cs)
);

always begin
    #5
    CLK100MHZ = ~CLK100MHZ;
end

initial begin
    
    CLK100MHZ = 1;
    spi_config_in = 0;
    spi_config_selected = 0;
    spi_data_in = 0;
    spi_data_selected = 0;
    io_val = 0;
    #15
    spi_config_in = 32'd1 << 31 | 32'd0 << 29 |  32'd1 << 16 |  32'd31 << 11 | 32'd0 << 8 | 32'd8;
    spi_config_selected = 1'b1;
    #10
    spi_config_selected = 1'b0;
    #20
    spi_data_in = 32'b10111111111111110000001111001101;
    spi_data_selected = 1'b1;
    #10
    spi_data_selected = 1'b0;
    
    #3000
    spi_config_in = 32'd1 << 31 | 32'd1 << 29 |  32'd1 << 16 |  32'd7 << 11 | 32'd1 << 8 | 32'd8;
    spi_config_selected = 1'b1;
    #10
    spi_config_selected = 1'b0;
    #20
    spi_data_in = 32'b00110111111111110000001111001101;
    spi_data_selected = 1'b1;
    #10
    spi_data_selected = 1'b0;
    
    
    #3000
    spi_config_in = 32'd0 << 31 | 32'd1 << 30 | 32'd0 << 29 |  32'd1 << 16 |  32'd7 << 11 | 32'd1 << 8 | 32'd8;
    spi_config_selected = 1'b1;
    #10
    spi_config_selected = 1'b0;
    #20
    spi_data_in = 32'b0;
    spi_data_selected = 1'b1;
    #10;
    spi_data_selected = 1'b0;
    io_val = 1;
    #40;
    io_val = 0;
    #80
    io_val = 1;
    #80
    io_val = 0;
    #80
    io_val = 0;
    #80
    io_val = 1;
    #80
    io_val = 0;
    
    #3000
    spi_config_in = 32'd0 << 31 | 32'd1 << 30 | 32'd1 << 29 |  32'd1 << 16 |  32'd7 << 11 | 32'd0 << 8 | 32'd8;
    spi_config_selected = 1'b1;
    #10
    spi_config_selected = 1'b0;
    #20
    spi_data_in = 32'b0;
    spi_data_selected = 1'b1;
    #10;
    spi_data_selected = 1'b0;
    io_val = 1;
    #120;
    io_val = 0;
    #80
    io_val = 1;
    #80
    io_val = 0;
    #80
    io_val = 0;
    #80
    io_val = 1;
    #80
    io_val = 0;
end

endmodule
