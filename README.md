# ✈️ FlyTrack

Aplicação **Django** para busca de passagens, histórico e contato, com **API (Django REST Framework)** e páginas estáticas customizadas.

> **Stack:** Python 3.13 · Django 5 · Django REST Framework · HTML · CSS · JavaScript

---

## ✨ Funcionalidades

- 🏠 Página inicial com busca de passagens  
- 📊 Página de **Resultados** com dados simulados  
- 🕓 Página de **Histórico de viagens**  
- 💌 Página de **Contato** com envio de e-mail via Gmail  
- 🔐 Login e Cadastro personalizados (com CPF e data de nascimento)  
- 🔌 API REST para busca de voos (endpoint `/api/busca/`)  

---

## 🏗️ Estrutura do Projeto

```
flytrack-project/
├─ flytrack/                      # Configurações do projeto Django
│  ├─ settings.py                 # inclui DRF, templates, static, e-mail Gmail
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
├─ core/                          # App principal
│  ├─ admin.py
│  ├─ api.py                      # Endpoint REST: busca_voos (IsAuthenticated)
│  ├─ apps.py
│  ├─ forms.py                    # ContactForm, SignupForm (email, birth_date, cpf)
│  ├─ models.py                   # (vazio no MVP)
│  ├─ urls.py                     # home, resultados, historico, contato
│  ├─ views.py                    # páginas + contato (envia e-mail) + signup
│  ├─ static/
│  │  └─ core/
│  │     ├─ img/                  # logos e ícones
│  │     └─ css/js (se houver)
│  └─ templates/
│     ├─ home.html
│     ├─ resultados.html
│     ├─ historico.html
│     ├─ contato.html
│     └─ registration/
│        ├─ login.html
│        └─ signup.html
├─ static/                        # Arquivos estáticos adicionais
├─ manage.py
├─ requirements.txt
├─ .env.example
└─ .gitignore
```

---

## 🧩 Apps e Responsabilidades

- **core**: páginas públicas (Home, Resultados, Histórico, Contato), formulários e fluxo principal.  
- **api**: endpoints REST com autenticação.  
- *(outros apps podem ser adicionados futuramente, ex. `accounts`, `booking` etc.)*

---

## 🧠 Forms

- **SignupForm:** herda `UserCreationForm` e adiciona campos extras:
  - `email`
  - `birth_date`
  - `cpf` (com validação numérica e placeholder)
- **ContactForm:** campos `nome`, `email`, `mensagem` e `concordo` (opt-in).  
- Validações customizadas implementadas em `forms.py`.

---

## 🔌 API (Django REST Framework)

**Endpoint:** `/api/busca/`  
**Permissão:** `IsAuthenticated`  
**Parâmetros:** `origem`, `destino`, `data`, `pax` (GET ou POST)  

### Exemplo de Resposta
```json
{
  "ok": true,
  "recomendado": {
    "preco": 5340,
    "preco_fmt": "R$ 5.340",
    "descricao": "Tarifa recomendada com 1 mala despachada"
  },
  "mais_barato": {
    "preco": 4900,
    "preco_fmt": "R$ 4.900"
  },
  "parametros": {
    "origem": "São Paulo",
    "destino": "Recife",
    "data": "2025-12-10",
    "pax": 1
  }
}
```

### Teste rápido
```bash
curl -H "Cookie: sessionid=SEU_SESSION_ID" "http://127.0.0.1:8000/api/busca/?origem=São Paulo&destino=Recife&data=2025-12-10&pax=1"
```

---

## ⚙️ Como Rodar Localmente

### 1️⃣ Criar ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar variáveis de ambiente

Crie um arquivo `.env` (baseie-se em `.env.example`) e **não** suba no GitHub.

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
EMAIL_HOST_USER=flytrackcontato@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
```

> ⚠️ Use **senha de app** do Gmail (Configurações → Segurança → Senhas de app).

### 4️⃣ Criar banco e superusuário
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5️⃣ Rodar servidor
```bash
python manage.py runserver
```

Abra no navegador: http://127.0.0.1:8000/

---

## 📬 Envio de E-mail (Contato)

O `views.contato`:
- valida campos do formulário,
- envia e-mail para `CONTACT_TO_EMAIL`,
- envia cópia de confirmação para o remetente.

**Configuração usada:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
CONTACT_TO_EMAIL = os.getenv('CONTACT_TO_EMAIL', EMAIL_HOST_USER)
```

---

## 🔐 Autenticação

- Login e logout via templates em `core/templates/registration/`
- Cadastro customizado (`signup.html`)
- `LOGIN_REDIRECT_URL = 'core:home'`
- `LOGOUT_REDIRECT_URL = 'core:home'`
- Em breve: **login com Google (OAuth2)**

---

## 🚀 Deploy (Render / Railway)

1. Crie conta em https://render.com ou https://railway.app  
2. Conecte o repositório GitHub (`flytrack-project`)
3. Defina variáveis de ambiente:
   ```
   DEBUG=False
   SECRET_KEY=chave-secreta
   EMAIL_HOST_USER=flytrackcontato@gmail.com
   EMAIL_HOST_PASSWORD=senha-de-app
   ```
4. Comando de start:
   ```
   python manage.py migrate && gunicorn flytrack.wsgi
   ```
5. Configure domínio ou subdomínio conforme a plataforma.

---

## 🧪 Testes

Rodar testes automatizados:
```bash
python manage.py test
```
ou, se preferir pytest:
```bash
pytest
```

---

## 📸 Screenshots (Exemplos)

| Página | Descrição |
|--------|------------|
| 🏠 **Home** | Busca de passagens e botões de ação |
| 📈 **Resultados** | Exibição de voos simulados |
| 🕓 **Histórico** | Viagens compradas ou em andamento |
| 💌 **Contato** | Formulário com envio de e-mail |
| 🔐 **Login / Cadastro** | Autenticação personalizada |

*(Adicione imagens na pasta `/static/core/img/` e insira aqui se quiser mostrar prints.)*

---

## 📄 Licença e Autoria

Projeto desenvolvido por **Maria Eduarda Sousa Silva**  
🎓 Eng. Mecatrônica — Escola Politécnica da USP  

📧 Contato: flytrackcontato@gmail.com  
🌐 GitHub: https://github.com/SEU_USUARIO/flytrack-project

---

🛫 *FlyTrack — encontre e acompanhe suas viagens de forma simples e acessível!*
