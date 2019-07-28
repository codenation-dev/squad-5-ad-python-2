# Squad 5 AD Python - Gestão de comissões Televendas

API que implementa os requisitos do Projeto Final da aceleração AD Python, da Codenation.

## Requisitos

Recomenda-se a utilização de um ambiente virtual e do gerenciador de pacotes pip.

```bash
pip3 install virtualenv
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

## Comissões

#### Cadastrar Comissão:

`POST /comissions`: Realiza o cadastro da comissão.

#### Body example:

```
{
	"lower_percentage": 5,
	"min_value": 10000
	"upper_percentage": 10,
}
```
#### Retorna as Comissões:

`GET /comissions`: Retorna todas as comissões cadastradas.

#### Retorna Comissão:

`GET /comissions/id`: Retorna uma comissão cadastrada.

#### Alterar Comissão:

`PUT /comissions/id`: Altera uma comissão cadastrada.

#### Retorna Comissão:

`DELETE /comissions/id`: Remove uma comissão cadastrada.
