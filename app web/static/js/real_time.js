$(document).ready(function(){
var label_info_dist = document.getElementById("label_info_dist");
var info_dist = document.getElementById("info_dist");
var info_position = document.getElementById("info_position");
var btn_arreter = document.getElementById("arreter");
var ripple = document.getElementById("ripple");
var alert_status; var list_requests_post=[]; var list_requests_get=[];
var id_watch_position; var is_active=true;
var current_position = {latitude:0, longitude:0};
var $request_get; var $request_post;
// Option de la géolocalisation par le navigateur
var options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

console.log("REAL TIME TEMPLATE");
handleLocation();
$("#arreter").on("click", stop);

/* FONCTION APPELE LORSQUE LE BOUTTON ARRETE EST CLIQUE*/
function stop(e){
  e.preventDefault();
  is_active=false;
  var infos = document.getElementById("infos");
  var deconnection_progress = document.getElementById("deconnection_progress");
  infos.style.display = "none";// ENLEVER LES INFORMATIONS 
  deconnection_progress.style.display = "block";// AFFICHAGE DE DECONNECTION EN COURS
  navigator.vibrate(0);// ARRET DES VIBRATIONS SI UNE EST EN COURS
  /* ANNULATION DES REQUETES EN COUR*/
  abort_requests(list_requests_get); // ANNULATION DES REQUEST POST ET GET SI LE BOUTTON ARRETER EST CLIQUE
  abort_requests(list_requests_post);
  alert_status=0;
  navigator.geolocation.clearWatch(id_watch_position); // SUPPRESSION DE LA MISE A JOUR DE LA POSITION
  var $req = dropUserFromDB(); // ENVOI SIGNAL SUPPRESION DE L UTILISATEUR DANS LA BASE DE DONNEE
  $req.done(function (){
    window.location = "/";
  })
  
}

/* FONCTION ANNULANT UNE LISTE DE REQUETTES*/
function abort_requests(list_requests){
  for (var i = list_requests.length - 1; i >= 0; i--) {
    if (list_requests[i] != null){ list_requests[i].abort(); list_requests[i]=null;}
  }
}
/* FONCTION RECUPERANT LA POSITION DE L UTILISATEUR A TRAVERS LE NAVIGATEUR*/
function handleLocation() {
  if (navigator.geolocation){
   id_watch_position=navigator.geolocation.watchPosition(sucess_pos, error_pos_watch, options);
  } 
  else {
    alert('Votre navigateur est imcompatible. Merci de changer de navigateur.')}
};

/* FONCTION APPELEE EN CAS DE SUCCES DE RECUPERATION DE LA POSITION PAR LE NAVIGATEUR*/
function sucess_pos(position) {
  console.log("Mise à jour de la position");
  current_position['latitude'] = position.coords.latitude;
  current_position['longitude'] = position.coords.longitude;
  var accuracy = position.coords.accuracy;
  console.log(position);

  info_position.innerHTML = "Estimation de votre position:" + 
                            "<br><strong>Latitude</strong>: " + current_position.latitude +
                            "<br><strong>Longitude</strong>: " + current_position.longitude + 
                            "<br><strong>Précision</strong>: " + accuracy + "m";
  info_position.style['font-size'] = "14px";
   realTimeDistanceComputation(); // ENVOIS DES DONNEES A FLASK POUR LA MISE A JOUR DE LA POSITION ET LE CALCULE DES DISTANCES
};


/* FONCTION APPELE EN D ERREUR DU SUIVI DE LA POSITION DE L UTILISATEUR, C EST A DIRE SI LA POSITION EST FIXE */
function error_pos_watch(err){
  navigator.geolocation.getCurrentPosition(sucess_pos, error_pos, options);
};
/* FONCTION APPELE EN CAS D ERREUR DE RECUPERATION DE LA POSITION DE L UTILISATEUR PAR LE NAVIGATEUR*/
function error_pos(err){
  alert("Erreur dans lors de la mise à jour de votre position!");
};


/* FONCTION APPELLE CHAQUE interval_freq QUI CALCUL DE LA DISTANCE DE L UTILISATEUR
PAR RAPPORT AUX AUTRES*/
function realTimeDistanceComputation() {
  if (is_active)
  {
        //handleLocation(); // MISE A JOUR DE LA POSITION DE L UTILISATEUR
        $request_get = $.get({
          url:"/realtime/start", 
          data:{},
          success:handle_response_real_time,
          dataType:"json"});

        function handle_response_real_time(response) {
          dist_closest_user = response.dist_closest_user;
          info_dist.style.display="block";
          info_dist.innerHTML = "La personne la plus proche de vous est à " + `<strong>${parseFloat(dist_closest_user).toFixed(2)}</strong>` + "m" ;
          info_dist.style['font-size'] = "14px";
            alert_status = response.alert;
            if(alert_status == 1){
              ripple.className = "ripple_red";
              navigator.vibrate(100000000);// ACTIVATION DE LA VIBRATION INFINIT
            }
            else{ripple.className = "ripple_green";
            navigator.vibrate(0);} // ARRET DE VIBRATION SI UNE EST EN COURS
          }

          xhr = $request_get;          
          xhr.done(function (){// SI LA REQUETE GET EST ACCOMPLIE, METTRE A JOUR LA POSITION ET ENVOI DES DONNEES A FLASK
              latlng = {"lat":current_position.latitude, "lng":current_position.longitude};
              sendDataToFlask(is_active, "/realtime/latlng", latlng, list_requests_post); // ENVOI DES COORDONNEES A FLASK
              console.log("Readyyyyy OKKKKKKK");
          });
    }
  }


/* ENVOI UNE REQUETE DE SUPPRESSION DE L UTILISATEUR DE LA BASE DE DONNEE*/
function dropUserFromDB(){
  var $req = $.post({
    url:"/realtime/stop",
    data: {},
    success: handle_response_stop,
    dataType:"json"});
    function handle_response_stop(response) {};
  return $req
}      

})