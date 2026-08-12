class VocabAgent:
    def apply_sm2(self, q: int, repetitions: int, interval: float, ef: float):
        if q >= 3:
            if repetitions == 0:
                interval = 1
            elif repetitions == 1:
                interval = 6
            else:
                interval = interval * ef
            repetitions += 1
            status = 'learned' if q > 3 else 'shaky'
        else:
            repetitions = 0
            interval = 1
            status = 'forgotten'
            
        ef = max(1.3, ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
        return repetitions, interval, ef, status
