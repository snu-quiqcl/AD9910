`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/17 17:27:19
// Design Name: 
// Module Name: spi_fsm_module
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


module spi_fsm_module
#(
    parameter NUM_CS = 1
)
(
    input wire CLK100MHZ,
    input wire [31:0] spi_config_in,
    input wire spi_config_selected,
    input wire [31:0] spi_data_in,
    input wire spi_data_selected,
    output wire busy,
    output wire [31:0] spi_data_out,
    output wire data_write,
    output wire sdi,
    output wire sdo,
    output wire cpha,
    output wire cpol,
    output wire cspol,
    output wire slave_en,
    output wire cs_next,
    output wire off_spi,
    output wire sck_next,
    output wire[NUM_CS-1:0] cs
    );
    
reg config_lsb_first;
reg config_slave_en;
reg config_off_spi;
reg config_end_spi;
reg[11:0] config_cs;
reg[4:0] config_length;
reg config_cspol;
reg config_cpol;
reg config_cpha;
reg[7:0] clk_div;

reg busy_state;
reg[2:0] spi_fsm_state;
reg spi_start;
reg [4:0] data_remain;
reg data_load;
reg sck_next_state;
reg cs_next_state;
reg spi_counter_state;
reg clear_register;
reg write_en;
reg [31:0] data_buffer;

wire spi_counter_end;

parameter IDLE = 3'h0;
parameter LOW = 3'h1;
parameter HIGH = 3'h2;
parameter WAIT_LOW = 3'h3;

initial begin
    busy_state <= 1'b0;
    spi_fsm_state <= IDLE;
end

assign busy = busy_state;
assign cpha = config_cpha;
assign cpol = config_cpol;
assign cspol = config_cspol;
assign slave_en = config_slave_en;
assign cs_next = cs_next_state;
assign off_spi = config_off_spi;
assign sck_next = sck_next_state;
assign cs[NUM_CS-1:0] = config_cs[NUM_CS-1:0];

clock_divider clock_divider_0 (
    .CLK100MHZ(CLK100MHZ),
    .divide(clk_div),
    .count_enable(spi_counter_state),
    .count_end(spi_counter_end)
);

shift_register_out shift_register_out_0(
    .CLK100MHZ(CLK100MHZ),
    .lsb_first(config_lsb_first),
    .data_load(data_load),
    .data_in(data_buffer),
    .write(spi_start),
    .sdo(sdo)
);

shift_register_in shift_register_in_0(
    .CLK100MHZ(CLK100MHZ),
    .lsb_first(config_lsb_first),
    .data_load(data_load),
    .sdi(sdi),
    .clear_register(clear_register),
    .data_out(spi_data_out)
);

always @(posedge CLK100MHZ) begin
    if( spi_config_selected & ~busy_state) begin
        {config_lsb_first, config_slave_en, config_off_spi, config_end_spi, config_cs, config_length, config_cspol, config_cpol, config_cpha, clk_div} <= spi_config_in;
    end
    spi_start <= spi_data_selected & ~busy_state;
    data_buffer[31:0] <= spi_data_in[31:0];
end

//FSM of SPI
always @(posedge CLK100MHZ) begin
    case(spi_fsm_state)
        IDLE:
        begin
            data_remain <= config_length;
            if(spi_start == 1'b1) begin
                busy_state <= 1'b1;
                cs_next_state <= 1'b1;
                spi_fsm_state <= LOW;
                spi_counter_state <= 1'b1;
                sck_next_state <= config_cpha;
                clear_register <= 1'b0;
                write_en <= 1'b0;
                if(config_cpha == 1'b0) begin
                    data_load <= 1'b1;
                end
                else begin
                    data_load <= 1'b0;
                end
            end
            else begin
                cs_next_state <= 1'b1;
                sck_next_state <= config_cpha;
                busy_state <= 1'b0;
                data_load <= 1'b0;
                spi_counter_state <= 1'b0;
                clear_register <= 1'b1;
                write_en <= 1'b0;
            end
        end
        
        LOW:
        begin
            if(spi_counter_end == 1'b1) begin
                if(data_remain[4:0] == 5'd0) begin
                    if(config_end_spi == 1'b1) begin
                        sck_next_state <= config_cpha;
                        spi_fsm_state <= IDLE;
                        data_load <= 1'b0;
                        busy_state <= 1'b0;
                        write_en <= config_slave_en;
                    end
                    else begin
                        spi_fsm_state <= WAIT_LOW;
                        sck_next_state <= config_cpha;
                        data_load <= 1'b0;
                        busy_state <= 1'b0;
                        write_en <= config_slave_en;
                    end
                end
                
                else begin
                    spi_fsm_state <= HIGH;
                    sck_next_state <= ~cpha;
                    if( cpha == 1'b1 ) begin
                        data_load <= 1'b1;
                    end
                    else begin
                        data_load <= 1'b0;
                    end
                end
            end
            
            else begin
                sck_next_state <= cpha;
                data_load <= 1'b0;
            end
        end
        
        HIGH:
        begin
            if( spi_counter_end == 1'b1 ) begin
                data_remain[4:0] <= data_remain[4:0] - 5'd1;
                spi_fsm_state <= LOW;
                if( config_cpha == 1'b1 ) begin
                    data_load <= 1'b0;
                end
                else begin
                    data_load <= 1'b1;
                end
                sck_next_state <= config_cpha;
            end
            
            else begin
                sck_next_state <= ~config_cpha;
                data_load <= 1'b0;
            end
        end
        
        WAIT_LOW:
        begin
            if(spi_start == 1'b1) begin
                busy_state <= 1'b1;
                spi_fsm_state = LOW;
                write_en <= 1'b0;
                spi_counter_state <= 1'b1;
                if( config_cpha == 1'b0 ) begin
                    data_load <= 1'b1;
                end
                else begin
                    data_load <= 1'b0;
                end
            end
            
            else begin
                spi_counter_state <= 1'b0;
                busy_state <= 1'b0;
                data_load <= 1'b0;
                write_en <= 1'b0;
            end
        end
    endcase
end

endmodule
