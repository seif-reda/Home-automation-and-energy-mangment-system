int sensorsensitivity=66 
float kwhprice=0.564 
int refV=5 
int supplyV=240 
int powerfactor=85 
int offset=2500
A0 produces value from 0 to 1024
int adcvalue = analogRead(A0);
int voltagedraw = (adcvalue / 1024.0) * 1000;
int currentdraw = ((supplyV – offset) / voltagedraw);

int Vp = voltagedraw /2
int Vrms = Vp x 0.707 (root 2)
int Irms = Vrms x Sensitivity
int watt= Vrms x Irms x powerfactor
int Wh = watt * (time / 3600000.0)
int kWh = Wh / 1000
int Cost = 0.564* kWh.
