from __future__ import annotations
import random
from .models import TelemetryDataset,TelemetryRecord

def generate_fleet(vehicle_count:int=100,samples_per_vehicle:int=40,seed:int=42)->TelemetryDataset:
    if not 2<=vehicle_count<=10000 or not 5<=samples_per_vehicle<=10000:raise ValueError("synthetic dimensions out of range")
    randomizer=random.Random(seed);records=[]
    for vehicle_index in range(vehicle_count):
        version="2.1.0" if vehicle_index>=vehicle_count*0.7 else "2.0.0";variant=["base","long-range","performance"][vehicle_index%3];degrading=version=="2.1.0" and variant=="performance"
        for sample_index in range(samples_per_vehicle):
            vibration=1.0+randomizer.gauss(0,.05)+(sample_index*0.035 if degrading else 0);temperature=70+randomizer.gauss(0,1)+(sample_index*.25 if degrading else 0);pressure=2.5+randomizer.gauss(0,.03);records.append(TelemetryRecord(f"veh-{vehicle_index:04d}",sample_index*1000,version,variant,{"Powertrain.Motor.Vibration":vibration,"Powertrain.Motor.Temperature":temperature,"Powertrain.Oil.Pressure":pressure},f"trip-{vehicle_index}","high-mileage" if vehicle_index%2 else "standard"))
    return TelemetryDataset("synthetic-fleet","1.0",tuple(records))
