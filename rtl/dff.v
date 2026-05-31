module dff (
    input  D, CLK, RST,
    output reg Q
);
    always @(posedge CLK or posedge RST) begin
        if (RST) Q <= 1'b0;
        else     Q <= D;
    end
endmodule
