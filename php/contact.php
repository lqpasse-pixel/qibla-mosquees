<?php
// Traitement du formulaire de contact Qibla (remplace Netlify Forms).
// Compatible o2switch (mail() natif, sendmail local).

header('Content-Type: application/json; charset=utf-8');

$destinataire = 'qibla.mosk@gmail.com';

function champ($nom) {
    return isset($_POST[$nom]) ? trim($_POST[$nom]) : '';
}

function nettoie_entete($valeur) {
    // Empêche l'injection d'en-têtes SMTP via un champ contenant des retours à la ligne.
    return str_replace(["\r", "\n"], '', $valeur);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'erreur' => 'Méthode non autorisée']);
    exit;
}

$nom = champ('nom');
$email = champ('email');
$message = champ('message');

// Piège à robots : champ caché "site-web", normalement toujours vide pour un humain.
if (champ('site-web') !== '') {
    echo json_encode(['ok' => true]);
    exit;
}

if ($nom === '' || $email === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'erreur' => 'Champs invalides']);
    exit;
}

$nom_propre = nettoie_entete($nom);
$email_propre = nettoie_entete($email);

$sujet = '[Qibla] Nouveau message de contact';
$corps = "Nom : $nom_propre\nE-mail : $email_propre\n\nMessage :\n$message\n";
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
