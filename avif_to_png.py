#!/usr/bin/env python3
"""

Convert all .avif → .png in the current directory,
then delete the original .avif files.
Requires pillow-avif-plugin + system libavif.
"""

import pillow_avif        # 🛠 Register the AVIF plugin with PIL
from PIL import Image
import os

def main():
    for fn in os.listdir('.'):
        if fn.lower().endswith('.avif'):
            png = fn[:-5] + '.png'
            try:
                with Image.open(fn) as img:
                    img.save(png, 'PNG')
                os.remove(fn)
                print(f"✓ Converted & removed: {fn} → {png}")
            except Exception as e:
                print(f"⚠ Failed on {fn}: {e}")

if __name__ == '__main__':
    main()
