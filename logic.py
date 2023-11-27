from obj import Warehouse
from os.path import exists


wh = Warehouse()
wh.import_status() if exists('warehouse_status.txt') else wh.export_status()