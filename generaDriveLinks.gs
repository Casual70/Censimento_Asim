/**
 * generaDriveLinks v2
 *
 * Struttura Drive attesa:
 *   root (Censimento)
 *     └─ 1_San Giustino_comune    (depth 1 = comune)
 *         └─ 5_SelciLama          (depth 2 = zona)
 *             └─ Schedario3       (depth 3+ = schedario, ignorato per la chiave)
 *                 └─ Scheda fabbricato-140.doc   → chiave: "SelciLama/Scheda fabbricato-140"
 *
 * Le chiavi prodotte sono di due tipi:
 *   1. "zona/nomeFile"   → per Schede fabbricato (evita duplicati tra zone)
 *   2. "nomeFile"        → per tutti gli altri file (foto 100_XXXX ecc., univoci per natura)
 *
 * La normalizzazione del nome zona:
 *   "5_SelciLama"  → "SelciLama"   (rimuove prefisso numerico N_)
 *   "PIANDASSINO"  → "PIANDASSINO" (invariato)
 *   "1_San Giustino_comune" NON diventa zona (depth 1)
 */

var ROOT_ID = "1rrCwYsK27d-LqNwzWZ19mH_VhKT8-YBY"; // <-- ID cartella root Censimento

function generaDriveLinks() {
  var map = {};
  var errori = [];
  var totaleFile = 0;

  // Normalizza il nome cartella zona rimuovendo prefisso "N_" iniziale
  function normalizzaZona(nome) {
    return nome.replace(/^\d+[_\s]+/, "").trim();
  }

  /**
   * @param {string} folderId  ID cartella Google Drive
   * @param {number} depth     0=root, 1=comune, 2=zona, 3+=schedario
   * @param {string} zona      Nome zona normalizzato (valorizzato a depth >= 2)
   * @param {string} path      Percorso testuale (solo per log)
   */
  function scanFolder(folderId, depth, zona, path) {
    try {
      var folder = DriveApp.getFolderById(folderId);
      Logger.log("Scansione [depth=" + depth + "]: " + path);

      // A depth 2 siamo nella cartella zona: la impostiamo
      var zonaCorrente = zona;
      if (depth === 2) {
        zonaCorrente = normalizzaZona(folder.getName());
      }

      // Scansiona i file nella cartella corrente
      var files = folder.getFiles();
      var count = 0;
      while (files.hasNext()) {
        var f = files.next();
        var nomeBase = f.getName().replace(/\.[^.]+$/, ""); // rimuove estensione
        var id = f.getId();

        if (nomeBase.indexOf("Scheda fabbricato") === 0 && zonaCorrente) {
          // Chiave con zona (univoca)
          map[zonaCorrente + "/" + nomeBase] = id;
        } else {
          // Chiave semplice (foto 100_XXXX, altri documenti)
          map[nomeBase] = id;
        }
        count++;
        totaleFile++;
      }
      Logger.log("  → " + count + " file");

      // Ricorsione nelle sottocartelle
      var subs = folder.getFolders();
      while (subs.hasNext()) {
        var sub = subs.next();
        scanFolder(sub.getId(), depth + 1, zonaCorrente, path + "/" + sub.getName());
      }

    } catch (e) {
      errori.push("ERRORE in " + path + ": " + e.message);
      Logger.log("ERRORE in " + path + ": " + e.message);
    }
  }

  scanFolder(ROOT_ID, 0, "", "root");

  Logger.log("=== TOTALE FILE: " + totaleFile + " ===");
  if (errori.length > 0) {
    Logger.log("ERRORI (" + errori.length + "): " + errori.join(" | "));
  }

  // Salva il file JSON nel Drive
  try {
    var json = JSON.stringify(map, null, 2);
    var blob = Utilities.newBlob(json, "application/json", "drive_links.json");
    var file = DriveApp.createFile(blob);
    Logger.log("File creato con ID: " + file.getId());
    Logger.log("URL: " + file.getUrl());
  } catch (e) {
    Logger.log("ERRORE creazione file: " + e.message);
  }
}
