# 💳 Monitoramento de gastos por cartão

## Sobre o projeto

Esse projeto surgiu de um problema que eu tenho no dia a dia.

Eu e minha namorada usamos cartões ligados à mesma fatura para concentrar os gastos e juntar mais pontos. O problema é que, no aplicativo do Santander, eu consigo ver qual cartão fez cada compra, mas não consigo ver de forma rápida quanto cada cartão gastou no total.

No final, sempre acaba naquele processo manual de olhar compra por compra, separar o que é meu e o que é dela e depois somar tudo.

A ideia desse projeto é justamente tirar essa parte manual do caminho.

## 🎯 Objetivo

O objetivo é criar um sistema que consulte as transações da conta, identifique qual cartão foi usado em cada compra e vá somando automaticamente os valores de cada cartão.

A ideia é ter uma visualização simples, mais ou menos assim:

```text
Fatura atual

Meu cartão
R$ 1.420,50

Cartão da minha namorada
R$ 863,70

Total da fatura
R$ 2.284,20
```

Assim, em vez de precisar fazer as contas manualmente toda vez, o sistema já mostra quanto cada cartão gastou.

## ⚙️ Como pretendo fazer

Inicialmente, pretendo usar:

### Backend

* Python
* Flask

### Frontend

* HTML
* CSS
* JavaScript

### Integração com o banco

* Pluggy API

A Pluggy será usada para facilitar a conexão com o banco e a obtenção das transações através do Open Finance, evitando que eu precise implementar toda a parte mais complexa de conexão e autenticação bancária do zero.

## 🚧 Status

O projeto ainda está no começo.

A stack, a estrutura e até algumas funcionalidades podem mudar conforme eu for desenvolvendo, estudando a API e entendendo melhor as limitações da integração com o banco.
