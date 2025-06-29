# Reconhecimento de display de 7 segmentos com OpenCV

## Visão Geral

O projeto tem como objetivo permitir o reconhecimento e leitura de displays de segmentos com
visão computacional, utilizando a biblioteca OpenCV para receber e processar imagems de câmera obtidas
através de um microcontrolador.

## Utilização

- Extraia os arquivos do projeto (ou clone o repositório)
- Instale a biblioteca do OpenCV `pip install opencv-python`

Obs.: É necessário ter o Python instalado (min v. 3.6)

## Progresso

[06-06-2025] - Primeiros passos

Aplicação básica de leitura e exibição de imagem com OpenCV para fins de estudo e familiarização com
a biblioteca.

[24-06-2025] - Testes com filtros e binarização

Testes simples aplicados sobre uma imagem amostral de procedimentos de processamento de imagem como converção para escala de cinza, aplicação de filtro gaussiano, binarização de pixels e inversão de cores.

Realizada a primeira identificação e demarcação dos contornos mas os parâmetros de filtro ainda precisam ser ajustados.

[28-06-2025] - Identificação de displays

Os parâmetros para obtenção dos contornos foram ajustados para extrair com maior precisão a região de interesse do display dos
aparelhos.

Além disso, as rotinas de tratamento de imagem foram reorganizadas em funções para que possam ser reutilizadas ao longo do
projeto.

Os testes de extração de display com 7 imagens amostrais foi bem sucedido.