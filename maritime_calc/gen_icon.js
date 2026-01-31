const fs = require('fs');
const { PNG } = require('pngjs');

const width = 512;
const height = 512;
const png = new PNG({ width, height });

for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
        const idx = (width * y + x) << 2;
        // Blue background #006064 (from app theme)
        png.data[idx] = 0x00;
        png.data[idx + 1] = 0x60;
        png.data[idx + 2] = 0x64;
        png.data[idx + 3] = 0xff;

        // Draw 'C' roughly
        if (x > 100 && x < 412 && y > 100 && y < 412) {
             // Border
             if ( (x < 150 || y < 150 || y > 362) && !(x > 362 && y > 150 && y < 362) ) {
                 png.data[idx] = 0xff;
                 png.data[idx + 1] = 0xff;
                 png.data[idx + 2] = 0xff;
             }
        }
    }
}

png.pack().pipe(fs.createWriteStream('www/res/icon.png'));
