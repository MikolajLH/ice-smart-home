package smarthome.devices.bulbs;

import com.zeroc.Ice.Current;


public class BulbI implements DevicesIce.Bulb {
    boolean on;

    public BulbI() {
        this.on = false;
    }

    @Override
    public String info(Current __current) {
        return "Bulb " + __current.id + " " + __current.facet + " " + __current.operation + " " + __current.con;
    }

    @Override
    public void lightOn(Current __current) {
        this.on = true;
    }

    @Override
    public void lightOff(Current __current) {
        this.on = false;
    }

    @Override
    public void switchLight(Current __current) {
        this.on = !this.on;
    }

    @Override
    public boolean isOn(Current __current) {
        return this.on;
    }
}
