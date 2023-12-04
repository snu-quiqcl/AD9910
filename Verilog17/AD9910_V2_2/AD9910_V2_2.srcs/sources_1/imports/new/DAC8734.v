`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2018/02/13 08:07:29
// Design Name: 
// Module Name: DAC8734
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


module DAC8734(
	input clock,
	input start_trigger, // This trigger will start DAC FSM
	input [23:0] data,
	output sclk,
	output reg cs_bar,
	output reg sdi,
	output reg busy
   );

	reg [2:0] state;
	parameter [2:0] 	STANDBY = 0,
						WRITE_DAC = 3,
						END_OF_CYCLE = 4;
						
	reg [5:0] count;
	reg [23:0] data_to_DAC;
						
	initial begin
		busy <= 1'b0;
		cs_bar <= 1'b1;
		state <= STANDBY;
		count <= 'd0;
		data_to_DAC <= 'd0;
	end

    assign sclk = cs_bar | clock;
    
	always @(posedge clock) begin
		case (state)
			STANDBY:
				if (start_trigger == 1'b1) begin
					state <= WRITE_DAC;
				    data_to_DAC <= data;
					busy <= 1'b1;
					count <= 'd1;
				end
				else begin
					busy <= 1'b0;
				end
			WRITE_DAC: begin // Writing to DAC
    				cs_bar <= 0;
    				sdi <= data_to_DAC[23];
			     	data_to_DAC[23:0] <= {data_to_DAC[22:0], 1'b0};
    				if (count == 'd24) state <= END_OF_CYCLE;
	       		    else state <= WRITE_DAC;
			        count <= count + 1;
			    end
			END_OF_CYCLE: begin
				    cs_bar <= 1;
				    state <= STANDBY;
				end
			default:
				state <= STANDBY;
		endcase
	end
endmodule
