Basic micropython library to control the OLED SSD1306 128x64 I2C with a micro:bit
#################################################################################


To create a bitmap, 

1. Create a bitmap with an image editor with only 2 bits per pixel (black and white) 
2. Use the LCDAssistant (http://en.radzio.dxp.pl/bitmap_converter/) to generate the hex data. 
3. Copy the hex data into the bitmap_converter.py file and run it on a computer.
4. Copy the generated file to the microbit using mu
5. Use the function show_bitmap to display the file

   .. image:: https://cdn.rawgit.com/fizban99/microbit_ssd1306/7f60064d/microbit_with_logo.jpg
      :width: 100%
      :align: center

Due to the low memory of the micro:bit, all functions except for show_bitmap, work in zoom mode, so the effective screen resolution is 64x32 pixels of twice the size.

Text is rendered using the internal microbit fonts.
