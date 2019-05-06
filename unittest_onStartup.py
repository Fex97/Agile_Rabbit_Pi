import unittest
from mock import Mock #pip install mock. 
from mock import patch
import onstartupV2
import time

class TestStartupTests(unittest.TestCase):
        def test_uartConnection(self):
                ser = Mock()
                ser.readline = Mock(return_value="OK")
                self.assertTrue(onstartupV2.check_uartConnection(ser))
        def test_setCGNSPower(self):
                ser = Mock()
                ser.readline = Mock(return_value="OK")
                self.assertTrue(onstartupV2.set_CGNSPower(ser))
        def test_CGNSPOWER_is_1(self):
                ser = Mock()
                ser.readline = Mock(return_value="+CGNSPWR:1")
                self.assertTrue(onstartupV2.check_CGNSPower(ser))
        def test_CGNSPOWER_is_0(self):
                ser = Mock()
                ser.readline = Mock(return_value="+CGNSPWR:0")
                self.assertFalse(onstartupV2.check_CGNSPower(ser))
        def test_RSSI_is_ok(self):
                ser = Mock()
                ser.readline = Mock(return_value="+CSQ: 10,10")
                self.assertTrue(onstartupV2.check_RSSI(ser))
        def test_RSSI_is_low(self):
                ser = Mock()
                ser.readline = Mock(return_value="+CSQ:3,10")
                self.assertFalse(onstartupV2.check_RSSI(ser))
        def test_batterypercent_and_voltageLevel_is_ok(self):
                ser = Mock()
                ser.readline = Mock(return_value="+CBC: 0,100,3400")
                self.assertTrue(onstartupV2.check_batteryLevel(ser))
        def test_batterypercent_and_voltageLevel_is_notok(self):
                ser = Mock()
                ser.readline = Mock(return_value="+CBC: 0,9,2200")
                self.assertFalse(onstartupV2.check_batteryLevel(ser))
        def test_batterypercent_is_notok(self):
                ser = Mock()
                ser.readline = Mock(return_value="+CBC: 0,9,3400")
                self.assertFalse(onstartupV2.check_batteryLevel(ser))
        def test_voltageLevel_is_notok(self):
                ser = Mock()
                ser.readline = Mock(return_value="+CBC: 0,90,4400")
                self.assertFalse(onstartupV2.check_batteryLevel(ser))

        def test_fix_is_1(self):
                ser = Mock()
                ser.readline = Mock(return_value="+CGNSINF: <GNSS run status>,1,<UTC date & Time>,<Latitude>,<Longitude>,<MSL Altitude>,<Speed Over Ground>,<Course Over Ground>,<Fix Mode>,<Reserved1>,<HDOP>,<PDOP>,<VDOP>,<Reserved2>,<GNSS Satellites in View>,<GNSS Satellites Used>,<GLONASS SatellitesUsed>,<Reserved3>,<C/N0 max>,<HPA>,<VPA>  ")
                self.assertTrue(onstartupV2.check_gpsFix(ser))
        def test_gps_fetch(self):
                ser = Mock()
                ser.readline = Mock(return_value="+CGNSINF: <GNSS run status>,1,<UTC date & Time>,9999,1111,<MSL Altitude>,<Speed Over Ground>,<Course Over Ground>,<Fix Mode>,<Reserved1>,<HDOP>,<PDOP>,<VDOP>,<Reserved2>,<GNSS Satellites in View>,<GNSS Satellites Used>,<GLONASS SatellitesUsed>,<Reserved3>,<C/N0 max>,<HPA>,<VPA>  ")
                self.assertEqual = Mock(return_value=99991111)
if __name__ == '__main__':
        unittest.main()
