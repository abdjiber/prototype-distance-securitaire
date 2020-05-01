$(document).ready(function(){
/* DEFINITION DE VARIABLES GLOBALES*/
var ripple = document.getElementById("ripple");
var btn_demarer = document.getElementById("demarer");
var description_city = document.getElementById("description_city");
var form = document.getElementById("form");
var distance_min = document.getElementById("distance");
var description_distance = document.getElementById("description_distance");
var connexion = document.getElementById("connexion");
var connection_progress = document.getElementById("connection_progress");
var ville = ""; var interval_freq=10000; // FREQUENCE D APPEL DE LA FONCTION REALTIME EN MILISECONDES


$("#demarer").on("click", start);
$("#cities").focus(focus_city);
$("#distance").focus(focus_distance);
$(".input").val("");

function focus_city(e){
    e.preventDefault();
    display_msg(description_city, "Veuillez choisir votre ville dans la liste.", false);
};

function focus_distance(e){
    e.preventDefault();
    display_msg(description_distance, "Distance minimale par rapport aux autres personnes", false);
};

/* FONCTION AFFICHANT DES ERREURS DE SAISIE*/
function display_msg(element, msg, error){
    element.style.display = "block";
    element.innerHTML = msg;
    if (error){element.style.color = "red";}
    else{element.style.color = "black";}
}


/* FONCTION APPELEE LORSQUE LE BOUTTON DEMARRER EST APPUYE*/
function start(e){
  e.preventDefault();
  is_active=true;
  ville = $("#cities").val();
  min_distance = $("#distance").val();
  /* CONTROL DE SAISIE*/
  if (ville == ""  || min_distance == "" || !cities.includes(ville)){
    if (ville == ""){// VILLE NON RENSEIGNE
    display_msg(description_city, "Veuillez renseigner votre ville.", true);
    }
  else{// VILLE RENSEIGNE MAIS INCORRECTE (N EST PAS DANS LA LISTE)
    display_msg(description_city, "Ville incorrect! Veuillez choisir dans la liste.", true);}
  if (min_distance == ""){// DISTANCE NON RENSEIGNE
    display_msg(description_distance, "Veuillez renseigner votre distance minimale.", true);
    }
  }
  else{
      if (parseFloat(min_distance) < 1){// DISTANCE INFERIEURE A 1
        display_msg(description_distance, "La distance doit être au moins égale à 1.", true);
      }
    else{// SI LA VILLE ET LA DISTANCE SONT CORRECTE
    ripple.className = "ripple_green";
    var city_dist = {ville: ville, min_distance:min_distance, uuid:uuidv4()};
    var form_and_animation = document.getElementById("form_and_animation");
    form_and_animation.style.display = "none"; 
    connection_progress.style.display = "block"; // AFFICHAGE DE "Connection en cours"
    var $request_post = sendDataToFlask(true, "/connection", city_dist, []);
    // SI LA REQUETE GET EST ACCOMPLIE, METTRE A JOUR LA POSITION ET ENVOI DES DONNEES A FLASK
    console.log("Ready state change");
    console.log($request_post);
    $request_post.done(function(){// REDIRECTION
      connection_progress.style.display = "none";
      window.location = "/realtime";
    })
        
    }
  }
}
/* GENERATION DE UUID */
/* https://stackoverflow.com/questions/105034/how-to-create-guid-uuid */
function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}


});// FIN FONCTION DOCUMENT READY