package br.com.slmm.meuiot;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private static final int PERMISSION_ALL = 1;

    String[] PERMISSIONS ={
            Manifest.permission.INTERNET,
            Manifest.permission.ACCESS_WIFI_STATE,
            Manifest.permission.ACCESS_NETWORK_STATE,
            Manifest.permission.CHANGE_WIFI_MULTICAST_STATE
    };

    private Button btnPesquisa;
    private WifiManager.MulticastLock multicastLock;

    // variaveis para o listview
    private ListView listView1;
    private ArrayAdapter<String> listAdapter1;
    private ArrayList<String> items;

    //tag para log
    private static final String TAG = "TI 502...";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (!hasPermissions(this, PERMISSIONS)){
            ActivityCompat.requestPermissions(this, PERMISSIONS,PERMISSION_ALL);
        }

        findViewById(R.id.button2).setOnClickListener((View)->{ finish(); });

        btnPesquisa = (Button)findViewById(R.id.button);
        btnPesquisa.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // dispara a pesquisa...
                if (listAdapter1 != null) {
                    listAdapter1.clear();
                }
                runThread();
            }
        });

        // preciso fazer um lock para o multicast poder trabalhar
        WifiManager wifi = (WifiManager)getApplicationContext().getSystemService(Context.WIFI_SERVICE);
        multicastLock = wifi.createMulticastLock("DS502 lock");
        multicastLock.acquire();

        // inicializa o list view a ser populado pela pesquisa
        listView1 = (ListView)findViewById(R.id.listPesquisa);
        items = new ArrayList<String>();
        listAdapter1 = new ArrayAdapter<String>(this, R.layout.simple_list_row, items);
        listView1.setAdapter(listAdapter1);

        listView1.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Toast toast = Toast.makeText(getApplicationContext(),
                        listView1.getItemAtPosition(i).toString(), Toast.LENGTH_LONG);
                toast.setGravity(Gravity.CENTER_HORIZONTAL | Gravity.CENTER_VERTICAL, 0,0);
                toast.show();
            }
        });

    }

    public static boolean hasPermissions(Context context, String...permissions){
        if (context != null && permissions != null){
            for (String permission: permissions){
                if (ActivityCompat.checkSelfPermission(context, permission) !=
                        PackageManager.PERMISSION_GRANTED){
                    return false;
                }
            }
        }
        return true;
    }

    private void runThread() {
        new Thread(){
            public void run() {
                DatagramSocket socket = null;
                InetAddress group = null;

                try {
                    group = InetAddress.getByName("239.255.255.250");
                    String msg = "M-SEARCH * HTTP/1.1\r\n" +
                            "HOST:239.255.255.250:1900\r\n" +
                            "MAN:\"ssdp:discover\"\r\n" +
                            "MX: 2\r\n" +
                            "ST: upnp:rootdevice\r\n\r\n";

                    socket = new DatagramSocket(1900);
                    socket.setReuseAddress(true);

                    byte[] bytes = msg.getBytes();
                    DatagramPacket hi = new DatagramPacket(bytes, bytes.length, group, 1900);

                    socket.send(hi);

                    socket.setSoTimeout(2000);
                    while (true) {
                        try {
                            DatagramPacket p = new DatagramPacket(new byte[300], 300);
                            socket.receive(p);
                            String s = new String(p.getData(), 0, p.getLength());
                            synchronized (items) {
                                items.add(s);
                            }
                        } catch (SocketTimeoutException e) {

                            break;
                        }
                    }

                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            synchronized (items) {
                                listAdapter1.notifyDataSetChanged();
                            }
                        }
                    });
                } catch (IOException ioException) {
                    ioException.printStackTrace();
                }

                finally {
                    if (socket != null) {
                        try {
                            socket.close();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
        }.start();
    }

}




















