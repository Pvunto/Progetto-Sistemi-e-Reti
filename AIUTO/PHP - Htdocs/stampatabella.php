<!DOCTYPE html>
<html>
<head>
    <title>Stampa Tabella</title>
    <link rel="stylesheet" href="stampatabella.css">
</head>
<body>

<h1>Dati della Tabella COLONNINA</h1>

<?php
$db_server_name = "localhost";
$db_username = "root";
$db_password = "";
$db_name_database = "ricarica_colonnine";

$db_connessione = new mysqli(
    $db_server_name,
    $db_username,
    $db_password,
    $db_name_database
);

// controllo connessione
if ($db_connessione->connect_errno) {
    echo "<p class='error'>Errore di connessione: " . $db_connessione->connect_error . "</p>";
    exit();
}

echo "<p class='success'>Connessione riuscita</p>";

// query
$db_sql = "SELECT id_macchina, clienti_day, consumo, profitto, runtime, posizione
           FROM informazioni_colonnine
           ORDER BY TIME_TO_SEC(runtime) DESC";

$risultato = $db_connessione->query($db_sql);

if (!$risultato) {
    echo "<p class='error'>Errore nella query!</p>";
    exit();
}

if ($risultato->num_rows == 0) {
    echo "<p class='error'>Tabella vuota</p>";
} else {

    echo "
    <table>
        <tr>
            <th>id_colonnina</th>
            <th>nclienti</th>
            <th>consumo</th>
            <th>profitto</th>
            <th>runtime</th>
            <th>posizione</th>
        </tr>";

    while ($riga = $risultato->fetch_assoc()) {
        echo "<tr>";
        echo "<td>" . $riga['id_macchina'] . "</td>";
        echo "<td>" . $riga['clienti_day'] . "</td>";
        echo "<td>" . $riga['consumo'] . "</td>";
        echo "<td>" . $riga['profitto'] . "</td>";
        echo "<td>" . $riga['runtime'] . "</td>";
        echo "<td>" . $riga['posizione'] . "</td>";
        echo "</tr>";
    }

    echo "</table>";
}

$db_connessione->close();
?>

</body>
</html>