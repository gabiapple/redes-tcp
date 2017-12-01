<?php

//Variaveis para conexao TCP
$seq=0;
$ack;
$window = 1000000000;

function exibePDU($pdu, $protocolo){
    echo "Porta origem: $pdu[0]\n";
    echo "Porta destino: $pdu[1]\n";
    if($protocolo == 'udp')
        echo "Tamanho: $pdu[2]\n";
    else{
        echo "Seq: $pdu[2]\n";
        echo "ACK: $pdu[3]\n";
        echo "Window: $pdu[4]\n";
    }
    echo "--------------------------------------\n";
}

function criaSegmentoUDP($porta_origem, $porta_destino,$mensagem){
    $length = sizeof($porta_origem) + sizeof($porta_destino) +  sizeof($mensagem);
    $segmento = $porta_origem."\n".$porta_destino."\n".$length."\n".$mensagem;
    echo "--------------------------------------\nGerando PDU da camada de transporte\n";
    exibePDU(explode("\n",$segmento),'udp');
    return $segmento;
}

function criaSegmentoTCP($porta_origem, $porta_destino,$mensagem){
    global $seq, $ack, $window;
    $seq++;
    $ack = strlen($mensagem);
    $segmento = $porta_origem."\n".$porta_destino."\n".$seq."\n".$ack."\n".$window."\n".$mensagem;
    echo "--------------------------------------\nGerando PDU da camada de transporte\n";
    exibePDU(explode("\n",$segmento),'tcp');
    return $segmento;
}

$host = "localhost";
$port1 = "10000";
$camada_superior = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
$lim_bytes = 1000000000; //1 GB
//Atribui-se uma identidade ao socket para se comunicar com a camada superior
socket_bind($camada_superior, $host, $port1);

//Espera por conexão ("ouve" o meio)
socket_listen($camada_superior, SOMAXCONN);

//Aceita a conexão do cliente, se e enquanto for possível
$conn_superior;
$sequencia_de_bytes;
$sequencia_de_bytes_retorno_do_server;

//Variaveis para conexao TCP
$seq=0;
$ack;
$window = $lim_bytes;


const log = " log_cTrans";
$arquivo = fopen(log, "w") or die("Unable to open file!");

while (1) {
    echo "Esperando um cliente...\n";  
    fwrite($arquivo," Espera por cliente aplicacao   "  );
    fwrite($arquivo, date('m/d/Y h:i:s a', time()) );	
    //Conectando com a camada superior
    while(($conn_superior = socket_accept($camada_superior)) != FALSE) {
        echo "Recebeu requisição\n";
        fwrite($arquivo,"\n Recebe requisicao de aplicacao    "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );

        //Lê-se o conteúdo do socket com um tamanho especificado e o escreve num arquivo
        //Perceba que há um limite de bytes a serem lidos
        echo "Servidor iniciado!\n";
        $sequencia_de_bytes = socket_read($conn_superior, $lim_bytes, PHP_BINARY_READ);
        fwrite($arquivo,"\n Recebe dados de aplicacao   "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );

        //Cria segmento com cabeçalho TCP
        $segmento = criaSegmentoTCP(getmypid(), 10006, $sequencia_de_bytes);

        //iniciando cliente que irá se comunicar com a camada inferior
        $port2 = 10001;
        //Abre-se e faz o teste do socket
        $camada_inferior = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        
        if ($camada_inferior === false) {
            echo "Deu ruim. Tá aqui o motivo: " . socket_strerror(socket_last_error()) . "\n";
        }
        else {
            echo "Parabéns! Socket criado.\n";
        }

        //Conectar-se ao servidor
        fwrite($arquivo,"\n Conecta com fisica   "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
        echo "Tentativa de conectar-se a $host pela porta $port2...";
        $conn_inferior = socket_connect($camada_inferior, $host, $port2);
        if ($conn_inferior === false) {
            echo "Deu ruim... Tenta entender o motivo: " . socket_strerror(socket_last_error($camada_inferior)) . "\n";
        } else {
            echo "Parabéns! Conectado a $host.\n";
        }

        //Escreve o conteúdo do arquivo no socket
        fwrite($arquivo,"\n Envia para fisica   "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
        socket_write($camada_inferior, $segmento, strlen($segmento));
        $sequencia_de_bytes_retorno_do_server = socket_read($camada_inferior, $lim_bytes, PHP_BINARY_READ);
        fwrite($arquivo,"\n Recebe da fisica   "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );

        $pdu = explode("\n",$sequencia_de_bytes_retorno_do_server);
        echo "--------------------------------------\nProcessando PDU da camada de transporte\n";
        exibePDU($pdu,'tcp');
        $resposta = implode("\n",array_slice($pdu, 5));

        socket_write($conn_superior, $resposta, strlen($resposta));
        fwrite($arquivo,"\n  Retorna para aplicacao   "  );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
        socket_close($conn_superior);
        socket_close($camada_inferior);
        break;
    }
}
    fwrite($arquivo,"\n Encerra conexoes   "  );
    fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
    //Encerra-se a conexão
    socket_close($conn_superior);
    echo "Servidor terminado...\n";
    fclose($arquivo);
?>
