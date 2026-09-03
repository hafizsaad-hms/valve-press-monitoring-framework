# valve-press-monitoring-framework
PLC and HMI monitoring framework for valve-pressing force evaluation, assembly defect detection, and real-time engine head traceability.
# PLC & HMI-Based Valve-Pressing Monitoring Framework

An industrial automation and process-monitoring framework designed to optimize quality assurance, pressing force evaluation, and real-time traceability during engine head assembly.

---

## 📌 Project Overview
During assembly operations in automotive manufacturing, precise valve seat/guide insertion is critical to combustion sealing and engine reliability. This research project conceptualizes an integrated automation and supervisory framework for the **Engine Assembly Plant (EAP)** at **Millat Tractors Limited**.

The system addresses variations in manual/semi-automated press fitting by deploying real-time sensor feedback, programmable logic controllers (PLC), and Human-Machine Interface (HMI) dashboards.

---

## 🎯 Key Objectives & Research Scope
* **Pressing Force Evaluation:** Continuous monitoring of press force profiles to prevent valve seat distortion, under-pressing, or structural micro-fractures.
* **Traceability & Production Tracking:** Automated logging of engine head count, pass/fail metrics, and cycle-time bottlenecks.
* **Supervisory Control:** Conceptual design of PLC ladder architecture and an HMI interface for plant engineers to view real-time diagnostics and fault trends.

---

## ⚙️ System Architecture & Methodology

flowchart TD
    subgraph Station["Physical Assembly Station (Engine Head)"]
        LC["Load Cell (Force Feedback)"]
        LVDT["LVDT (Displacement Encoder)"]
        Cyl["Hydraulic Press Ram"]
    end

    subgraph DAQ["Signal Conditioning & Control Layer"]
        AI["Analog Input Module (4-20mA / 0-10V)"]
        PLC["Industrial PLC (Core Logic Engine)"]
        LimitCheck{"Force vs. Stroke Envelope Verification"}
    end

    subgraph Interface["HMI & Traceability Layer"]
        HMI["HMI Touch Panel (Live Curve & Status)"]
        Counter["Cycle Counter & Production Audit Log"]
        DB[(Traceability Database / Local CSV)]
    end

    Cyl -->|Press Stroke| LC
    Cyl -->|Position| LVDT
    LC -->|Force Signal| AI
    LVDT -->|Position Signal| AI
    AI --> PLC
    PLC --> LimitCheck

    LimitCheck -->|Within Bounds| Accept["PASS: Increment Head Count & Retract"]
    LimitCheck -->|Out of Envelope| Reject["FAIL: Interlock Stop & Audible Alarm"]

    Accept --> HMI
    Reject --> HMI
    HMI --> Counter
    Counter --> DB
