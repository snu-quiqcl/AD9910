*Main Circuit File
* Interconnect subcircuit statements for Board DESIGN
xDESIGN_icn_ckt 1 2 DESIGN_icn_ckt
* Component subcircuit statements
xDESIGN.IO1 1 DESIGN.IO1
xDESIGN.IO2 2 DESIGN.IO2
.include ./interconn.spc
.include ./comps.spc
.include ./stimulus.spc
.end
