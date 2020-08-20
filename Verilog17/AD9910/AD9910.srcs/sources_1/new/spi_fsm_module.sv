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
    input wire reset,
    input wire [31:0] spi_config_in,
    input wire spi_config_selected,
    input wire [31:0] spi_data_in,
    input wire spi_data_selected,
    input wire sdi,
    output wire busy,
    output wire [31:0] spi_data_out,
    output wire data_write,
    output wire sdo,
    output wire cpha,
    output wire cpol,
    output wire cspol,
    output wire slave_en,
    output wire cs_next,
    //output wire off_spi,
    output wire sck_next,
    output wire[NUM_CS-1:0] cs_val
    );
    
reg config_lsb_first;
reg config_slave_en;
//reg config_off_spi;
reg config_end_spi;
reg[4:0] config_dummy;
reg[7:0] config_cs;
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
reg write_en;
reg initialize_reg;
reg [31:0] data_buffer;

wire spi_counter_end;
wire reduced_config_cpha;

parameter IDLE = 3'h0;
parameter LOW = 3'h1;
parameter HIGH = 3'h2;
parameter WAIT_LOW = 3'h3;
parameter LAST_HIGH = 3'h4;
parameter LAST_LOW = 3'h5;
parameter EXTEND_LOW = 4'h6;

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
//assign off_spi = config_off_spi;
assign sck_next = sck_next_state;
assign cs_val[NUM_CS-1:0] = config_cs[NUM_CS-1:0];
assign reduced_config_cpha = config_cpha ^ config_slave_en;
assign data_write = write_en;

clock_divider clock_divider_0 (
    .CLK100MHZ(CLK100MHZ),
    .reset(reset),
    .divide(clk_div),
    .count_enable(spi_counter_state),
    .count_end(spi_counter_end)
);

shift_register_out shift_register_out_0(
    .CLK100MHZ(CLK100MHZ),
    .reset(reset),
    .lsb_first(config_lsb_first),
    .data_load(data_load),
    .data_in(data_buffer),
    .write(initialize_reg),
    .sdo(sdo)
);

shift_register_in shift_register_in_0(
    .CLK100MHZ(CLK100MHZ),
    .reset(reset),
    .lsb_first(config_lsb_first),
    .data_load(data_load),
    .sdi(sdi),
    .clear_register(initialize_reg),
    .data_out(spi_data_out)
);

always @(posedge CLK100MHZ) begin
    if(reset) begin
        spi_start <= 1'b0;
        data_buffer[31:0] <= 32'h0;
        {config_lsb_first, config_slave_en, config_end_spi, config_dummy, config_cs, config_length, config_cspol, config_cpol, config_cpha, clk_div} <= 32'h0;
    end
    else begin
        if( spi_config_selected & ~busy_state) begin
            {config_lsb_first, config_slave_en, config_end_spi, config_dummy, config_cs, config_length, config_cspol, config_cpol, config_cpha, clk_div} <= spi_config_in;
        end
        spi_start <= spi_data_selected & ~busy_state;
        data_buffer[31:0] <= spi_data_in[31:0];
    end
end

//FSM of SPI
always @(posedge CLK100MHZ) begin
    if(reset) begin
        busy_state <= 1'b0;
        spi_fsm_state[2:0] <= IDLE;
        data_remain[4:0] <= 5'h0;
        data_load <= 1'b0;
        sck_next_state <= 1'b0;
        cs_next_state <= 1'b0;
        spi_counter_state <= 1'b0;
        write_en <= 1'b0;
        initialize_reg <= 1'b0;
    end
    else begin
        case(spi_fsm_state)
            IDLE:
            begin
                data_remain[4:0] <= config_length[4:0];
                if(spi_start == 1'b1) begin
                    busy_state <= 1'b1;
                    cs_next_state <= 1'b1;
                    
                    if(reduced_config_cpha == 1'b0) begin
                        data_load <= 1'b1;
                        spi_fsm_state <= LOW;
                    end
                    
                    else begin
                        data_load <= 1'b0;
                        spi_fsm_state <= EXTEND_LOW;
                    end
                    
                    spi_counter_state <= 1'b1;
                    sck_next_state <= 1'b0;
                    write_en <= 1'b0;
                    initialize_reg <= 1'b0;
                end
                else begin
                    cs_next_state <= 1'b0;
                    sck_next_state <= 1'b0;
                    busy_state <= spi_data_selected;
                    data_load <= 1'b0;
                    spi_counter_state <= 1'b0;
                    initialize_reg <= 1'b1;
                    write_en <= 1'b0;
                end
            end
            
            LOW:
            begin
                initialize_reg <= 1'b0;
                if(spi_counter_end == 1'b1) begin
                    if(data_remain[4:0] == 5'h0) begin
                        spi_fsm_state <= LAST_HIGH;
                        //sck_next_state <= ~config_cpha;
                        sck_next_state <= 1'b1;
                        if( reduced_config_cpha == 1'b1 ) begin
                            data_load <= 1'b1;
                        end
                        
                        else begin
                            data_load <= 1'b0;
                        end
                    end
                    
                    else begin
                        spi_fsm_state <= HIGH;
                        //sck_next_state <= ~config_cpha;
                        sck_next_state <= 1'b1;
                        if( reduced_config_cpha == 1'b1 ) begin
                            data_load <= 1'b1;
                        end
                        
                        else begin
                            data_load <= 1'b0;
                        end
                    end
                end
                
                else begin
                    //sck_next_state <= config_cpha;
                    sck_next_state <= 1'b0;
                    data_load <= 1'b0;
                end
            end
            
            HIGH:
            begin
                if( spi_counter_end == 1'b1 ) begin
                    data_remain[4:0] <= data_remain[4:0] - 5'h1;
                    spi_fsm_state <= LOW;
                    if( reduced_config_cpha == 1'b1 ) begin
                        data_load <= 1'b0;
                    end
                    else begin
                        data_load <= 1'b1;
                    end
                    sck_next_state <= 1'b0;
                end
                
                else begin
                    sck_next_state <= 1'b1;
                    data_load <= 1'b0;
                end
            end
            
            WAIT_LOW:
            begin
                data_remain[4:0] <= config_length[4:0];
                if(spi_start == 1'b1) begin
                    busy_state <= 1'b1;
                    if(reduced_config_cpha == 1'b0) begin
                        spi_fsm_state <= LOW;
                        data_load <= 1'b1;
                    end
                    
                    else begin
                        spi_fsm_state <= EXTEND_LOW;
                        data_load <= 1'b0;
                    end
                    write_en <= 1'b0;
                    spi_counter_state <= 1'b1;
                    initialize_reg <= 1'b0;
                    sck_next_state <= 1'b0;
                end
                
                else begin
                    initialize_reg <= 1'b1;
                    spi_counter_state <= 1'b0;
                    busy_state <= 1'b0;
                    data_load <= 1'b0;
                    write_en <= 1'b0;
                    sck_next_state <= 1'b0;
                end
            end
            
            LAST_HIGH:
            begin
                if(spi_counter_end == 1'b1) begin
                    spi_fsm_state <= LAST_LOW;
                    if( reduced_config_cpha == 1'b1 ) begin
                        data_load <= 1'b0;
                    end
                    else if( config_slave_en == 1'b0) begin
                        data_load <= 1'b1;
                    end
                    sck_next_state <= 1'b0;
                end
                else begin
                    sck_next_state <= 1'b1;
                    data_load <= 1'b0;
                end
            end
            LAST_LOW:
            begin
                if(spi_counter_end == 1'b1) begin
                    if(config_end_spi == 1'b1) begin
                        sck_next_state <= 1'b0;
                        spi_fsm_state <= IDLE;
                        data_load <= 1'b0;
                        busy_state <= 1'b1;
                        write_en <= config_slave_en;
                        cs_next_state <= 1'b0;
                    end
                    else begin
                        spi_fsm_state <= WAIT_LOW;
                        sck_next_state <= 1'b0;
                        data_load <= 1'b0;
                        busy_state <= 1'b1;
                        write_en <= config_slave_en;
                    end
                end
                else begin
                    sck_next_state <= 1'b0;
                    data_load <= 1'b0;
                end
            end
            
            EXTEND_LOW:
            begin
                initialize_reg <= 1'b0;
                if(spi_counter_end == 1'b1) begin
                    begin
                        spi_fsm_state <= LOW;
                        sck_next_state <= 1'b0;
                        data_load <= 1'b0;
                    end
                end
                
                else begin
                    sck_next_state <= 1'b0;
                    data_load <= 1'b0;
                end
            end
        endcase
    end
end

endmodule
