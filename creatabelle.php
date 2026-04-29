<?php
    $db_server_name = "localhost";
    $db_username = "root";
    $db_password = ""; 
    $db_name_database = "colonnine_ricarica";
    
    $db_connessione = new mysqli($db_server_name, $db_username, $db_password, $db_name_database);           //l'ordine delle variabili e' prestabilito: ha una logica

    if($db_connessione->connect_errno == 0){
        echo "Connessione riuscita";
    }else{
        echo "Errore di connessione".$db_connessione->errno;
        echo "Descrizione dell'errore: ".$db_connessione->error;
    }
    $db_sql="CREATE TABLE IF NOT EXISTS COLONNINA(
        id_colonnina varchar(20) primary key,
        nclienti int(3) not null,
        consumo int(3) not null,
        profitto int(4),
        runtime int(3)
    );";  //il primo ; è legato al crea tabella e il secondo alla query
    if($db_connessione->query($db_sql)){
        echo"tabella creata correttamente";
    }else{
        echo "ERRORE ERRORE!";
    }
    $db_connessione->close(); //una connessione si apre  e si chiude

?>