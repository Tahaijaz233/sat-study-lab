import unittest
import sys
import os

if __name__ == '__main__':
    # Ensure C:\SAT is in path if needed
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
