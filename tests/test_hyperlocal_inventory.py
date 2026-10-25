import math
import tempfile
import unittest
from pathlib import Path
from src.hyperlocal_inventory import connect, ingest, nearby, seed, meters_between

class HyperlocalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.db=connect(str(Path(self.tmp.name)/'test.sqlite'))
    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()
    def test_demo_boundary(self):
        seed(self.db,0.0,0.0)
        records=nearby(self.db,0.0,0.0)
        self.assertEqual(len(records),3)
        self.assertNotIn('demo-outside',{r['key'] for r in records})
        self.assertTrue(all(r['distance_feet']<=50 for r in records))
    def test_updated_location_replaces_index(self):
        sample=dict(key='a',name='Lab device',kind='camera',lat=0.0,lon=0.0,source='enrolled-lab')
        ingest(self.db,sample)
        self.assertEqual(len(nearby(self.db,0.0,0.0)),1)
        sample['lat']=0.002
        ingest(self.db,sample)
        self.assertEqual(len(nearby(self.db,0.0,0.0)),0)
        self.assertEqual(len(nearby(self.db,0.002,0.0)),1)
    def test_invalid_inputs(self):
        item=dict(key='a',name='test',kind='camera',lat=91,lon=0,source='demo')
        with self.assertRaises(ValueError):ingest(self.db,item)
        item['lat']=float('nan')
        with self.assertRaises(ValueError):ingest(self.db,item)
        item['lat']=0
        item['name']=''
        with self.assertRaises(ValueError):ingest(self.db,item)
    def test_distance(self):
        self.assertEqual(meters_between(0,0,0,0),0)
        self.assertAlmostEqual(meters_between(0,0,0.001,0),111.195,delta=.2)
if __name__=='__main__':
    unittest.main()
