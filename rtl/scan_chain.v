// 4-FF scan chain.
// In capture mode (SE=0): each FF captures its own D[i].
// In shift mode  (SE=1): data shifts ff0→ff1→ff2→ff3; SI enters ff0, SO exits ff3.

module scan_chain (
    input  [3:0] D,
    input        SI, SE, CLK, RST,
    output [3:0] Q,
    output       SO
);
    scan_dff ff0 (.D(D[0]), .SI(SI),   .SE(SE), .CLK(CLK), .RST(RST), .Q(Q[0]));
    scan_dff ff1 (.D(D[1]), .SI(Q[0]), .SE(SE), .CLK(CLK), .RST(RST), .Q(Q[1]));
    scan_dff ff2 (.D(D[2]), .SI(Q[1]), .SE(SE), .CLK(CLK), .RST(RST), .Q(Q[2]));
    scan_dff ff3 (.D(D[3]), .SI(Q[2]), .SE(SE), .CLK(CLK), .RST(RST), .Q(Q[3]));
    assign SO = Q[3];
endmodule
