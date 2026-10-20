from __future__ import annotations
from .models import AnalysisPolicy,SignalDefinition

def default_catalogue()->list[SignalDefinition]:
    return [SignalDefinition("Powertrain.Motor.Vibration","g",0,20,True),SignalDefinition("Powertrain.Motor.Temperature","degC",-40,200,True),SignalDefinition("Powertrain.Oil.Pressure","bar",0,20,True)]

def policy_from_dict(value:dict)->AnalysisPolicy:return AnalysisPolicy(**{key:value[key] for key in AnalysisPolicy.__dataclass_fields__ if key in value})
