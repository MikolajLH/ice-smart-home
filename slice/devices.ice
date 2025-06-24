#pragma once
module DevicesIce
{
    exception ValueError{ string info; }

    struct Pixel {
        double value;
    }

    sequence<Pixel> PixelBuffer;

    struct Frame {
        int rows;
        int cols;
        PixelBuffer buffer;
    }

    struct RGBColor {
        double r;
        double g;
        double b;
    }


    interface Device {
        string info();
    }

    interface Camera extends Device {
        Frame getFrame();
    }

    interface Bulb extends Device {
        idempotent void lightOn();
        idempotent void lightOff();
        void switchLight();
        idempotent bool isOn();
    }

    
    interface LEDBulb extends Bulb {
        idempotent double getBrightness();
        idempotent void setBrightness(double brigthness) throws ValueError;
        void setDefaultBrightness(double brightness) throws ValueError;
    }

    
    interface RGBBulb extends Bulb {
        idempotent RGBColor getColor();
        idempotent void setColor(RGBColor color) throws ValueError;
        void setDefaultColor(RGBColor color) throws ValueError;
    }
}