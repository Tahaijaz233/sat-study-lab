import unittest

def sm2(quality, repetitions, previous_interval, previous_ef):
    if quality < 3:
        return 0, 1, previous_ef
    
    if repetitions == 0:
        interval = 1
    elif repetitions == 1:
        interval = 6
    else:
        interval = round(previous_interval * previous_ef)
    
    ef = previous_ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(1.3, ef)
    
    return repetitions + 1, interval, ef

def get_status(interval):
    if interval == 1:
        return 'forgotten'
    elif interval < 7:
        return 'shaky'
    else:
        return 'learned'

class TestSM2(unittest.TestCase):
    def test_quality_less_than_3(self):
        rep, interval, ef = sm2(2, 5, 20, 2.5)
        self.assertEqual(rep, 0)
        self.assertEqual(interval, 1)
        self.assertEqual(ef, 2.5)
        self.assertEqual(get_status(interval), 'forgotten')

    def test_quality_greater_equal_3(self):
        rep, interval, ef = sm2(3, 1, 1, 2.5)
        self.assertEqual(rep, 2)
        self.assertEqual(interval, 6)
        self.assertTrue(ef < 2.5)
        self.assertEqual(get_status(interval), 'shaky')
        
        rep_q4, interval_q4, ef_q4 = sm2(4, 1, 1, 2.5)
        self.assertEqual(ef_q4, 2.5)
        
        rep2, interval2, ef2 = sm2(5, 2, 6, 2.5)
        self.assertEqual(rep2, 3)
        self.assertEqual(interval2, 15)
        self.assertTrue(ef2 > 2.5)
        self.assertEqual(get_status(interval2), 'learned')

    def test_ef_minimum_bound(self):
        rep, interval, ef = sm2(3, 1, 1, 1.3)
        self.assertEqual(ef, 1.3)

if __name__ == '__main__':
    unittest.main()
