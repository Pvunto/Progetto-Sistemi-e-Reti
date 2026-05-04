<?php
    $db_server_name = "localhost";
    $db_username = "root";
    $db_password = "";
    $db_name_database = "colonnine_ricarica";
    $db_connessione = new mysqli($db_server_name, $db_username, $db_password, $db_name_database);

    // Query SQL per eliminare la tabella
    $db_sql = "DROP TABLE IF EXISTS COLONNINA";

    // Esegui la query di eliminazione
    $db_connessione->query($db_sql);
    echo "Tabella COLONNINA eliminata con successo.";
    $db_connessione->close();
    echo "\nTra 5 secondi tornerai alla pagina di index";
    header("Refresh:5 ; URL=home.html"); //dopo 5 secondi torni alla pagina di index
?>

