class Pacemaker:
    def __init__(self,
                _pacingMode="",
                _upperRate=0,
                _lowerRate=0,
                _amplitude=0,
                _pulseWidth=0,
                _sensitivity=0,
                _RP=0,
                _hysteresis=0,
                _smoothing=0,
                _PVARP=0,
                _maximumSensorRate=0,
                _activityThreshold=0,
                _reactionTime=0,
                _responseFactor=0,
                _recoveryTime=0
                        ):

        #note: Similar modes are combined where it makes sense. Ie; Atr. Sensitivity and Vent. Sensitivity...
        self.pacingMode=_pacingMode
        self.upperRate=_upperRate
        self.lowerRate=_lowerRate
        self.amplitude=_amplitude
        self.pulseWidth=_pulseWidth
        self.sensitivity=_sensitivity
        self.RP=_RP
        self.hysteresis=_hysteresis
        self.smoothing=_smoothing
        self.PVARP=_PVARP
        
        #A2 parameters
        self.maximumSensorRate=_maximumSensorRate
        self.activityThreshold=_activityThreshold
        self.reactionTime=_reactionTime
        self.responseFactor=_responseFactor
        self.recoveryTime=_recoveryTime





    def connect(self):
        return False #ADD proper funtionality in assignment 2 (connect to simulink)