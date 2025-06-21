package smarthome;

import com.zeroc.Ice.Communicator;
import com.zeroc.Ice.Identity;
import com.zeroc.Ice.ObjectAdapter;
import com.zeroc.Ice.Util;
import smarthome.devices.cameras.CameraI;

public class Server {
    public void t1(String[] args){
        int status = 0;
        Communicator communicator = null;
        try{
            communicator = Util.initialize(args);
            ObjectAdapter adapter = communicator.createObjectAdapter("Adapter");

            adapter.add(new CameraI(5, 7), new Identity("camera", "cameras"));

            //adapter.add(new CameraI(5,5), new Identity("camera-1", "cameras"));
            //adapter.add(new PrinterI(), new Identity("printer-1", "devices"));

            adapter.activate();

            System.out.println("Entering event processing loop...");
            communicator.waitForShutdown();

        } catch (Exception e) {
            e.printStackTrace(System.err);
            status = 1;
        }
        if (communicator != null) {
            try {
                communicator.destroy();
            } catch (Exception e) {
                e.printStackTrace(System.err);
                status = 1;
            }
        }
        System.exit(status);
    }

    public static void main(String[] args) {
        Server server = new Server();
        server.t1(args);
    }
}
