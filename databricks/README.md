# ⚡ PulseFlat no Databricks

Este diretório contém os scripts, notebooks e instruções completas para executar os scrapers e pipelines de dados do **PulseFlat** dentro do ambiente **Databricks**, replicando a automação que hoje roda no GitHub Actions via **Databricks Git Folders (Repos)** e **Databricks Workflows (Jobs)**.

---

## 🎯 Arquitetura da Solução

```text
Databricks Workspace
│
├── Git Folders (Repos)
│   └── PulseFlat/ (clonado direto do GitHub)
│       ├── databricks/
│       │   ├── run_pulseflat_job.py          <-- Script Python para Databricks Job
│       │   └── notebooks/
│       │       ├── 01_orchestrator_notebook  <-- Notebook interativo com widgets
│       │       └── 02_delta_lake_exporter    <-- Ingestão para Delta Lake / Unity Catalog
│       ├── run_all.py                        <-- Orquestrador padrão
│       └── scrapers/                         <-- Todos os scrapers reutilizados 100%
│
└── Workflows (Jobs)
    └── Job Agendado (Quartz Cron / On-Demand)
        └── Task 1: Executar Scrapers (run_pulseflat_job.py)
        └── Task 2 (Opcional): Exportar para Delta Lake (02_delta_lake_exporter)
```

---

## 🚀 Passo a Passo de Configuração

### 1. Conectar o Repositório no Databricks (Git Folders)
1. No Databricks, acesse o menu lateral: **Workspace > Users > seu.email**.
2. Clique com o botão direito ou no menu de contexto e selecione **Create > Git Folder** (ou **Add > Repo**).
3. Insira a URL do repositório:
   `https://github.com/PulseDataLabs/PulseFlat.git`
4. Selecione o Provedor Git (ex: **GitHub**) e confirme. O projeto será sincronizado instantaneamente.

---

### 2. Configurar os Segredos / Credenciais
Você tem duas opções para disponibilizar as credenciais dos scrapers:

#### Opção A: Environment Variables no Job ou Cluster (Mais Fácil)
Ao configurar o Cluster ou o Job no Databricks:
1. Expanda **Advanced Options > Spark**.
2. No campo **Environment Variables**, adicione as chaves necessárias:
   ```bash
   ANBIMA_CLIENT_ID=seu_client_id
   ANBIMA_CLIENT_SECRET=seu_client_secret
   EULERPOOL_API_KEY=sua_chave_eulerpool
   FRED_API_KEY=sua_chave_fred
   ORACLE_DB_DSN=seu_dsn
   ORACLE_DB_USER=seu_usuario
   ORACLE_DB_PASSWORD=sua_senha
   ORACLE_DB_WALLET_PASSWORD=sua_wallet_senha
   ORACLE_DB_WALLET_BASE64=conteudo_base64_do_zip
   ```

#### Opção B: Databricks Secrets Scope (Mais Seguro)
Se tiver acesso ao Databricks CLI:
```bash
databricks secrets create-scope pulseflat
databricks secrets put-secret pulseflat ANBIMA_CLIENT_ID
databricks secrets put-secret pulseflat ANBIMA_CLIENT_SECRET
databricks secrets put-secret pulseflat FRED_API_KEY
```
*O script `run_pulseflat_job.py` e os notebooks já verificam o scope `pulseflat` automaticamente.*

---

### 3. Criando o Workflow Agendado (Databricks Job)
Para clonar a automação diária do GitHub Actions:

1. No menu lateral, acesse **Workflows** (ou **Jobs**) e clique em **Create Job**.
2. Dê um nome ao Job: `PulseFlat - Extracao Diaria`.
3. Configure a **Task 1**:
   - **Task name**: `run_scrapers`
   - **Type**: `Python script`
   - **Source**: `Git provider` (ou selecione direto de `Workspace / Repos / PulseFlat`)
   - **Path**: `databricks/run_pulseflat_job.py`
   - **Parameters** (opcional):
     ```text
     ["--parallel", "--max-workers", "8"]
     ```
     *(Você também pode filtrar por grupo: `["--group", "anbima", "--parallel"]`)*
   - **Cluster**:
     - Pode ser um **Serverless Job Compute** (se disponível na sua empresa) ou um cluster Single Node padrão (ex: `Standard_D4s_v5` ou similar).
   - **Dependent Libraries**:
     - Clique em **Add Dependent Library > PyPI** e instale as bibliotecas de `requirements.txt` (ex: `requests`, `beautifulsoup4`, `curl-cffi`, `openpyxl`, `bizdays`, `pandas`, `oracledb`).
4. Configure o **Schedule (Agendamento)**:
   - Clique em **Add trigger / Schedule**.
   - Defina os horários equivalentes ao GitHub Actions (ex: Horário de Brasília, dias úteis às 06h, 08h, 18h).
5. Clique em **Run now** para testar manualmente!

---

### 4. Execução Interativa via Notebook (Depuração)
Se quiser testar os scrapers manualmente ou rodar apenas um coletor específico:
1. Abra o notebook `databricks/notebooks/01_orchestrator_notebook`.
2. Conecte a um cluster ativo.
3. Use os seletores (widgets) no topo da tela para escolher o grupo (ex: `anbima`, `bcb`), quantidade de workers e modo de execução.
4. Clique em **Run All**.

---

### 5. Opcional: Ingestão Direta para Delta Lake (Unity Catalog)
Se você quiser que os dados coletados fiquem disponíveis para consultas SQL no Databricks:
- Adicione uma **Task 2** no seu Workflow dependente da Task 1 apontando para:
  `databricks/notebooks/02_delta_lake_exporter`
- Esse notebook lê todos os arquivos gerados em `./data` e atualiza tabelas Delta com suporte a versionamento ACID e Time Travel.
