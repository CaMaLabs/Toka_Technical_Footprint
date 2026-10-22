import unittest
from src.onvif_collect import target_ip,parse_device_info
XML=b'<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:d="http://www.onvif.org/ver10/device/wsdl"><s:Body><d:GetDeviceInformationResponse><d:Manufacturer>DemoCo</d:Manufacturer><d:Model>A</d:Model><d:FirmwareVersion>2</d:FirmwareVersion><d:HardwareId>board</d:HardwareId><d:SerialNumber>hidden</d:SerialNumber></d:GetDeviceInformationResponse></s:Body></s:Envelope>'
class TestOnvif(unittest.TestCase):
 def test_private(self):self.assertEqual(target_ip("192.168.1.4"),"192.168.1.4")
 def test_public_rejected(self):
  with self.assertRaises(ValueError):target_ip("8.8.8.8")
 def test_loopback_rejected(self):
  with self.assertRaises(ValueError):target_ip("127.0.0.1")
 def test_parse(self):
  result=parse_device_info(XML);self.assertEqual(result["firmware"],"2");self.assertNotIn("serialnumber",result)
 def test_invalid(self):
  with self.assertRaises(ValueError):parse_device_info(b"<x/>")
