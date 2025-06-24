package smarthome.devices.cameras;

import com.zeroc.Ice.Current;

import DevicesIce.Camera;
import DevicesIce.Pixel;
import DevicesIce.Frame;



public class CameraI implements Camera {
    Frame currentFrame;

    public CameraI(int rows, int cols) {
        this.currentFrame = new Frame(rows, cols, new Pixel[rows * cols]);
        for(int i = 0; i < rows * cols; i++){
            this.currentFrame.buffer[i] = new Pixel(0.0);
        }
    }

    @Override
    public String info(Current __current) {
        return "Camera " + __current.id + " " + __current.facet + " " + __current.operation + " " + __current.con;
    }

    @Override
    public Frame getFrame(Current __current) {
        for(int r = 0; r < this.currentFrame.rows; r++){
            for(int c = 0; c < this.currentFrame.cols; c++){
                this.currentFrame.buffer[r * this.currentFrame.cols + c].value = Math.random();
            }
        }
        return this.currentFrame;

    }
}
