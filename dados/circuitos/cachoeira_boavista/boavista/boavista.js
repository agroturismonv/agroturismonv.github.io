/**
 * LOCAL: Cachoeira Boa Vista
 * Localização: dados/circuitos/cachoeira_boavista/boavista/boavista.js
 */
window.LOCAL_BOAVISTA = Object.freeze({ // Ajustado de LOCAL_CACHOEIRABOAVISTA para LOCAL_BOAVISTA
  id: 'boavista', 

  cover: '../imagens/boa_vista/cachoeira.jpg',
  hero: '../imagens/boa_vista/cachoeira.jpg',

  gallery: [
    '../imagens/boa_vista/cachoeira.jpg',
    '../imagens/boa_vista/cachoeira-1.jpg',
    '../imagens/boa_vista/cachoeira-2.jpg'
  ],

  location: {
    maps: 'https://goo.gl/maps/exemplo', 
    qr: 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://www.google.com/maps/search/Cachoeira+Boa+Vista+Nova+Venécia',
  },

  texts: {
    pt: {
      title: 'Cachoeira Boa Vista',
      subtitle: 'Lazer, descanso e natureza',
      description: 'A Cachoeira Boa Vista é um refúgio natural ideal para quem busca descanso e contato com a natureza.'
    },
    en: {
      title: 'Boa Vista Waterfall',
      subtitle: 'Leisure and nature',
      description: 'Boa Vista Waterfall is a natural retreat perfect for relaxation and contact with nature.'
    },
    es: {
      title: 'Cascada Boa Vista',
      subtitle: 'Ocio y naturaleza',
      description: 'La Cascada Boa Vista es un refugio natural ideal para el descanso y el contacto con la naturaleza.'
    }
  },

  RAvisionScreen: false,
  RAvisionlink: 'https://novavenecia360.com.br/'
});