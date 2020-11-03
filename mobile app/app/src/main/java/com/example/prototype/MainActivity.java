package com.example.prototype;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.DialogInterface;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.webkit.*;
import android.widget.ProgressBar;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import static android.Manifest.permission.*;

/* CLASSE D ACTIVITE PRINCIPALE */
public class MainActivity extends AppCompatActivity {
    private final int REQUEST_CODE = 1;
    private WebView webview; // ATTRIBUT WebView POUR AFFICHER LA PAGE WEB DU PROTOTYPE
    private  final int ALERT_STATUS_UPDATE_INTERVAL = 10000; // CODE UTILISE POUR LES DEMANDES DE PERMISSIONS
    public static ProgressBar progress_bar; // BAR DE PROGRESSION UTILISE LORS DU CHARGEMENT DE LA PAGE WEB
    public static TextView text_progression; // TEXTE DE DESCRIPTION DU CHARGNEMENT DE LA PAGE WEB

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        requestPermissions(); // DEMANDES DES PERMISSIONS (POSITION, etc...)
        WebViewSettings(); // CONFIGURATION DU NAVIGATEUR QUI AFFICHERA LA PAGE WEB
        text_progression = (TextView) findViewById(R.id.textview);
        progress_bar = (ProgressBar) findViewById(R.id.pBar);
    }

    // FONCTION PERMETTANT LES DEMANDES D AUTORISATIONS NECESSAIRES
    public void requestPermissions(){
            if (checkPermission(INTERNET)){HandlePermissionDialog(INTERNET, "L'accès à internet est nécessaire.");}
            if (checkPermission(ACCESS_FINE_LOCATION)){HandlePermissionDialog(ACCESS_FINE_LOCATION, "L'accès à votre position est nécessaire.");}
            if (checkPermission(ACCESS_COARSE_LOCATION)){HandlePermissionDialog(ACCESS_COARSE_LOCATION, "L'accès à votre position est nécessaire.");}
            if (checkPermission(VIBRATE)){HandlePermissionDialog(VIBRATE, "Veuillez autoriser la vibration du téléphone.");}
    }

    // FONCTION VERIFIANT SI UNE PERMISSION EST DEJA ACCORDEE
    private boolean checkPermission(String perm){
        return PackageManager.PERMISSION_GRANTED != ActivityCompat.checkSelfPermission(this, perm);
    }

    //  FONCTION PERMETTANT D AFFICHER UNE DE BOITES DE DIALOGUES POUR LES DEMANDES D AUTORISATIONS
    private void HandlePermissionDialog(final String perm, String msg){
        if (ActivityCompat.shouldShowRequestPermissionRationale(this, perm)) {
            new AlertDialog.Builder(MainActivity.this)
                    .setTitle("Autorisation nécessaire")
                    .setMessage(msg)
                    .setPositiveButton("Autoriser", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            requestPermission(perm);
                        }
                    })
                    .setNegativeButton("Refuser", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            dialog.dismiss();
                        }
                    })
                    .create()
                    .show();
        }else{requestPermission(perm);}
    }

    // CONFIGURATION DU NAVIGATEUR CHROME PERMETTANT D AFFICHER LA PAGE WEB
    @SuppressLint("SetJavaScriptEnabled")
    public void WebViewSettings(){
        webview = (WebView) findViewById(R.id.webview);
        webview = (WebView) findViewById(R.id.webview);
        WebSettings websettings = webview.getSettings();
        websettings.setDomStorageEnabled(true);
        websettings.setJavaScriptEnabled(true); // ACTIVATION DE JAVASCRIPT
        websettings.setJavaScriptCanOpenWindowsAutomatically(true);
        websettings.setBuiltInZoomControls(true);
        websettings.setSupportZoom(true);
        websettings.setLoadWithOverviewMode(true);
        websettings.setGeolocationEnabled(true); // ACTIVATION DE LA GEOLOCATION AVEC LE NAVIGATEUR
        webview.setHapticFeedbackEnabled(true); // ACTIVATION DE LA VIBRATION DU NAVIGATEUR
        webview.setVerticalScrollBarEnabled(true);
        webview.setWebViewClient(new WebViewClient());
        webview.setWebChromeClient(new GeoWebChromeClient(this)); // UTILISATION D UNE EXTENSION DE CHROME POUR GERER LA GEOLOCALISATION
        webview.loadUrl("https://prototype-distance-securitaire.ew.r.appspot.com/"); // CHARGEMENT DE LA PAGE
    }

    // ACTIVATION DU RETOUR EN ARRIERE
    @Override
    public void onBackPressed() {
        if(webview.canGoBack()){
            webview.goBack();
        }else{
        super.onBackPressed();}
    }

    // FONCTION APPELE LORSQU UN RESULAT DE PERMISSION EST DONNE
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if (requestCode == REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                //abc
            } else {
            }
        }
    }

    // FONCTION PERMETTANT LA DEMANDE DE PERMISSION
    private void requestPermission(String perm){
        ActivityCompat.requestPermissions(MainActivity.this, new String[] {perm}, REQUEST_CODE);
    }


    /* INTERFACE JAVA SCRIPT POUR RECUERR DES DONNEES DE JAVA SCRIPT VERS ANDROID ET VICE VERSA
    public class JSInterface{
        Context context;
        JSInterface(Context c){context=c;}
        @JavascriptInterface
        public void setAlertStatus(String value) {
            alertStatus = Integer.valueOf(value);
            Log.v("Alert Status", String.valueOf(alertStatus));
        }
    }
    DEFINITION D UNE INTERFACE JAVASCRIPT POUR RECUPERER DES DONNEES DE JAVASCRIPT
    public void getAlertStatusFromJS(){
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
            webview.evaluateJavascript("javascript:JSI.setAlertStatus(getAlertStatus());", new ValueCallback<String>() {
                @Override
                public void onReceiveValue(String value) {
                    Log.v("Alert Status value from JS", value);
                }
            });
        } else {
            webview.loadUrl("javascript:JSI.setAlertStatus(getAlertStatus());");
        }
    }


    @Override
    public void onDestroy() {
        super.onDestroy();
        stopUpdateStatus();
    }

    Runnable statusChecker = new Runnable() {
        @Override
        public void run() {
            try {
                getAlertStatusFromJS();
            } finally {// MISE A JOUR PERIODIQUE DU STATUS ALERT
                alertStatusHandler.postDelayed(statusChecker, ALERT_STATUS_UPDATE_INTERVAL);
            }
        }
    };

    void startUpdateStatus() {// MISE A JOUR DU STATUS ALERT
        statusChecker.run();
    }

    void stopUpdateStatus() {// ARRET DE LA MISE A JOUR DU STATUS ALERT
        alertStatusHandler.removeCallbacks(statusChecker);
    }*/
}
