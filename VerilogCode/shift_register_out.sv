`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/17 20:01:59
// Design Name: 
// Module Name: shift_register_out
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


module shift_register_out(
    input wire CLK100MHZ,
    input wire reset,
    input wire lsb_first,
    input wire data_load,
    input wire [31:0] data_in,
    input wire write,
    output wire sdo
    );

reg [33:0] data;

assign sdo = (lsb_first)? data[0]:data[33];

always @(posedge CLK100MHZ) begin
    if(reset) begin
        data[33:0] <= 34'h0;
    end
    else begin
        if(write == 1'b1) begin
            data[33:0] <= {1'b0,data_in[31:0],1'b0};
        end
        else if(data_load == 1'b1) begin
            if( lsb_first == 1'b1 ) begin
                data[33:0] <= {1'b0, data[33:1]};
            end
            
            else begin
                data[33:0] <= {data[32:0], 1'b0};
            end
        end
    end
end
endmodule
