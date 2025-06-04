# Track&Go - Piattaforma per Spedizioni

Track&Go è una piattaforma web che permette agli utenti di gestire spedizioni e consegne in modo semplice ed efficiente.

## Funzionalità

- Registrazione e autenticazione utenti
- Dashboard personale
- Gestione spedizioni
- Sistema di tracking in tempo reale
- Recensioni e feedback

## Tecnologie Utilizzate

- Frontend: HTML, CSS, JavaScript
- Backend: Python con FastAPI
- Database: SQLite
- Autenticazione: JWT

## Installazione

1. Clona il repository:
```bash
git clone https://github.com/tuousername/track-and-go.git
cd track-and-go
```

2. Installa le dipendenze del backend:
```bash
cd progetto/backend
pip install -r requirements.txt
```

3. Avvia il server:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8081
```

4. Apri il browser e vai su:
```
http://localhost:8081
```

## Struttura del Progetto

```
progetto/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   └── routes_auth.py
└── frontend/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── css/
    └── js/
```

## Contribuire

Se vuoi contribuire al progetto, segui questi passaggi:

1. Fai un fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/nome-feature`)
3. Fai commit delle tue modifiche (`git commit -am 'Aggiungi feature'`)
4. Pusha il branch (`git push origin feature/nome-feature`)
5. Apri una Pull Request

## Licenza

Questo progetto è sotto licenza MIT. 