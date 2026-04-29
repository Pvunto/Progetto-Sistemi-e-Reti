<!DOCTYPE html>
<html>
<head>
    <title>Stampa Tabella</title>
    <link rel="stylesheet" href="CSS/stampatabella.css">
</head>
<body>
    <h1>Dati della Tabella COLONNINA</h1>
<?php
    $db_server_name = "localhost";
    $db_username = "root";
    $db_password = ""; 
    $db_name_database = "colonnine_ricarica";
    
    $db_connessione = new mysqli($db_server_name, $db_username, $db_password, $db_name_database);

    if($db_connessione->connect_errno == 0){
        echo "<p class='success'>Connessione riuscita</p>";
    }else{
        echo "<p class='error'>Errore di connessione: ".$db_connessione->errno."</p>";
        echo "<p class='error'>Descrizione dell'errore: ".$db_connessione->error."</p>";
    }

    $db_sql="SELECT id_colonnina, nclienti, consumo, profitto, runtime FROM COLONNINA;";

    $risultato=$db_connessione->query($db_sql);

    if($risultato){
        if($risultato->num_rows == 0){
            echo "<p class='error'>Tabella vuota</p>";
        }else{
            $stampa="
            <table>
                <tr>
                <th>id_colonnina</th>
                <th>nclienti</th>
                <th>consumo</th>
                <th>profitto</th>
                <th>runtime</th>
            </tr>";
            while($riga=$risultato->fetch_assoc()){
                $stampa=$stampa."<tr>";
                $stampa=$stampa."<td>".$riga['id_colonnina']."</td>";
                $stampa=$stampa."<td>".$riga['nclienti']."</td>";
                $stampa=$stampa."<td>".$riga['consumo']."</td>";
                $stampa=$stampa."<td>".$riga['profitto']."</td>";
                $stampa=$stampa."<td>".$riga['runtime']."</td>";
                $stampa=$stampa."</tr>";
            }
            $stampa=$stampa."</table>";
            echo $stampa;
        }
    }else{
        echo "<p class='error'>ERRORE nella query!</p>";
    }
    $db_connessione->close();
?>
</body>
</html>