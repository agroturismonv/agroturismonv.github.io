/**
 * CONFIGURAÇÃO DO CIRCUITO: Pedra da Fortaleza
 */
window.CONFIG_PEDRA_FORTALEZA = Object.freeze({
  id: 'pedra_fortaleza',
  
  // Imagem para o Slider da Home (Caminho a partir da Raiz)
  cover: '../imagens/fortaleza/fortaleza.jpg', 
  
  // Imagem para o Topo do circuitos.html (Caminho a partir de /layout/)
  banner: '../imagens/fortaleza/fortaleza.jpg', 

  texts: {
    pt: { 
      title: 'Pedra da Fortaleza', 
      subtitle: 'O ponto mais alto para contemplar a imensidão veneciana.' 
    },
    en: { 
      title: 'Fortress Rock', 
      subtitle: 'The highest point to contemplate the Venetian immensity.' 
    },
    es: { 
      title: 'Piedra Fortaleza', 
      subtitle: 'El punto más alto para contemplar la inmensidad veneciana.' 
    }
  },

  // IDs dos locais que aparecem no grid deste circuito
  locais: ['fortaleza'] 
});

