<?php
    $db_server_name = "localhost";
    $db_username = "root";
    $db_password = ""; 
    $db_name_database = "gestione_macchine";
    
    $db_connessione = new mysqli($db_server_name, $db_username, $db_password, $db_name_database);           //l'ordine delle variabili e' prestabilito: ha una logica

    if($db_connessione->connect_errno == 0){
        echo "Connessione riuscita";
    }else{
        echo "\nErrore di connessione".$db_connessione->errno;
        echo " \nDescrizione dell'errore: ".$db_connessione->error;
    }
    $db_sql="CREATE TABLE IF NOT EXISTS dati_macchine(
        id_colonnina VARCHAR(50) primary key,
        clienti_day INT not null,
        consumo INT not null,
        profitto INT,
        runtime VARCHAR(20),
        posizione TEXT
    );";  //il primo ; è legato al crea tabella e il secondo alla query
    if($db_connessione->query($db_sql)){
        echo"\ntabella creata correttamente";
    }else{
        echo "\nERRORE ERRORE!";
    }
    $db_connessione->close(); //una connessione si apre  e si chiude
    echo "\nTra 5 secondi tornerai alla pagina di index";
    header("Refresh:5 ; URL=home.html"); //dopo 5 secondi torni alla pagina di index
?>