.subckt DESIGN.IO2 3 

*** Printing nodes ****

.node_param 3 name=DESIGN.IO2.1  vlo_max=0.8 vhi_min=2 print  cycles=(1 ) 
*** End of node printing ***

*** Pin Iocells Section ***
* This component has no signal model
v_short_DESIGN.IO2.1 2 3 0.0

bdrvr 18 3 19 23 22 20 21 Model=SPARTAN7_LVCMOS33_S_12_HR_Typ_27degC File=ibis_models.inc
* stimulus for pin DESIGN.IO2.1
x_stimulus 22 23 19 DESIGN.IO2.1_stim

*** No signal model: Guessing Dc Voltages from iocell ***

*** Guessing Dc power_bus Voltage ***
v_power_bus_DESIGN.IO2.1_18 18 0 3.3

*** Guessing Dc ground_bus Voltage ***
v_ground_bus_DESIGN.IO2.1_19 19 0 0

*** Guessing Dc power_clamp_bus Voltage ***
v_power_clamp_bus_DESIGN.IO2.1_20 20 0 3.3

*** Guessing Dc ground_clamp_bus Voltage ***
v_ground_clamp_bus_DESIGN.IO2.1_21 21 0 0
.ends DESIGN.IO2
.subckt DESIGN.IO1 3 

*** Printing nodes ****

.node_param 3 name=DESIGN.IO1.1  vlo_max=0.8 vhi_min=2 print refnode cycles=(3 ) 
*** End of node printing ***

*** Pin Iocells Section ***
* This component has no signal model
v_short_DESIGN.IO1.1 2 3 0.0

bdrvr 18 3 19 23 22 20 21 Model=SPARTAN7_LVCMOS33_S_12_HR_Typ_27degC File=ibis_models.inc
* stimulus for pin DESIGN.IO1.1
x_stimulus 22 23 19 DESIGN.IO1.1_stim

*** No signal model: Guessing Dc Voltages from iocell ***

*** Guessing Dc power_bus Voltage ***
v_power_bus_DESIGN.IO1.1_18 18 0 3.3

*** Guessing Dc ground_bus Voltage ***
v_ground_bus_DESIGN.IO1.1_19 19 0 0

*** Guessing Dc power_clamp_bus Voltage ***
v_power_clamp_bus_DESIGN.IO1.1_20 20 0 3.3

*** Guessing Dc ground_clamp_bus Voltage ***
v_ground_clamp_bus_DESIGN.IO1.1_21 21 0 0
.ends DESIGN.IO1
