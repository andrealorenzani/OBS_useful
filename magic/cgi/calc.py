#!/usr/bin/env python3

tarocs = {
    'Il Mago': ["Il mago è una figura che rappresenta attività, infatti il mago è colui che è artefice della propria fortuna, che è intraprendente, che agisce, e che ottiene dei risultati. E’ una carta indubbiamente positiva, infatti rappresenta colui che ha capacità ed intelligenza, le usa, e grazie ai suoi meriti raggiunge dei risultati. Rappresenta: azione, capacità, intraprendenza, merito, risultati.","ROVESCIATO: Si esaltano tutti gli aspetti negativi dell’agire; ad esempio può significare: agire per il male, troppa fretta e agire senza riflettere, arrivismo, sfiducia nelle proprie capacità che invece ci sono, agire male, ossessione per i risultati materiali trascurando i veri valori."],
    'La Papessa': ["La carta della papessa rappresenta serenità, conoscenza, fede e fedeltà, valori e rettitudine morale. Spesso può riferirsi ad una figura femminile, affidabile e sincera. E’ una carta indubbiamente positiva.", "ROVESCIATA: Risultare saccenti e presuntuosi, utilizzare informazioni a fini discutibili, insidia da parte di una donna molto intelligente"],
    'L\'imperatrice': ["L’imperatrice indica stabilità, forza, e protezione. Questi concetti sono ben simboleggiati rispettivamente da: trono, scettro, e scudo. L’imperatrice rappresenta forza interiore, forza di volontà, governo delle cose. Può rappresentare una figura esterna forte che ci aiuta in una determinata situazione, un appoggio su cui contare, un punto di stabilità e forza a nostro favore.", "ROVESCIATA: Rigidità morale e nell’agire, eccesso di misure drastiche, eccessivo istinto protettivo nei confronti di un’altra persona, fatica nel mantenere lo status attuale."],
    'L\'imperatore': ["L’imperatore dei tarocchi simboleggia forza, autorità, sicurezza, potere, ricchezza, carisma, virilità, consapevolezza, fermezza. L’imperatore è il punto massimo del potere terreno, ed al tempo stesso è una figura saggia ed intelligente, spesso anche giusta.", "ROVESCIATA: Rigidità, prepotenza, severità, drasticità, uso eccessivo di forza"],
    'Il Papa': ["Il papa simboleggia buoni consigli disinteressati, avallo altrui, successo giusto, persona fedele e leale su cui contare. Il papa può rappresentare una figura esterna, un mentore, una figura che rispettiamo e da cui dovremmo prendere il buon esempio.", "ROVESCIATA: Cercare troppo l’approvazione altrui, non prendere delle decisioni originali e di testa propria, schierarsi sempre dove tira il vento senza avere la forza di sostenere le nostre vere posizioni. In alcuni casi può significare anche eccessivo moralismo."],
    'Gli Amanti': ["Il simbolismo della carta è ovvio: l’amore. Altri significati della carta degli amanti possono essere: desiderio di una relazione d’amore vera, attrazione fisica che si trasforma in attrazione spirituale, tentazioni positive.", "ROVESCIATA: Troppo amore che risulta oppressivo, unione non positiva, separazione e rottura, tentazioni negative, fino ad arrivare all’infedeltà."],
    'Il Carro': ["Il carro preannuncia il successo in una ben determinata faccenda. Il successo sarà netto e potente, e trasmetterà piena soddisfazione e gloria.", "ROVESCIATA: Il successo è un’arma a doppio taglio, come l’auriga deve saper condurre il carro trainato da più cavalli (forze contrapposte), così il successo va gestito e guidato. Chi non sa condurre il successo, oltre a non trarne soddisfazione, rischia effetti negativi. Il carro rovesciato può simboleggiare anche eccessivo vantarsi con gli altri dei propri successi, generando antipatie o gelosie."],
    'La Giustizia': ["La giustizia rappresenta equità e rettitudine, ma anche resa dei conti, verifica, prova superata, virtù", "ROVESCIATA: Rottura dell’equilibrio, ingiustizia, eccessiva severità, valutazione sfavorevole"],
    'L\'Eremita': ["L’eremita è il simbolo della saggezza. Il riferimento simbolico alla saggezza è sia nella lanterna che tiene in mano l’eremita – che illumina la realtà dei fatti – sia nella figura dell’eremita stesso. La saggezza dell’eremita dei tarocchi è anche prudenza, ad esempio nel valutare dove si sta andando e cosa si sta facendo. Significa anche riflessione su se stessi, e sulle situazioni indicate dalle carte vicine. Desiderio di scoprire la verità, ricerca della verità.", "ROVESCIATA: Eccesso di prudenza, eccesso di isolamento dagli altri, eccessiva riflessione e scarso agire, imprudenza, cattivo orientamento su ciò che si sta facendo. Non avere ancora capito come in realtà stanno le cose, e di chi potersi fidare."],
    'La Fortuna': ["Questa carta ricorda la precarietà di situazioni destinate ad evolvere e mutare. Il punto cruciale è che le cose possono evolvere per il meglio, ma anche verso condizioni peggiori. La carta rimanda a condizioni di equilibrio precario. In generale la fortuna è una carta più positiva che negativa, infatti il cambiamento è sempre un’opportunità fruttuosa per chi la sa cogliere.", "ROVESCIATA: Mutamenti della situazione per il peggio, sorte avversa. Mancanza di prontezza nello sfruttare il cambiamento come opportunità."],
    'La Forza': ["La carta simboleggia la forza bruta (il leone) vinta dall’intelligenza. Richiama quindi ad un uso della propria intelligenza per risolvere le situazioni, non ricorrendo invece a misure drastiche, a soluzioni affrettate, o alla forza. Il tarocco della forza indica anche successo nel risolvere le situazioni grazie alla propria forza interiore, coraggio, ed astuzia.", "ROVESCIATA: Cattivi risultati dovuti a uso eccessivo della forza o a reazioni impulsive, senza riflettere. Mancanza di tempo per riflettere – vinti degli eventi – e conseguenti azioni sbagliate."],
    'L\'Appeso': ["Ad una prima analisi questa carta sembra trasmettere una situazione negativa di immobilità, ma ad uno sguardo più attento si capisce che è invece la situazione di chi non si profonde in sforzi che sarebbero inutili, ed attende il mutamento degli eventi nella consapevolezza che la situazione sfavorevole è solo temporanea. La carta simboleggia un sacrificio, una condizione sfavorevole da sopportare, per raggiungere un obiettivo. Sono necessari degli sforzi importanti, delle rinunce, sarà necessario superare delle prove difficili. E’ necessario fare buon viso a cattiva sorte, in quanto reagendo in modo istintivo e sbagliato questa situazione temporaneamente difficile rischia di trasformarsi in condizione permanente. Bisogna sacrificarsi, essere lucidi nelle condizioni di difficoltà, e saper sopportare. Sacrificio temporaneo, per poter poi migliorare la propria situazione.", "ROVESCIATA: Cattiva reazione a condizioni di difficoltà temporanea. Fatiche inutili per modificare una situazione per cui invece c’è da fare solo una cosa: attendere."],
    'La Morte': ["La morte simboleggia una fase di quello che è il ciclo della vita, una fase traumatica ma che precede una nuova nascita. Una figura così spaventosa non significa quindi in modo scontato che la morte sia una carta portatrice di sventure, infatti il suo significato è principalmente quello di cambiamento, di chiusura di un ciclo e di conseguente rinnovamento. La morte significa fine della situazione corrente, magari in modo traumatico, e nuova situazione che ne consegue. La morte può riguardare anche la fine di un ciclo negativo. Ovviamente questa carta, associata ad altre carte sfavorevoli, contribuisce a delineare un quadro non positivo.", "ROVESCIATA: Cattivo epilogo di una situazione, sventure"],
    'La Temperanza': ["La carta della temperanza invita alla moderazione. Come in passato il vino veniva temperato con l’acqua, così vanno evitati gli eccessi nella vita. Si deve ricercare la moderazione, l’autocontrollo, ci si deve rilassare. Oppure anche: si sta prendendo una situazione con il giusto equilibrio, si deve mantenere il giusto equilibrio.", "ROVESCIATA: Mancanza di moderazione, eccessi. Non si sta prendendo la situazione con il giusto equilibrio, si sta sbagliando atteggiamento."],
    'Il Diavolo': ["La carta del diavolo è la carta più negativa dei tarocchi. Può simboleggiare il male o un pericolo. Anche immoralità, degenerazione, cattiverie, e vizi vari sono associabili a questa carta.", "ROVESCIATA: Il male puro. In alcuni rari casi può riferire a passione sfrenata. In altri casi può riferire alla fine di una situazione di pericolo."],
    'La Torre': ["La torre dei tarocchi rappresenta la superbia punita. E’ una carta sfavorevole, che preannuncia un fallimento, dovuto proprio alla nostra presunzione e superbia. Affronteremo una dura punizione dovuta alla nostra mancanza di umiltà. Abbiamo attirato invidie e inimicizie, dovute al nostro successo ostentato o alla nostra ambizione, e qualcuno farà in modo che ciò si ritorca contro di noi. La carta della torre può essere anche solo un ammonimento: attenzione a non ostentare troppo il proprio successo, a non essere troppo presuntuosi o superbi con gli altri, altrimenti ciò porterà ad una dura punizione.", "ROVESCIATA: Eccesso forte di superbia, ostentazione, o ambizione. Inimicizia forte di qualcuno che proverà in tutti i modi a metterci i bastoni tra le ruote. Perdite."],
    'Le Stelle': ["La carta delle stelle è senza dubbio positiva. Bisogna essere ottimisti perché gli astri sono con noi e stanno emanando i loro benefici influssi. Abbiamo il favore del cielo e le stelle ci rischiarano il cammino. Fertilità di idee e circostanze favorevoli. Questa carta ha un benefico influsso sulle carte circostanti e sulle situazioni a cui queste si riferiscono. Le stelle non indicano necessariamente il successo materiale in una specifica azione, ci dicono piuttosto che troveremo la gioia, il buon umore, che saremo appagati e felici. Tutto è predisposto per il meglio per la nostra felicità.", "ROVESCIATA: Situazione favorevole che non è stata colta, occasioni non sfruttate. Pessimismo eccessivo quando invece la situazione non è così grave."],
    'La Luna': ["L’iconografia della carta rimanda chiaramente al suo significato: c’è un’atmosfera sinistra e oscura che è portatrice di inganno. Se non si presta la dovuta attenzione si cadrà in errore, le circostanze esterne sono sfavorevoli, tentatrici ed ingannevoli. E’ possibile tuttavia passarne indenni, ma non senza attenzione e capacità. La luce lunare nasconde le insidie e i pericoli di un terreno accidentato, non sarà semplice orientarsi con successo e non cadere in errore. Qualcuno vi sta ingannando o sta parlando alle vostre spalle. Circostanze sfavorevoli, insidie nascoste, inganni, persone ingannevoli, nemici travestiti da amici.", "ROVESCIATA: Si sta subendo un inganno. Insidie molto pesanti a breve termine."],
    'Il Sole': ["Torna la luce del sole ad illuminarci il cammino e a cancellare le insidie dell’oscurità. Ora la via è più chiara e senza pericoli. Ci aspetta un periodo di serenità e buon umore. Dopo periodi difficili (l’oscurità), tutto volge per il meglio. Grande appagamento personale poiché il momento positivo viene dopo momenti meno fortunati.", "ROVESCIATA: Una situazione negativa ritarda a volgere al meglio. Si fatica nel trarre gioia e spensieratezza dalle situazioni che sono positive."],
    'L\'Angelo': ["L’angelo è una carta di rinnovamento, evidentemente una situazione va mutando. La situazione muta poiché si è arrivati al momento della resa dei conti. Non si può più tergiversare, posticipare, ma si deve affrontare la resa dei conti e le relative conseguenze. L’angelo può rappresentare anche la necessità di liberarsi da ossessioni materiali e riscoprire i veri valori che fanno realmente la felicità. Nodi che vengono al pettine, chiusura di una situazione, giudizio finale.", "ROVESCIATA: Resa dei conti sfavorevole. Punizione subita. Operato scorretto che viene scoperto e sanzionato. Viene scoperto che si è tenuta una condotta biasimabile."],
    'Il Mondo': ["Il mondo è una della carte più positive dei tarocchi; rappresenta purezza ed armonia, la creazione e lo scibile umano. Gli obiettivi saranno raggiunti, si avrà successo in ciò che si sta facendo. Si sarà prolifici. Verrà raggiunta la serenità interiore. Impareremo a sentirci appagati della nostra situazione e a godere di ciò che abbiamo.", "ROVESCIATA: Avremo successo ma non agendo in modo corretto. Verranno tenuti comportamenti sbagliati, ma nonostante questo tutto andrà bene."],
    'Il Matto': ["La carta del matto può avere un duplice significato: sia positivo che negativo. Il significato positivo è l’incitazione a lasciarci andare, a vivere liberamente. Liberiamoci dell’eccesso di logica, di razionalità, e facciamo ciò che più ci piace. Viviamo quindi “come dei matti”, rompiamo le regole che altri hanno imposto e facciamo ciò che ci fa sentire meglio, anche se contrasta col senso comune; l’importante è che per noi sia positivo ed appagante. O anche: estro e genialità (spesso incompresa). L’interpretazione negativa della carta, invece, riguarda azioni sconsiderate, compiute senza logica alcuna, \“da matto\”. Persona che ha agito in modo irresponsabile, che ha bisogno di tornare sui suoi passi. O anche: poco rispetto per se stessi; lasciarsi condurre dagli eventi in modo passivo.", "ROVESCIATA: Irresponsabilità, irrazionalità, ossessione, immaturità, mancanza di logica, agire d’istinto totalmente sbagliato, mancanza di valori guida."],
    'Re di Bastoni': ["Potere acquisito col duro lavoro. Uomo di animo buono, tollerante nonostante la propria forza. Uomo di successo, maturo ed intelligente, sicuro di sé al punto da non dover ostentare nulla.", "ROVESCIATA: Uomo severo. Troppa rigidità."],
    'Regina di Bastoni': ["Donna eccezionale, carismatica e di forte influsso. Donna fidata e tollerante, di buoni valori, altruista, di successo. Persona pronta ad aiutare e sensibile. Probabili aiuti inaspettati, supporto tangibile dall’esterno.", "ROVESCIATA: Persona con secondi fini, donna molto intelligente e pericolosa."],
    'Cavaliere di Bastoni': ["Azione forte di successo. Persona protettiva nei nostri confronti, pronta a prendere le nostre difese concretamente. Successo meritato.", "ROVESCIATA: Prepotenza, minaccia, contrasti, litigi."],
    'Fante di Bastoni': ["Impeto giovanile, colpo di testa ma positivo. Persona più giovane di noi e positivamente impetuosa (sia uomo che donna).", "ROVESCIATA: Brutte notizie. Errori d’inesperienza. Giovane ribelle."],
    '10 di Bastoni': ["Massimo della forza per portare a compimento le nostre azioni. Energia e dinamismo.", "ROVESCIATA: Eccesso di zelo, troppa irrequietezza che genera fastidio negli altri."],
    '9 di Bastoni': ["Azione perfettamente eseguita (i bastoni sono il seme dell’azione, e il nove è il numero più che perfetto, poiché è il risultato della moltiplicazione del 3, numero perfetto, per se stesso). Ottima idea.", "ROVESCIATA: Invidie o gelosie nei nostri confronti."],
    '8 di Bastoni': ["Carta dell’equilibro. Nonostante le azioni la situazione rimane ferma. La situazione è ben predisposta e tende a rimanere tale.", "ROVESCIATA: Situazione in blocco."],
    '7 di Bastoni': ["Sblocco di una situazione, sorprese positive inattese.", "ROVESCIATA: Eccesso nei vizi, o anche nelle virtù."],
    '6 di Bastoni': ["Situazione generale positiva per il nostro agire, condizioni esterne favorevoli, buone basi per il futuro.", "ROVESCIATA: Certezze in pericolo, status e sicurezze in pericolo."],
    '5 di Bastoni': ["Instabilità, rottura dell’equilibrio, dinamismo.", "ROVESCIATA: Troppa impetuosità, disputa, desiderio eccessivo."],
    '4 di Bastoni': ["Simmetria ed armonia nella nostra vita. Stabilità ritrovata, rilassatezza. Piccoli successi appaganti.", "ROVESCIATA: Mancanza di tranquillità immotivata."],
    '3 di Bastoni': ["Azione perfetta. Protezione nei nostri confronti. I tre bastoni formano una sorta di scudo a nostra protezione.", "ROVESCIATA: Bisogno di protezione, di supporto."],
    '2 di Bastoni': ["Unione positiva e salda. Forte collaborazione ad un progetto, alleanze. Persona su cui poter contare, di supporto.", "ROVESCIATA: Contrasti di coppia. Scontri con persone a noi vicine. Legami troppo stretti, soffocanti."],
    'Asso di Bastoni': ["Creatività, iniziativa, potenza, forza, intraprendenza. Creazione di cose nuove, produzione di idee nuove, azione portatrice di frutti.", "ROVESCIATA: Agire sbagliato, obiettivi non raggiunti, decadenza."],
    'Re di Coppe': ["Uomo carismatico, uomo che ci vuole bene in modo disinteressato e che ci guiderà sempre per il meglio", "ROVESCIATA: Uomo troppo severo con noi, uomo che ci tutela troppo"],
    'Regina di Coppe': ["Donna con istinto materno molto sviluppato, donna molto intelligente e capace. Donna che ci vuole bene in modo disinteressato e che ci consiglierà sempre per il meglio. Donna che si sacrifica per noi. Donna con grande influenza su di noi.", "ROVESCIATA: Figura femminile oppressiva, donna rigida e limitante nei nostri confronti."],
    'Cavaliere di Coppe': ["Vitalità in amore, novità e rinascita dell’amore. Riscoperta di sentimenti sopiti, desiderio di conoscere persone nuove e dinamiche.", "ROVESCIATA: Gelosie, amore tormentato, tradimento."],
    'Fante di Coppe': ["Attrazione e fantasie persistenti nei confronti di una persona molto attraente che ci ha colpito. Giovane attraente.", "ROVESCIATA: Persona senza scrupoli, inganno in amore, infedeltà, reali intenzioni nascoste."],
    '10  di Coppe': ["Massima serenità d’animo e disposizione ad amare. Grande ricchezza interiore che finalmente genererà risultati e sarà apprezzata dagli altri... da alcuni in modo molto particolare. Siamo finalmente attraenti per la nostra ricchezza interiore.", "ROVESCIATA: Grandissime potenzialità non sfruttate a causa unicamente del fatto che non crediamo sufficientemente in noi stessi e nel nostro fascino sugli altri."],
    '9 di Coppe': ["Momento di massima soddisfazione personale, sia affettiva che lavorativa. Buone nuove occasioni da cogliere. Non potrebbe andare meglio.", "ROVESCIATA: Errori nella gestione di una situazione che sarebbe pienamente favorevole. Nonostante i discreti risultati, si poteva raccogliere molto di più."],
    '8 di Coppe': ["Occasione per riflettere. Buone basi per creare qualcosa insieme ad un’altra persona.", "ROVESCIATA: Rischio che si sgretoli una situazione che sembrava ormai consolidata."],
    '7 di Coppe': ["Ciò che sembrava ormai non arrivare più finalmente è in arrivo. Periodo magico.", "ROVESCIATA: Quasi una maledizione non ci fa mai trovare la felicità."],
    '6 di Coppe': ["Un passato fatto di serenità potrebbe tornare. Bei ricordi ci tornano alla mente, ci fanno riflettere sulla nostra situazione, e sono di stimolo per il nostro futuro a breve termine.", "ROVESCIATA: Ricordi dolorosi. Non riuscire ad eliminare dai nostri pensieri un ricordo doloroso."],
    '5 di Coppe': ["Buone nuove. Occasioni nuove da cogliere, però rapidamente, perché l’opportunità non durerà a lungo.", "ROVESCIATA: Occasione non sfruttata, perdita di opportunità importanti che avrebbero portato finalmente a una grande soddisfazione personale."],
    '4 di Coppe': ["Equilibrio negli affetti. Stabilità positiva. Piacere ritrovato nella vita di tutti i giorni.", "ROVESCIATA: Mancanza di stabilità negli affetti. Alti e bassi"],
    '3 di Coppe': ["Relazione di comprensione perfetta. Affari fruttuosi e pienamente appaganti. Sintonia completa e felicità. Nascita di opportunità.", "ROVESCIATA: Nuove opportunità sorgono all’orizzonte, ma sarà difficile riuscire ad approfittarne."],
    '2 di Coppe': ["Unione. Stretto legame con un’altra persona. Relazione prolifica. Amore.", "ROVESCIATA: Legame con un’altra persona che si sta incrinando. Problemi di coppia. Relazione gettata via."],
    'Asso di Coppe': ["Massimo della fertilità e della gioia di vivere. Forti soddisfazioni e sentimenti forti in arrivo.", "ROVESCIATA: Occasione sprecata, relazione gettata al vento, spreco di risorse, delusione."],
    'Re di Spade': ["Persona importante, un possibile alleato, persona di stimolo su di noi che ci motiva ad agire.", "ROVESCIATA: Persona che può ostacolarci."],
    'Regina di Spade': ["Donna da prendere come esempio e di cui seguire i consigli se vogliamo migliorare la nostra situazione. Donna leale e combattiva.", "ROVESCIATA: Donna che ci insidia."],
    'Cavaliere di Spade': ["Rabbia e aggressività positive. Persona pronta a prendere le nostre difese, agendo anche in modo molto duro.", "ROVESCIATA: Aggressività. Persona aggressiva nei nostri confronti."],
    'Fante di Spade': ["Soddisfazioni provenienti da azioni scorrette. Attrazione proibita nei confronti di un’altra persona. Azioni contro la morale o il senso comune, ma molto appaganti proprio per la loro rarità e per il gusto del proibito.", "ROVESCIATA: Cattive compagnie, compagnie pericolose"],
    '10  di Spade': ["Massimo livello di desiderio di primeggiare, di conquistare, di guadagnare a tutti i costi.", "ROVESCIATA: Profitti e vantaggi da azioni non oneste. Autorità guadagnata a discapito di altri."],
    '9 di Spade': ["Ambizione positiva, dinamismo vincente. Destreggiarsi ottimamente tra le insidie.", "ROVESCIATA: Numerose insidie, odio."],
    '8 di Spade': ["Situazione che richiede molto dinamismo. Buoni risultati, a patto che si profondano tutte le nostre energie nel progetto.", "ROVESCIATA: Opposizioni, incomprensioni."],
    '7 di Spade': ["Fine della vecchia strada. Nuovo progetto che richiede molte energie, nuovo progetto ambizioso.", "ROVESCIATA: Ostacolo, nuovo progetto rischioso."],
    '6 di Spade': ["Percorso, viaggio, scelta. Scelta da prendere che genera ansia ed irrequietezza.", "ROVESCIATA: Scelta errata, troppa foga nel prendere una scelta."],
    '5 di Spade': ["Grave perdita. Agitazione e perdita della razionalità e della tranquillità.", "ROVESCIATA: Forte dolore, preoccupazione forte, sensazione di non avere alcuna via d’uscita."],
    '4 di Spade': ["Solitudine e conflitto interiore. Ristrettezze, ostacoli", "ROVESCIATA: Abbandono, ossessione."],
    '3 di Spade': ["Rottura di una relazione o di una collaborazione. Rottura non necessariamente negativa.", "ROVESCIATA: Distacco traumatico, rottura traumatica."],
    '2 di Spade': ["Compagno d’armi ritrovato. Un alleato per combattere e farsi valere. Una persona leale", "ROVESCIATA: Scontro, duello. Contrasti con una persona amica."],
    'Asso di Spade': ["Forza e ambizione. Senza paura, sfrontati. Otterremo giustizia.", "ROVESCIATA: Risultare presuntuosi ed arroganti. Farsi giustizia da soli."],
    'Re di Denari': ["Uomo ricco, di potere. Persona con grande attitudine agli affari. Capo carismatico. Possesso di cose di valore, anche non necessariamente materiali.", "ROVESCIATA: Uomo corrotto, falso, egoista, ingannatore per perseguire i propri fini."],
    'Regina di Denari': ["Donna generosa. Donna ricca in tutti i sensi, soprattutto d’animo. Donna che può decisamente aiutare a trovare la felicità.", "ROVESCIATA: Aiuto rifiutato, figura femminile generosa ed altruista."],
    'Cavaliere di Denari': ["Successo negli affari. Dinamismo negli affari. Persona di supporto per i nostri affari, che aiuta molto il nostro successo personale.", "ROVESCIATA: Eccessivo desiderio di successo economico, persona che insegue troppo il denaro. Persona desiderosa del nostro denaro."],
    'Fante di Denari': ["Buone notizie sul lato economico. Persona che ci porta buone notizie.", "ROVESCIATA: Cattive notizie sul lato economico. Persona che ci porta cattive notizie."],
    '10  di Denari': ["Opportunità veramente molto grande, non è però detto che sapremo coglierla.", "ROVESCIATA: Attenzione che più in alto si sale, maggiore è l’altezza da cui è possibile cadere."],
    '9 di Denari': ["Sicurezza economica. Le nostre qualità sono finalmente riconosciute ed apprezzate a fondo.", "ROVESCIATA: Prestare prudenza sul da farsi. Le conquiste personali non danno la felicità se ottenute con mancanza di rispetto dei valori morali: generano solo astio e commenti sgraditi."],
    '8 di Denari': ["Guadagniamo in serenità da una situazione positiva. Ci accorgiamo che i beni materiali rivestono scarsa importanza per la nostra ed altrui felicità.", "ROVESCIATA: Sentimenti contrapposti nei nostri confronti. Persona instabile nei nostri confronti."],
    '7 di Denari': ["Ottimi risultati, obiettivo raggiunto, suscitiamo curiosità positiva negli altri ed ammirazione.", "ROVESCIATA: Non ci accorgiamo di chi ci ammira."],
    '6 di Denari': ["Generosità altrui inaspettata, doni inaspettati, fortuna ed equilibrio, benessere materiale e generale.", "ROVESCIATA: Dubbi, equilibrio precario di una situazione."],
    '5 di Denari': ["Dinamismo. Importanti conquiste, non necessariamente materiali, all’orizzonte. Periodo felice in cui risultiamo apprezzati ed attraenti.", "ROVESCIATA: Successi esclusivamente materiali."],
    '4 di Denari': ["Equilibrio nella gestione delle risorse. Stabilità generale nella propria vita.", "ROVESCIATA: Situazione economica bloccata, mancanza di intraprendenza."],
    '3 di Denari': ["Carta positiva, vita felice, buoni affari in senso lato, non esclusivamente materiali. Ottima disposizione della situazione generale per il raggiungimento della nostra soddisfazione.", "ROVESCIATA: Occasione molto positiva non colta. La situazione rimane positiva, ma poteva decisamente passare ad un livello superiore."],
    '2 di Denari': ["Collaborazioni d’affari. Lato sia positivo che negativo del denaro. Buon partner con cui fare affari.", "ROVESCIATA: Personalità disturbata, tensioni contrapposte, dubbi morali."],
    'Asso di Denari': ["Realizzazione dei nostri desideri. Felicità, addirittura euforia. Carta estremamente positiva, soprattutto dal lato economico, ma non solo.", "ROVESCIATA: Desiderio eccessivo verso il denaro, avidità."]
}

n_card = 0
ZODIAC_API="https://zodiacal.herokuapp.com"

import math
import datetime
import requests
from dateutil.parser import parse
from operator import le, ge

def  physical_bio(numDays):
    return bio(numDays, 23)
    
def  emotional_bio(numDays):
    return bio(numDays, 28)
    
def  intellectual_bio(numDays):
    return bio(numDays, 33)
    
def bio(num_days, range_days):
    days_in_range = num_days % range_days
    ratio = (days_in_range*2)/range_days
    return math.sin(ratio * math.pi)

def compare(your_days, its_days, bio_fun):
    res = { 'max_value': -3, 'max_days': -1, 'min_value': 3, 'min_days': -1}
    for x in range(33):
        value = bio_fun(your_days+x) + bio_fun(its_days+x) 
        if value > res['max_value']:
            res['max_value'] = value
            res['max_days'] = x
        if value < res['min_value']:
            res['min_value'] = value
            res['min_days'] = x
    return (res['max_days'], res['min_days'], str_value(res['max_value']))
    
def max_bio(num_days, bio_fun, math_fun = ge):
    res = { 'value': None, 'days': -1}
    for x in range(33):
        if not res['value'] or math_fun(bio_fun(num_days+x), res['value']):
            res['value'] = bio_fun(num_days+x)
            res['days'] = x
    return res['days']

def str_value(value):
    if value <= 0.2:
        return "very low affinity"
    elif value <= 0.5:
        return "low affinity"
    elif value <= 1:
        return "average affinity"
    elif value <= 1.5:
        return "average affinity"
    elif value <= 1.8:
        return "very good affinity"
    elif value > 1.8:
        return "perfect affinity"

def shuffle(cards):
    import random
    random.shuffle(cards)
    return cards

def extract(num_cards, shuffled, cards_dic):
    from random import seed, randint
    global n_card
    for card in range(num_cards):
        extracted = shuffled[n_card]
        n_card+=1
        rev = 0 if randint(0,10) < 8 else 1
        print("%s: %s" % (extracted, cards_dic[extracted][rev]))

def zodiac(dob):
    resp = requests.get(ZODIAC_API + "/api")
    dob_month = dob.strftime('%B')
    user_sign = None
    for zsign in resp.json():
        st_val = zsign['sun_dates'][0].split()
        end_val = zsign['sun_dates'][1].split()
        if((st_val[0] == dob_month and int(st_val[1]) <= dob.day) or (end_val[0] == dob_month and int(end_val[1]) >= dob.day)):
            user_sign = zsign
            break
    print("----------------------------------------------------------------------------")
    print("The zodiac sign is %s (%s sign)" % (user_sign['name'], user_sign['element']))
    print("Secret wishes: %s" % user_sign['secret_wish'])
    print("Hates: %s" % user_sign['hates'])
    print("Bad traits: %s" % user_sign['bad_traits'])
    print("Good traits: %s" % user_sign['good_traits'])
    print("Keywords: %s" % user_sign['keywords'])
    print("Vibe: %s" % user_sign['vibe'])
    print("Mental traits: %s" % user_sign['mental_traits'])
    print("----------------------------------------------------------------------------")
    return user_sign

def main():
    print("Insert your DOB in format 'YYYY-MM-DD'")
    date_of_birth = parse(input())
    your_dob = datetime.datetime.now() - date_of_birth
    print("You are old %s days" % str(your_dob.days))
    print("Your best physical biorythm is in %s days, your worst is in %s days" % (max_bio(your_dob.days, physical_bio), max_bio(your_dob.days, physical_bio, le)))
    print("Your best emotional biorythm is in %s days, your worst is in %s days" % (max_bio(your_dob.days, emotional_bio), max_bio(your_dob.days, emotional_bio, le)))
    print("Your best intellectual biorythm is in %s days, your worst is in %s days" % (max_bio(your_dob.days, intellectual_bio), max_bio(your_dob.days, intellectual_bio, le)))
    #your_sign = zodiac(date_of_birth)
    print("Insert your interested person DOB in format 'YYYY-MM-DD' (return for no comparison)")
    its_dob = input()
    if len(its_dob) > 0:
        #its_sign = zodiac(parse(its_dob))
        #print("You are %s compatible with that and it is %s compatible with you" % ("" if its_sign['name'] in your_sign['compatibility'] else "not", "" if your_sign['name'] in its_sign['compatibility'] else "not"))
        its_dob = datetime.datetime.now() - parse(its_dob)
        print("His/her best physical biorythm is in %s days, the worst is in %s days" % (max_bio(its_dob.days, physical_bio), max_bio(its_dob.days, physical_bio, le)))
        print("His/her best emotional biorythm is in %s days, the worst is in %s days" % (max_bio(its_dob.days, emotional_bio), max_bio(its_dob.days, emotional_bio, le)))
        print("His/her best intellectual biorythm is in %s days, the worst is in %s days" % (max_bio(its_dob.days, intellectual_bio), max_bio(its_dob.days, intellectual_bio, le)))
        phy_diff = compare(your_dob.days, its_dob.days, physical_bio)
        emo_diff = compare(your_dob.days, its_dob.days, emotional_bio)
        int_diff = compare(your_dob.days, its_dob.days, intellectual_bio)
        print()
        print("Your best physical day is in %s days, the worst is in %s days (%s)" % phy_diff)
        print("Your best emotional day is in %s days, the worst is in %s days (%s)" % emo_diff)
        print("Your best intellectual day is in %s days, the worst is in %s days (%s)" % int_diff)
    print("Lettura Tarocchi")
    print()
    cards = shuffle(list(tarocs.keys()))
    extract(3, cards, tarocs)
    others = input("N. cards:")
    while others:
        extract(int(others), cards, tarocs)
        others = input("N. cards:")
    
main()
