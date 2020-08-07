`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/07 06:05:51
// Design Name: 
// Module Name: testbench_for_AD9910
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


module testbench_for_AD9910;

logic DDS_clock;
logic [3:0] data_length;
logic [63:0]DDS_data;
logic dds_data_ready_1;
logic DDS_busy_1;
logic rcsbar_1;
logic rsdio_1;

always begin 
    #1 DDS_clock = ~DDS_clock;
end

WriteToRegister WTR1(
    .DDS_clock(DDS_clock), 
    .dataLength(data_length[3:0]), 
    .registerData(DDS_data), 
    .registerDataReady(dds_data_ready_1), 
    .busy(DDS_busy_1),
    .wr_rcsbar(rcsbar_1), 
    .rsdio(rsdio_1) 
    );
    
initial begin
    DDS_clock = 0;
    DDS_data = 0;
    data_length = 0;
    dds_data_ready_1 = 0;
end

endmodule
