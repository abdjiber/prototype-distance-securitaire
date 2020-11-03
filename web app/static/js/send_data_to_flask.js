/**
 * FONCTION POUR ENVOYER DES DONNEES A FLASK A TRAVERS UNE REQUETE POST
*/
function sendDataToFlask(is_active, route, data, list_requests_post) {
    console.log("Sending data to FLASK to " + route + is_active);
    var $request_post;
    if (is_active) {
        $request_post = $.post({
          url:route,
          data: data,
          success: handle_response,
          dataType: "json"});
      if (list_requests_post != []) {
            list_requests_post.push($request_post); // AJOUT DE LA REQUETE DANS LA LISTE
        }
      function handle_response(response) {}
    }
    return $request_post
}