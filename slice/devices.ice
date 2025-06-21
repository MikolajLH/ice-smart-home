#pragma once
module DevicesIce
{
    struct Pixel {
        double value;
    }

    sequence<Pixel> PixelBuffer;

    struct Frame {
        int rows;
        int cols;
        PixelBuffer buffer;
    }

    interface Device {
        string info();
    }

    interface Camera extends Device {
        Frame getFrame();
    }
}