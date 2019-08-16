# Stažení dat ve formátu xml / Download xml

## Short description in English

Repository downloads xml records from NUSL (via OAI-PMH) and OpenAIRE (via public API) for master's thesis purpose. 

**thesis**  
Petra Černohlávková. (2019). Relationships of research outputs and projects: NUSL, Czech R&D Information System and OpenAIRE. Prague. Master thesis. Charles University. Supervisior Dvořák, Jan.

The details of this repository, which are given in the rest of this file, are described in the Czech language.

## Popis v češtině

Pro stahování z **NUŠL** byl použit prevzatý skript https://github.com/bloomonkey/oai-harvest, který přes OAI-PMH ukládá každý záznam do samostatného xml ve vybraném metadatovém formátu (v tomto případě využit marcxml).

Soubory uložené přímo v tomto repozitáři byly užity pro stahování záznamů z **OpenAIRE**.
 - openaire.py: Stahování přes OAI-PMH ze setu "openaire". Skript spouští několik procesů najednou a mezi nimi dělá přestávky, protože docházelo k překročení limitů OpenAIRE, který nestíhal odpovídat. Stahuje celý set s pomocí datestamps.
 - openaire_api.py: Stahování přes veřejné API záznamů, které odkazují alespoň na jeden projekt a byly vydány v rozmezí 2014-2018 včetně. Stahování je rozloženo po měsících (kromě prvního dne v roce) z důvodu limitu v API - 10tis. záznamů na dotaz. První den v roce přesahoval limitu pro stažení, proto byl stažen extra za použití skriptu pull.py 
	
