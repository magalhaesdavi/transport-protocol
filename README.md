# Protocolo de comunicação confiável baseado no UDP

## Descrição

Nesse projeto desenvolvemos um protocolo de comunicação confiável baseado no UDP. Para isso adicionamos algumas funcionalidades extras, algumas até estão presentes no TCP.

## Funcionalidades implementadas

Implemented algorithms:

- Fluxo Full-Duplex;
- Go-Back-N;
- Controle de fluxo;
- Controle de congestionamento (inspirado no RED);
- Fast Retransmit;

## Experimentos

Para avaliar a performance do protocolo e observar seu comportamento, realizamos 10 execuções sem perdas de pacotes e 10 execuções simulando perdas aleatórias. Os resultados obtidos são apresentados nos gráficos em ```/results```. Nos parâmetros de linha de comando utilizamos uma probabilidade de perda de 5% (nos testes com perda) e tamanho de buffer de 1500. Já como parâmetro interno, usamos tempo de timeout de 0.52 segundo. Chegamos a esse valor tendo como base o RTT médio e o RTT máximo.

## Como rodar

Para rodar o código basta rodar primeiro ```server.py```, da seguinte forma:

```
python server.py [-h] [-p PORT] [-l LOSS_PROBABILITY] [-s BUFFER_SIZE]
```

O campo ```[-h]``` não é mandatório, mas pode ser utilizado para obter uma descrição do script e dos campos e da forma de uso. Para isso, basta rodar:

```
python server.py -h
```

Ou

```
python server.py --help
```

Uma vez que o server está rodando basta rodar o cliente. De forma semelhante:

```
python client.py [-h] [-p PORT] [-f FILE_PATH]
```

Assim como na execução do server, pode-se utilizar o campo ```[-h]``` para obter uma ajuda para executar.

## Nota

A aplicação foi feita para enviar pacotes de 512 bytes por linha do arquivo. Até o momento atual esse parâmetro não é customizável. Caso o arquivo de teste tenha mais de 512 bytes por linha, ocorrerá erros.
