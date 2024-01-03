import unittest
import autotrading.machine.upbit_machine as upbit_machine
import inspect

class UpbitMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.upbit_machine = upbit_machine.UpbitMachine()

    def tearDown(self):
        pass

    def test_set_token(self):
        print(inspect.stack()[0][3])

    def test_get_token(self):
        print(inspect.stack()[0][3])
        m = upbit_machine.UpbitMachine()
        assert m.get_token()

    def test_get_wallet_status(self):
        print(inspect.stack()[0][3])
        m = upbit_machine.UpbitMachine()
        assert m.get_wallet_status()



