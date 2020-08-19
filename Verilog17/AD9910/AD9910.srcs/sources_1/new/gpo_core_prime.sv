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


module gpo_core_prime
#(
    parameter DEST_VAL = 15'h0,
    parameter CHANNEL_LENGTH = 12
)
(
    input wire CLK100MHZ,
    input wire override_en,
    input wire selected_en,
    input wire[63:0] override_value,
    input wire counter_matched,
    input wire [127:0] gpo_in,
    input wire busy,
    output wire selected,
    output wire [127:0] error_data,
    output wire overrided,
    output wire busy_error,
    output wire[63:0] gpo_out
    );

reg override_en_state;
reg selected_state;
reg [63:0] override_value_reg;
reg [127:0] gpo_out_buffer;
reg [127:0] error_data_buffer;
reg busy_error_state;
reg overrided_state;

wire selected_wire;
wire dest_check;

assign dest_check = ( gpo_in[96 + CHANNEL_LENGTH - 1:96] == DEST_VAL ) & counter_matched;
assign selected_wire = selected_en | ( dest_check & ~override_en );
assign selected = selected_state;
assign gpo_out[63:0] = (override_en_state == 1'b1)? override_value_reg[63:0] : {gpo_out_buffer[127:96],gpo_out_buffer[31:0]};
assign error_data[127:0] = error_data_buffer[127:0];
//assign overrided = dest_check & override_en;
//assign busy_error = busy & selected_wire;
assign overrided = overrided_state;
assign busy_error = busy_error_state;

always @(posedge CLK100MHZ) begin
    override_en_state <= override_en & ~busy;
    selected_state <= ~busy & selected_wire;
    busy_error_state <= busy & selected_wire;
    overrided_state <= dest_check & override_en;
    if( dest_check & ~busy ) begin
        gpo_out_buffer[127:0] <= gpo_in[127:0];
    end
    
    if( override_en & ~busy ) begin
        override_value_reg[63:0] <= override_value[63:0];
    end
    
    if( ( busy & selected_wire ) | ( dest_check & override_en ) ) begin
        if( dest_check ) begin
            error_data_buffer[127:0] <= gpo_in[127:0];
        end
        else begin
            error_data_buffer[127:0] <= {72'h0,override_value[63:0]};
        end
    end
end

endmodule