`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2018/02/01 23:09:22
// Design Name: 
// Module Name: mux2
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


module mux2 #(parameter WIDTH=16)
    (
    input [WIDTH-1:0] d0, d1,
    input select,
    output logic [WIDTH-1:0] y
    );
    always_comb
        case(select)
            0: y=d0;
            1: y=d1;
        endcase
endmodule
