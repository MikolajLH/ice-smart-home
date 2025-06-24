package smarthome.devices.bulbs;

import com.zeroc.Ice.Current;

public class LEDBulbI extends BulbI implements DevicesIce.LEDBulb {
    double brightness;
    double defaultOnBrightness;

    public LEDBulbI(double defaultOnBrightness){
        this.defaultOnBrightness = defaultOnBrightness;
        this.brightness = 0.0;
    }

    public String info(Current __current) {
        return "LEDBulb " + __current.id + " " + __current.facet + " " + __current.operation + " " + __current.con;
    }

    @Override
    public void lightOn(Current __current) {
        this.brightness = this.defaultOnBrightness;
    }

    @Override
    public void lightOff(Current __current) {
        this.brightness = 0.0;
    }

    @Override
    public void switchLight(Current __current) {
        if(this.brightness > 0.0){
            this.brightness = 0.0;
        }
        else{
            this.brightness = defaultOnBrightness;
        }
    }

    @Override
    public boolean isOn(Current __current) {
        return this.brightness > 0.0;
    }

    @Override
    public void setBrightness(double brightness, Current __current) throws DevicesIce.ValueError {
        if(brightness < 0.0 || brightness > 1.0)
            throw new DevicesIce.ValueError("brightness has to be between 0 and 1");
        this.brightness = brightness;
    }

    @Override
    public void setDefaultBrightness(double brightness, Current __current) throws DevicesIce.ValueError {
        if(brightness <= 0.0 || brightness > 1.0)
            throw new DevicesIce.ValueError("brightness has to be between 0 and 1");

        this.defaultOnBrightness = brightness;
    }

    public double getBrightness(Current __current) {
        return this.brightness;
    }
}
