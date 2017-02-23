Basic micropython library to control the OLED SSD1306 128x64 I2C with a micro:bit
#################################################################################

This library allows the micro:bit to control the typical low cost 0,96" OLED display sold in Amazon and eBay.  

Due to the low memory of the micro:bit, all functions except for show_bitmap, work in zoom mode, so the effective screen resolution is 64x32 dots of 4x4 pixels of size.

Text is rendered using the internal microbit fonts.

The library is distributed in different files to allow importing only the required funitons in order to reduce memory consumption.

.. contents::

.. section-numbering::


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

Library usage
=============


show_bitmap(filename)
+++++++++++++++++++++++


Displays on the OLED screen the image stored in the file *filename*. The image has to be encode as described in the previous section.

.. code-block:: python

   from SSD1306_bitmap import show_bitmap
   show_bitmap("microbit_logo")

set_px(x, y, color, draw=1)
+++++++++++++++++++++++++++++


Paints the pixel at position x, y (of a 64x32 coordinate system) with the corresponding color (0 dark or 1 lighted). 
If the optional parameter **draw** is set to 0 the screen will not be refreshed and **draw_screen()** needs to be called at a later stage, since multiple screen refreshes can be time consuming. This allows setting different pixels in the buffer without refreshing the screen, and finally refresh the display with the content of the buffer.

.. code-block:: python

   from SSD1306_px import set_px
   from SSD1306 import draw_screen
   set_px(10,10,1)
   set_px(20,20,0,0)
   draw_screen()


get_px(x, y)
++++++++++++


Returns the color of the given pixel (0 dark 1 lighted)

.. code-block:: python

   from SSD1306_px import get_px
   color=get_px(10,10)


add_text(x, y, text, draw=1)
++++++++++++++++++++++++++++++

Prints the text given by **text** at the row x and column y. The screen is divided into 12 columns and 5 rows. If the optional parameter **draw** is set to 0 the screen will not be refreshed and **draw_screen()** needs to be called at a later stage, since multiple screen refreshes can be time consuming. This allows writing different rows in the buffer without refreshing the screen, and finally refresh the display with the content of the buffer.

.. code-block:: python

   from SSD1306_text import add_text
   add_text(0, 2, "Hello, world")
   

create_stamp(img)
+++++++++++++++++

Creates a stamp from an Image object. A stamp is just a set of bytes that will be used to print the image on the OLED display. The function transforms any led value different than 0 to 1. This is used in combination of **draw_stamp** 


draw_stamp(x, y, stamp, color, draw=1)
++++++++++++++++++++++++++++++++++++++

Draws the stamp on the screen at the pixel position x, y. The stamp will be printed using **OR** if color is 1 and **NAND** if color is 0, effectively removing the stamp when color=0.

.. code-block:: python

   from SSD1306_stamp import create_stamp, draw_stamp
   from microbit import Image
   stamp = create_stamp(Image.HEART)
   draw_stamp(10, 10, stamp, 1)
   
