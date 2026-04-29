# 🌍 Eco-Awareness 2026 - Gestão de Ativistas

Projeto desenvolvido para o **Checkpoint 2 (CP2)** da disciplina de **DevOps & Storage** e **Database** na FIAP. A aplicação consiste em um sistema de gestão de participantes e distribuição de cashback para a iniciativa Eco-Awareness, utilizando containers Docker para orquestração.

## Integrantes
* **Matheus Nascimento Corregio** - RM 563765
* **Erick de Faria Gama** - RM 561951

##  Tecnologias e Conceitos Utilizados
* **Linguagem:** Python 3.10 (Flask)
* **Banco de Dados:** PostgreSQL 15
* **DevOps:** Docker & Docker Compose
* **Persistência:** Volumes Nomeados (Named Volumes)
* **Rede:** Docker Bridge Network
* **Database:** Script SQL (`init.sql`) para automação de schema e carga inicial (Seeders).

##  Arquitetura do Projeto

O projeto utiliza uma arquitetura de microserviços simplificada:
1. **App (Container Python):** Responsável pela lógica de negócio e interface web.
2. **DB (Container PostgreSQL):** Armazena dados de usuários, inscrições e auditoria.
3. **Volume (`cp2devops`):** Garante a persistência dos dados mesmo que os containers sejam removidos.



##  Como Executar o Projeto

Certifique-se de ter o Docker instalado e siga os passos:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/MATHEUSN06/CP_devops.git
   cd Cp2Devops

    docker-compose up --build -d

  Verificação: Indica que o acesso deve ser feito via localhost:5000.
