package com.example.prototype;
import android.content.Context;
import android.content.DialogInterface;
import android.util.Log;
import android.view.View;
import android.webkit.GeolocationPermissions;
import android.webkit.JsResult;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.widget.ProgressBar;
import android.widget.TextView;
import androidx.appcompat.app.AlertDialog;

// CLASS EXTENSION DE GOOGLE CHROME
public class GeoWebChromeClient extends WebChromeClient {
    private Context context;

    GeoWebChromeClient(Context context){
        super();
        this.context = context;
    }

    // DEMANDE D AUTORISATION DE LA GEOLOCATION AVEC LE NAVIGATEUR AVEC UNE BOITE DE DIALOGUE
    @Override
    public void onGeolocationPermissionsShowPrompt(final String origin, final GeolocationPermissions.Callback callback) {
        AlertDialog.Builder adb = new AlertDialog.Builder(this.context);
        adb.setTitle("Autorisation d'accès à votre position");
        adb.setMessage("Veuillez autoriser l'accès à votre position pour continuer.");
        // SI LA DEMANDE EST REFUSEE, NE PAS ENREGISTRER LE CHOIX DE L UTILISATEUR C EST A DIRE, REDEMANDER A CHAQUE
        adb.setNegativeButton("Refuser", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int which) {
                callback.invoke(origin, false, false);
            }
        });
        // SINON ON ENREGISTRE L AUTORISATION DE GEOLOCALISATION
        adb.setPositiveButton("Autoriser", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int which) {
                callback.invoke(origin, true, true);
            }
        });
        adb.show();
    }

    // CONFIRMATION D ALERTE JAVA SCRIPT
    @Override
    public boolean onJsAlert(WebView view, String url, String message, JsResult result) {
        Log.v("JS Alert", message);
        result.confirm();
        return true;
    }

    // FONCTION UTILISEE POUR LA BAR DE PROGRESSION
    @Override
    public void onProgressChanged(WebView view, int newProgress) {
        super.onProgressChanged(view, newProgress);
        ProgressBar pbar = MainActivity.progress_bar;
        if(newProgress < 100 && pbar.getVisibility() == ProgressBar.GONE){
            pbar.setVisibility(ProgressBar.VISIBLE);
            MainActivity.text_progression.setVisibility(View.VISIBLE);
        }

        pbar.setProgress(newProgress);
        if(newProgress == 100) {
            pbar.setVisibility(ProgressBar.GONE);
            MainActivity.text_progression.setVisibility(View.GONE);
        }
    }

}
