#!/bin/bash
# fix_and_start_openclaw.sh
# Fixt openclaw config en start gateway

python3 -c "
import json
with open('/home/prime/.openclaw/openclaw.json') as f: d=json.load(f)
d['agents']['defaults']['compaction'] = {'mode': 'safeguard'}
with open('/home/prime/.openclaw/openclaw.json','w') as f: json.dump(d,f,indent=2)
print('Config OK')
"
systemctl --user start openclaw-gateway
echo "Gateway gestart"
