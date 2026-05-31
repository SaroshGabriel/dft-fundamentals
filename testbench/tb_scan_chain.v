`timescale 1ns/1ps

// Mirrors scan_chain_simulator.py exactly:
//   d_inputs  = [1, 0, 1, 1]  ->  D = 4'b1101  (D[0]=1, D[1]=0, D[2]=1, D[3]=1)
//   shift_in  = "1010"        ->  SI sequence: 1,0,1,0  LSB-first
//   shifted_out expected "1011"

module tb_scan_chain;

    reg  [3:0] D;
    reg        SI, SE, CLK, RST;
    wire [3:0] Q;
    wire       SO;

    scan_chain dut (
        .D(D), .SI(SI), .SE(SE), .CLK(CLK), .RST(RST),
        .Q(Q), .SO(SO)
    );

    // 10 ns clock period
    initial CLK = 0;
    always #5 CLK = ~CLK;

    // Collect shifted-out bits
    reg [3:0] shifted_out;
    reg [3:0] pattern;
    integer i;

    task posedge_clk;
        begin
            @(posedge CLK);
            #1; // settle after edge
        end
    endtask

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, tb_scan_chain);

        // ── Reset ─────────────────────────────────────────────────────────
        RST = 1; SE = 0; SI = 0; D = 4'b0000;
        posedge_clk;
        RST = 0;
        $display("After reset:  Q = %b%b%b%b", Q[0],Q[1],Q[2],Q[3]);

        // ── Step 1: Shift in "1010" (LSB first: SI = 1,0,1,0) ─────────────
        // Python: chain.shift_in("1010") feeds pattern[0]=1, pattern[1]=0, ...
        SE = 1;
        D  = 4'b1101;   // present functional data (ignored while SE=1)
        pattern = 4'b0101;  // bit 0=1, bit 1=0, bit 2=1, bit 3=0
        for (i = 0; i < 4; i = i+1) begin
            SI = pattern[i];
            posedge_clk;
            $display("Shift in SI=%b -> Q=%b%b%b%b", SI, Q[0],Q[1],Q[2],Q[3]);
        end

        // ── Step 2: Capture (SE=0, one clock) ────────────────────────────
        SE = 0;
        posedge_clk;
        $display("After capture: Q=%b%b%b%b  (expect 1011)", Q[0],Q[1],Q[2],Q[3]);

        // ── Step 3: Shift out — read SO BEFORE the clock edge ────────────
        SE = 1; SI = 0;
        for (i = 0; i < 4; i = i+1) begin
            @(negedge CLK); #1;         // sample SO at negedge (stable value)
            shifted_out[i] = SO;
            $display("Shift out[%0d]: SO=%b  Q=%b%b%b%b", i, SO, Q[0],Q[1],Q[2],Q[3]);
            posedge_clk;
        end

        $display("");
        $display("Shifted out (LSB first): %b%b%b%b",
                 shifted_out[0], shifted_out[1], shifted_out[2], shifted_out[3]);

        // ── PASS / FAIL ───────────────────────────────────────────────────
        if (shifted_out === 4'b1011)
            $display("PASS: shifted_out matches Python output 1011");
        else
            $display("FAIL: expected 4'b1011, got %b%b%b%b",
                     shifted_out[0],shifted_out[1],shifted_out[2],shifted_out[3]);

        #20;
        $finish;
    end

endmodule
