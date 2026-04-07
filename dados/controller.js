
(function () {
    const ESTRUTURA = {
  "cachoeira_boavista": {
    "config": "../dados/circuitos/cachoeira_boavista/config.js",
    "pontos": [
      {
        "id": "boavista",
        "src": "../dados/circuitos/cachoeira_boavista/boavista/boavista.js",
        "var": "LOCAL_BOAVISTA"
      }
    ]
  },
  "pedra_elefante": {
    "config": "../dados/circuitos/pedra_elefante/config.js",
    "pontos": [
      {
        "id": "gameleira",
        "src": "../dados/circuitos/pedra_elefante/gameleira/gameleira.js",
        "var": "LOCAL_GAMELEIRA"
      },
      {
        "id": "elefante",
        "src": "../dados/circuitos/pedra_elefante/pedra_elefante/elefante.js",
        "var": "LOCAL_ELEFANTE"
      }
    ]
  },
  "pedra_fortaleza": {
    "config": "../dados/circuitos/pedra_fortaleza/config.js",
    "pontos": [
      {
        "id": "fortaleza",
        "src": "../dados/circuitos/pedra_fortaleza/pedra_fortaleza/fortaleza.js",
        "var": "LOCAL_FORTALEZA"
      }
    ]
  }
};
    let carregados = 0;
    let total = 0;

    // Conta quantos scripts existem no total para saber quando parar
    Object.values(ESTRUTURA).forEach(c => {
        total += 1; // O config.js
        total += c.pontos.length; // Os locais
    });

    function montarSistema() {
        // 1. Monta o banco de dados de locais (para circuitos.html e local.html)
        window.LOCAIS = {};
        // 2. Monta a lista de circuitos para o Slider (index.html)
        window.LISTA_CIRCUITOS = [];

        Object.values(ESTRUTURA).forEach(circuito => {
            // Busca a variável CONFIG_ gerada pelo config.js
            const nomePasta = Object.keys(ESTRUTURA).find(key => ESTRUTURA[key] === circuito).toUpperCase();
            const varConfig = "CONFIG_" + nomePasta;
            
            if(window[varConfig]) {
                window.LISTA_CIRCUITOS.push(window[varConfig]);
            }

            // Associa os locais carregados ao objeto window.LOCAIS
            circuito.pontos.forEach(ponto => {
                if(window[ponto.var]) {
                    window.LOCAIS[ponto.id] = window[ponto.var];
                }
            });
        });

        console.log("✅ Sistema Pronto: Index (Slider) e Circuitos conectados.");
        window.dispatchEvent(new Event('locais-ready'));
    }

    // Carregador Dinâmico
    Object.values(ESTRUTURA).forEach(circuito => {
        // Carrega o Config.js
        const sConf = document.createElement('script');
        sConf.src = circuito.config;
        sConf.onload = () => { if(++carregados === total) montarSistema(); };
        document.head.appendChild(sConf);

        // Carrega os Locais
        circuito.pontos.forEach(ponto => {
            const sLoc = document.createElement('script');
            sLoc.src = ponto.src;
            sLoc.onload = () => { if(++carregados === total) montarSistema(); };
            document.head.appendChild(sLoc);
        });
    });
})();
