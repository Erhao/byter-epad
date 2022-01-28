# -*- coding: utf-8 -*-
import os


BID = os.getenv('BYTER_BID', 'fake_bid')
MAC = os.getenv('BYTER_MAC', 'fake_mac')

RAW_PREFIX = "raw_"
INC_PREFIX = "inc_"

REALTIME = "HH:mm"
DATE = "YYYYMMDD"


TimeModeFmtMap = {
    REALTIME: lambda dt: dt.format(REALTIME),
    DATE: lambda dt: dt.format(DATE),
}
