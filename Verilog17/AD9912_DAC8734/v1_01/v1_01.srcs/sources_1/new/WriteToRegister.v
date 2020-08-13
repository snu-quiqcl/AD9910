`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    12:08:42 06/10/2014 
// Design Name: 
// Module Name:    WriteToRegister 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module WriteToRegister(DDS_clock, dataLength, registerData, registerDataReady, wr_rcsbar, /*rsclk,*/ rsdio, 
								countmonitor, registerDataReadymonitor, internalmonitor, busy); // extendedDataReady);
////
//****parameter changeded for AD9910****
////
//parameter MAXLENGTH = 8 ;
parameter MAXLENGTH = 9 ;
parameter MAXLENGTH8 = MAXLENGTH*8 ;
input			DDS_clock;
input [3:0]	dataLength;
input [MAXLENGTH*8-1:0]	registerData;
input registerDataReady;
output reg wr_rcsbar;
//output rsclk;
output rsdio;
output [6:0] countmonitor;
output reg registerDataReadymonitor;

output [7:0] internalmonitor;


// reg	oldregisterDataReady;

reg [MAXLENGTH*8-1:0] data;
reg [6:0] dataCount;
output reg busy ;


   

reg [1:0] writeStage;

parameter IDLE = 2'h0;
parameter READY = 2'h1;
parameter SEND = 2'h2;
parameter FINISH = 2'h3;

initial
begin
	data = {(MAXLENGTH*8){1'b0}};
	writeStage = IDLE;
	// oldregisterDataReady = 1'b0;
	wr_rcsbar = 1'b1;
	registerDataReadymonitor = 1'b0;
	busy = 1'b0;
end

always @(negedge DDS_clock)
begin
	case (writeStage)
	IDLE: // Waiting for registerDataReady
		if (registerDataReady)
			begin
				writeStage <= READY;
				busy <= 1'b1;
			end
		else
			begin
				busy <= 1'b0;
			end
	
	READY:
		begin
			data <= registerData; 
			dataCount <= {dataLength, 3'b000};
			wr_rcsbar <= 1'b0;
			registerDataReadymonitor <= ~registerDataReadymonitor;
			writeStage <= SEND;
		end	
	
	SEND: // Need to send the next bit7. Remaining bits: dataCount
		begin
			if (dataCount == 7'b0000001)
				begin
					writeStage <= FINISH;
					wr_rcsbar <= 1'b1;
				end
			
			dataCount <= dataCount - 7'b0000001;
			data <= {data[(MAXLENGTH8-2):0], 1'b0};
			
		end

	FINISH:  
		begin
			busy <= 1'b0;
			writeStage <= IDLE;
		end
	
	default:
	begin
		wr_rcsbar <= 1'b1;
		writeStage <= IDLE;
		busy <=1'b0;
	end
	endcase
end

assign internalmonitor [7:0]  = {registerDataReadymonitor, writeStage, registerDataReady, dataLength} ;
assign countmonitor = dataCount ;
assign rsdio = data[MAXLENGTH8-1];
//assign rsclk = clk & ~wr_rcsbar;


endmodule
