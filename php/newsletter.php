<?php
// Traitement de l'inscription newsletter Qibla (remplace Netlify Forms).
// Compatible o2switch (mail() natif, sendmail local).
// Note : ceci notifie seulement l'adresse éditoriale par e-mail ; pour une vraie gestion
// de liste de diffusion (envoi de campagnes), brancher plus tard un service dédié
// (Brevo, Mailjet...) est recommandé plutôt que de garder ce script comme base de données.

header('Content-Type: application/json; charset=utf-8');

$destinataire = 'qibla.mosk@gmail.com';

function champ($nom) {
    return isset($_POST[$nom]) ? trim($_POST[$nom]) : '';
}

function nettoie_entete($valeur) {
    return str_replace(["\r", "\n"], '', $valeur);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'erreur' => 'Méthode non autorisée']);
    exit;
}

$email = champ('email');

if (champ('site-web') !== '') {
    echo json_encode(['ok' => true]);
    exit;
}

if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'erreur' => 'E-mail invalide']);
    exit;
}

$email_propre = nettoie_entete($email);

$sujet = '[Qibla] Nouvelle inscription newsletter';
$corps = "Nouvelle inscription : $email_propre\n";
$entetes = "From: Qibla <no-reply@qiblamosk.com>\r\n" .
           "Reply-To: $email_propre\r\n" .
           "Content-Type: text/plain; charset=UTF-8";

$envoye = @mail($destinataire, $sujet, $corps, $entetes);

if ($envoye) {
    echo json_encode(['ok' => true]);
} else {
    http_response_code(500);
    echo json_encode(['ok' => false, 'erreur' => "L'envoi a échoué"]);
}
