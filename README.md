# Bot Borgo Altrove
Questi sono i file utilizzati per implementare il Bot del [server discord Borgo Altrove](<https://discord.gg/borgo-altrove-8090556690753126>).

Nella cartella 📁`bot` vi sono:
* `main.py`, il file main;
* `config.py`, un file da buttare che non serve a nulla;
Nella cartella 📁`cogs` invece vi sono tutte le funzioni del bot che sono:
* `basic_commands.py`, funzioni base come:
  * Clear (pulisce i messaggi)
  * Test (invia i messaggi e i file con il bot)
  * Join role (per il ruolo @Disperso e @BOT)
  * Shutdown (solo l'owner può usarlo per spegnere il bot da Discord)
* `join_to_create.py`, funzione che genera nuovi canali vocali per:
  * Sale Master
  * Sale Regionali
  * Sale Spam
* `sessione.py`, funzione per la proposta, approvazione e archiviazione delle sessioni di gioco dei master;
* `token.py`, ANCORA IN FASE DI IMPEMENTAZIONE ⚠️;
