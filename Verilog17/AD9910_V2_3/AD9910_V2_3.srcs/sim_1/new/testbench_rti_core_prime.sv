`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/08/20 14:10:03
// Design Name: 
// Module Name: testbench_rti_core_prime
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


module testbench_rti_core_prime;

logic clk;
logic reset;
logic flush;
logic write;
logic read;
logic [127:0] rti_in;
wire [127:0] rti_out;
wire [127:0] overflow_error_data;
wire overflow_error;
wire underflow_error;
wire full;
wire empty;

rti_core_prime rti_core_prime_0(
    .clk(clk),
    .reset(reset),
    .flush(flush),
    .write(write),
    .read(read),
    .rti_in(rti_in),
    .rti_out(rti_out),
    .overflow_error_data(overflow_error_data),
    .overflow_error(overflow_error),
    .underflow_error(underflow_error),
    .full(full),
    .empty(empty)
    );
    
always begin
    #5
    clk = ~clk;
end

integer i;
initial begin
    clk = 1'b0;
    reset = 1'b0;
    flush = 1'b0;
    write = 1'b0;
    read = 1'b0;
    rti_in[127:0] = 128'h0;
    
    #10
    reset = 1'b1;
    
    #10
    reset = 1'b0;
    
    #100
    rti_in = 128'h1234;
    write = 1'b1;
    
    #10
    write = 1'b0;
    
    #10
    rti_in = 128'h5678;
    write = 1'b1;
    
    #10
    write = 1'b0;
    
    #10
    rti_in = 128'h2468;
    write = 1'b1;
    
    #10
    write = 1'b0;
    
    #10
    read = 1'b1;
    
    #60
    read = 1'b0;
    
    for( i = 0; i < 512; i ++ ) begin
        #10
        rti_in = i+1;
        write = 1'b1;
        
        #10
        write = 1'b0;
    end
    
    #50
    rti_in = 128'h1234;
    write = 1'b1;
    
    #10
    write = 1'b0;
    
    #50
    rti_in = 128'h5678;
    write = 1'b1;
    
    #10
    write = 1'b0;
    
    #10
    rti_in = 128'h2468;
    write = 1'b1;
    
    #10
    write = 1'b0;
    
    #10
    flush = 1'b1;
    
    #10
    flush = 1'b0;
end

endmodule
