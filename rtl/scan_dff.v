// Scan flip-flop: D-FF with 2:1 mux at input.
// SE=1 → shift mode (captures SI from previous FF in chain)
// SE=0 → capture mode (captures functional data D)
module scan_dff (
    input  D, SI, SE, CLK, RST,
    output reg Q
);
    always @(posedge CLK or posedge RST) begin
        if (RST) Q <= 1'b0;
        else     Q <= SE ? SI : D;
    end
endmodule
