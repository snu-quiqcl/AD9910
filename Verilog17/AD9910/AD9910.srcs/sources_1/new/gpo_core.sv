`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/18 21:35:19
// Design Name: 
// Module Name: gpo_core
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


module gpo_core
#(
    parameter DEST_VAL = 15'h0,
    parameter CHANNEL_LENGTH = 12
)
(
    input wire CLK100MHZ,
    input wire override_en,
    input wire selected_en,
    input wire[47:0] override_value,
    input wire counter_matched,
    input wire [111:0] gpo_in,
    input wire busy,
    output wire selected,
    output wire [111:0] error_data,
    output wire overrided,
    output wire busy_error,
    output wire[47:0] gpo_out
    );

reg override_en_state;
reg selected_en_state;
reg [47:0] override_value_reg;
reg [111:0] gpo_out_buffer;

wire selected_wire;
wire dest_check;

assign dest_check = ( gpo_in[96 + CHANNEL_LENGTH - 1:96] == DEST_VAL ) & counter_matched;
assign selected_wire = selected_en_state | ( dest_check & ~override_en );
assign selected = selected_wire;
assign gpo_out[47:0] = (override_en == 1'b1)? override_value_reg[47:0] : {gpo_out_buffer[111:96],gpo_out_buffer[31:0]};
assign error_data[111:0] = gpo_out_buffer[111:0];
assign overrided = dest_check & override_en;
assign busy_error = busy & selected_wire;

always @(posedge CLK100MHZ) begin
    override_en_state <= override_en;
    selected_en_state <= selected_en;
    if( selected_wire & ~busy ) begin
        gpo_out_buffer[111:0] <= gpo_in[111:0];
    end
    if( override_en ) begin
        override_value_reg[47:0] <= override_value;
    end
end

endmodule
