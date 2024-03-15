`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2017/12/21 16:16:04
// Design Name: 
// Module Name: led_intensity_adjust
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


module led_intensity_adjust(
    output reg led0_r,
    output reg led0_g,
    output reg led0_b,
    output reg led1_r,
    output reg led1_g,
    output reg led1_b,
    input red0,
    input green0,
    input blue0,
    input red1,
    input green1,
    input blue1,
    input [7:0] intensity,
    input CLK100MHZ
    );

    reg [7:0] counter;
    
    initial begin
        counter = 'd0;
    end
    
    always @ (posedge CLK100MHZ) begin
            if (counter <= intensity) begin
                led0_r <= red0;
                led0_g <= green0;
                led0_b <= blue0;
                led1_r <= red1;
                led1_g <= green1;
                led1_b <= blue1;
            end
            else begin
                led0_r <= 1'b0;
                led0_g <= 1'b0;
                led0_b <= 1'b0;
                led1_r <= 1'b0;
                led1_g <= 1'b0;
                led1_b <= 1'b0;
            end
            counter <= counter + 'd1;
        end

endmodule
