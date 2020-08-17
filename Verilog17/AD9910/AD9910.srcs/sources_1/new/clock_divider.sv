`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/17 21:17:35
// Design Name: 
// Module Name: clock_divider
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


module clock_divider(
    input wire CLK100MHZ,
    input wire [7:0] divide,
    input wire count_enable,
    output wire count_end
    );

reg[7:0] count;
assign count_end = (count == 8'h0);
always @(posedge CLK100MHZ) begin
    if(count_enable == 1'b1) begin
        count[7:0] <= count[7:0] - 8'h1;
        if( count[7:0] == 8'h0 ) begin
            count[7:0] <= {1'b0,divide[7:1]} - 8'h1;
        end
    end
    
    else begin
        count[7:0] <= {1'b0,divide[7:1]} - 8'h1;
    end
end

endmodule
