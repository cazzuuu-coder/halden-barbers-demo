#!/bin/bash
set -e
OUT=/workspace/webaur-v2/_tools/lh
mkdir -p "$OUT"
export CI=1
export CHROME_PATH=/usr/bin/google-chrome
FLAGS='--headless --no-sandbox --disable-dev-shm-usage --disable-gpu'

run() {
  local url="$1" name="$2" form="$3"
  echo "=== $name $form ===" 
  if [ "$form" = "mobile" ]; then
    npx --yes lighthouse "$url" \
      --chrome-flags="$FLAGS" \
      --only-categories=performance,accessibility,best-practices,seo \
      --form-factor=mobile \
      --screenEmulation.mobile=true \
      --output=json --output-path="$OUT/${name}-mobile.json" \
      --quiet
  else
    npx --yes lighthouse "$url" \
      --chrome-flags="$FLAGS" \
      --only-categories=performance,accessibility,best-practices,seo \
      --preset=desktop \
      --output=json --output-path="$OUT/${name}-desktop.json" \
      --quiet
  fi
}

run http://127.0.0.1:8766/index.html home mobile
run http://127.0.0.1:8766/index.html home desktop
run http://127.0.0.1:8766/work.html work mobile
run http://127.0.0.1:8766/work.html work desktop
run http://127.0.0.1:8766/contact.html contact mobile
run http://127.0.0.1:8766/contact.html contact desktop
run http://127.0.0.1:8766/demos/barber-studio/index.html demo-barber mobile
run http://127.0.0.1:8766/demos/barber-studio/index.html demo-barber desktop

python3 - << 'PY'
import json
from pathlib import Path
out=Path('/workspace/webaur-v2/_tools/lh')
print(f"{'report':<32} {'Perf':>5} {'A11y':>5} {'BP':>5} {'SEO':>5}")
for p in sorted(out.glob('*.json')):
    d=json.loads(p.read_text())
    cats=d.get('categories',{})
    def sc(k):
        v=cats.get(k,{}).get('score')
        return '' if v is None else str(int(round(v*100)))
    print(f"{p.stem:<32} {sc('performance'):>5} {sc('accessibility'):>5} {sc('best-practices'):>5} {sc('seo'):>5}")
PY
