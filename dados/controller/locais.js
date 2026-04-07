(function () {
  const arquivos = [
    'dados/locais/elefante.js',
    'dados/locais/fortaleza.js',
    'dados/locais/cachoeiraBoaVista.js',
    'dados/locais/gameleira.js'
  ];

  let carregados = 0;

  function montarLocais() {
    window.LOCAIS = Object.freeze({
      elefante: window.LOCAL_ELEFANTE,
      fortaleza: window.LOCAL_FORTALEZA,
      cachoeiraBoaVista: window.LOCAL_CACHOEIRA,
      gameleira: window.LOCAL_GAMELEIRA
    });

    window.dispatchEvent(new Event('locaisLoaded'));
  }

  arquivos.forEach((src) => {
    const script = document.createElement('script');
    script.src = src;
    script.defer = true;

    script.onload = () => {
      carregados++;

      if (carregados === arquivos.length) {
        montarLocais();
      }
    };

    script.onerror = () => {
      console.error(`Erro ao carregar: ${src}`);
    };

    document.head.appendChild(script);
  });
})();