`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/17 20:31:16
// Design Name: 
// Module Name: shift_register_in
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


module shift_register_in(
    input wire CLK100MHZ,
    input wire reset,
    input wire lsb_first,
    input wire data_load,
    input wire sdi,
    input wire clear_register,
    output wire [31:0] data_out
    );
    
reg[31:0] data;
assign data_out[31:0] = data[31:0];

always@(posedge CLK100MHZ) begin
    if(reset) begin
        data[31:0] <= 32'h0;
    end
    else begin
        if( clear_register == 1'b1) begin
            data[31:0] <= 32'b0;
        end
        else if(data_load == 1'b1) begin
            if(lsb_first == 1'b1) begin
                data[31:0] <= {data[30:0], sdi};
            end
            else begin
                data[31:0] <= {sdi,data[31:1]};
            end
        end
    end
end

endmodule
