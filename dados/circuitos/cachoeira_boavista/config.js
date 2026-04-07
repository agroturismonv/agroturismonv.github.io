/**
 * CONFIGURAÇÃO DO CIRCUITO: Cachoeira Boa Vista
 * Localização: dados/circuitos/cachoeira_boavista/config.js
 */
window.CONFIG_CACHOEIRA_BOAVISTA = Object.freeze({
  id: 'cachoeira_boavista', // Ajustado para bater com o nome da pasta
  
  cover: 'imagens/boa_vista/cachoeira.jpg', // Sem ../ para o index.html funcionar
  banner: '../imagens/boa_vista/cachoeira.jpg', 

  texts: {
    pt: { title: 'Cachoeira Boa Vista', subtitle: 'Refúgio de águas cristalinas.' },
    en: { title: 'Boa Vista Waterfall', subtitle: 'A sanctuary of crystal clear waters.' },
    es: { title: 'Cascada Boa Vista', subtitle: 'Refugio de aguas cristalinas.' }
  },

  locais: ['boavista'] // ID minúsculo para bater com a chave do window.LOCAIS
});