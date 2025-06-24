package smarthome.devices.bulbs;

import DevicesIce.RGBColor;
import DevicesIce.ValueError;
import com.zeroc.Ice.Current;

public class RGBBulbI extends BulbI implements DevicesIce.RGBBulb {
    DevicesIce.RGBColor color;
    DevicesIce.RGBColor defaultColor;

    public RGBBulbI(DevicesIce.RGBColor c) {
        this.color = new DevicesIce.RGBColor(0, 0, 0);
        this.defaultColor = new DevicesIce.RGBColor(c.r, c.g, c.b);
    }

    public String info(Current __current) {
        return "RGBBulb " + __current.id + " " + __current.facet + " " + __current.operation + " " + __current.con;
    }

    @Override
    public void lightOn(Current __current) {
        this.color.r = this.defaultColor.r;
        this.color.g = this.defaultColor.g;
        this.color.b = this.defaultColor.b;
    }

    @Override
    public void lightOff(Current __current) {
        this.color.r = 0.0;
        this.color.g = 0.0;
        this.color.b = 0.0;
    }

    @Override
    public void switchLight(Current __current) {
        if(this.color.r > 0.0 || this.color.g > 0 || this.color.b > 0){
            this.color.r = 0;
            this.color.g = 0;
            this.color.b = 0;
        } else{
            this.color.r = this.defaultColor.r;
            this.color.g = this.defaultColor.g;
            this.color.b = this.defaultColor.b;
        }
    }

    @Override
    public boolean isOn(Current __current) {
        return this.color.r > 0.0 || this.color.g > 0 || this.color.b > 0;
    }

    @Override
    public RGBColor getColor(Current __current) {
        return this.color;
    }

    @Override
    public void setColor(RGBColor color, Current __current) {
        this.color.r = color.r;
        this.color.g = color.g;
        this.color.b = color.b;
    }

    @Override
    public void setDefaultColor(RGBColor color, Current __current) throws DevicesIce.ValueError{
        if(color.r <= 0 || color.r > 1 || color.g <= 0 || color.g > 1 || color.b <= 0 || color.b > 1){
            throw new ValueError("wrong rgb values for color");
        }
        this.defaultColor = color;
    }
}
