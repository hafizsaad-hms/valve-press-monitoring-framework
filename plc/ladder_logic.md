# PLC Interlock & Cycle Execution Logic

### Rung 1: Scaling Analog Sensor Signals
* Read `RAW_LOAD_CELL_INPUT` (Word, 0–27648) $\rightarrow$ Normalize and scale to `SCALED_FORCE_VAL` (0.0 to 12.0 kN).
* Read `RAW_DISPLACEMENT_INPUT` (Word, 0–27648) $\rightarrow$ Normalize and scale to `SCALED_POSITION_VAL` (0.0 to 30.0 mm).

### Rung 2: Dynamic Envelope Evaluation
* If `SCALED_POSITION_VAL` $\ge 22.0\text{ mm}$ AND `SCALED_FORCE_VAL` $< \text{FORCE\_LOWER\_LIMIT}$:
  * Latch `ALARM_INCOMPLETE_STROKE`.
  * Inhibit cylinder auto-cycle.
* If `SCALED_FORCE_VAL` $> \text{FORCE\_UPPER\_LIMIT}$:
  * Latch `ALARM_FORCE_EXCEEDED`.
  * De-energize hydraulic directional control valve immediately.

### Rung 3: Good Cycle Verification & Head Counting
* If stroke reaches target limit ($22.5\text{ mm} \pm 0.3\text{ mm}$) AND neither alarm flag is asserted:
  * Pulse `PASS_CYCLE_STROKE` (One-shot rising trigger).
  * Increment `ENGINE_HEAD_COUNT_TOTAL` by 1.
  * Trigger CSV log record sequence to central station via Industrial Ethernet.
