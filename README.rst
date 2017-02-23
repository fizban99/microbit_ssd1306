Basic micropython library to control the OLED SSD1306 128x64 I2C with a micro:bit
#################################################################################

This library allows to control the typical low cost 0,96" OLED display sold in Amazon and eBay from a micro:bit.  

Due to the low memory of the micro:bit, all functions except for show_bitmap, work in zoom mode, so the effective screen resolution is 64x32 dots of 4x4 pixels of size.

Text is rendered using the internal microbit fonts.

The library is distributed in different files to allow importing only the required funitons in order to reduce memory consumption.

Main features
=============

* Load a 128x64 bitmap file
* Set and get pixel value 
* Render of text using the internal micro:bit font
* Support of micro:bit Image object by transforming it into a stamp that can be displayed
* Sample programs demonstrating the different functions

Preparation and displaying of a bitmap image
============================================

1. Create a bitmap with an image editor with only 2 bits per pixel (black and white) 
2. Use the LCDAssistant (http://en.radzio.dxp.pl/bitmap_converter/) to generate the hex data. 
3. Copy the hex data into the bitmap_converter.py file and run it on a computer.
4. Flash a completely empty file from mu.
5. Copy the generated file to the microbit using the file transfer function in mu
6. Create a main.py file, import sdd1206_bitmap and use the function show_bitmap to display the file

   .. image:: https://cdn.rawgit.com/fizban99/microbit_ssd1306/7f60064d/microbit_with_logo.jpg
      :width: 100%
      :align: center

Usage
=====

show_bitmap(<filename>)
-----------------------

Will display on the OLED screen the image stored in the file 

.. code-block:: python

   from SSD1306_bitmap import show_bitmap
   show_bitmap("microbit_logo")


