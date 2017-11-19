<?php
    $host = "127.0.0.1";
    $port1 = "10000";
    $aragorn = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    $lim_bytes = 1000000000; //1 GB

    //Atribui-se uma identidade ao servidor
    socket_bind($aragorn, $host, $port1);

    //Espera por conexão ("ouve" o meio)
    socket_listen($aragorn, SOMAXCONN);
    //echo "Esperando um cliente...\n";

    //Aceita a conexão do cliente, se e enquanto for possível
    $frodo;
    $anel;
    $sequencia_de_bytes;
    $sequencia_de_bytes_retorno_do_server;
    $keep_going;

    const log = " log_cTrans";
    $arquivo = fopen(log, "w") or die("Unable to open file!");


while (1) {
    echo "Esperando um cliente...\n";  
    fwrite($arquivo," Espera por cliente aplicacao   "  );
    fwrite($arquivo, date('m/d/Y h:i:s a', time()) );	
    while(($frodo = socket_accept($aragorn)) != FALSE) {

        //Lê-se o conteúdo do socket com um tamanho especificado e o escreve num arquivo
        //Perceba que há um limite de bytes a serem lidos
        echo "Servidor iniciado!\n";
        $sequencia_de_bytes = socket_read($frodo, $lim_bytes, PHP_BINARY_READ);
	fwrite($arquivo,"\n Recebe requisicao de aplicacao    "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
	
        fwrite($arquivo,"\n Recebe dados de aplicacao   "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
        //iniciando cliente que irá se comunicar com a camada inferior
        $port2 = 10001;
        //Abre-se e faz o teste do socket
        $saruman = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        
        if ($saruman === false) {
            echo "Deu ruim. Tá aqui o motivo: " . socket_strerror(socket_last_error()) . "\n";
        }
        else {
            echo "Parabéns! Socket criado.\n";
        }

//Conectar-se ao servidor
	fwrite($arquivo,"\n Conecta com fisica   "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
        echo "Tentativa de conectar-se a $host pela porta $port2...";
        $result = socket_connect($saruman, $host, $port2);
        if ($result === false) {
            echo "Deu ruim... Tenta entender o motivo: " . socket_strerror(socket_last_error($saruman)) . "\n";
        } else {
            echo "Parabéns! Conectado a $host.\n";
        }

//Escreve o conteúdo do arquivo no socket
	fwrite($arquivo,"\n Envia para fisica   "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
        socket_write($saruman, $sequencia_de_bytes, strlen($sequencia_de_bytes));
        $sequencia_de_bytes_retorno_do_server = socket_read($saruman, $lim_bytes, PHP_BINARY_READ);
	fwrite($arquivo,"\n Recebe da fisica   "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );

        echo $sequencia_de_bytes_retorno_do_server;

        socket_write($frodo, $sequencia_de_bytes_retorno_do_server, strlen($sequencia_de_bytes_retorno_do_server));
        fwrite($arquivo,"\n  Retorna para aplicacao   "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
        socket_close($frodo);
        socket_close($saruman);
        break;
    }
}
    fwrite($arquivo,"\n Encerra conexoes   "  );
    fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
    //Encerra-se a conexão
    socket_close($aragorn);
    echo "Servidor terminado...\n";
    fclose($arquivo);
?>
