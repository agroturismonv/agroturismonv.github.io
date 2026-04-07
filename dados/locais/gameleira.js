window.LOCAL_GAMELEIRA = Object.freeze({
  id: 'gameleira',

  cover: 'https://terracapixaba.com/wp-content/uploads/2024/02/gameleira-de-nova-venecia-2.webp',

  hero: 'imagens/santuario/santuario-1.jpg',

  gallery: [
    'imagens/santuario/santuario.webp',
    'imagens/santuario/santuario-1.jpg',
    'imagens/santuario/santuario-2.jpg'
  ],

  location: {
   maps: 'https://www.google.com/maps/search/Santuário+Mãe+Peregrina+Gameleira+Nova+Venécia',
   mapEmbed: 'https://www.google.com/maps?q=Santuário+Mãe+Peregrina+Gameleira+Nova+Venécia&output=embed',
   qr: 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://www.google.com/maps/search/Santuário+Mãe+Peregrina+Gameleira+Nova+Venécia',
  },

  texts: {
     pt: {
        title: 'Santuário da Mãe Peregrina',
        subtitle: 'Fé, espiritualidade e paz',
        about: 'Sobre o local',
        description:
          'Localizado na comunidade da Gameleira, o Santuário da Mãe Peregrina é um importante ponto de devoção religiosa em Nova Venécia. O espaço oferece um ambiente de paz, reflexão e espiritualidade, recebendo visitantes e fiéis durante todo o ano.',
        gallery: 'Galeria de Fotos',
        location: 'Como chegar',
        qr: 'Escaneie o QR Code para abrir no Google Maps'
      },
      en: {
        title: 'Mother Pilgrim Shrine',
        subtitle: 'Faith and spirituality',
        about: 'About',
        description:
          'Located in the Gameleira community, the Mother Pilgrim Shrine is an important religious site in Nova Venécia. It offers a peaceful environment for prayer, reflection, and spiritual connection.',
        gallery: 'Photo Gallery',
        location: 'How to get there',
        qr: 'Scan the QR Code to open Google Maps'
      },
      es: {
        title: 'Santuario de la Madre Peregrina',
        subtitle: 'Fe y espiritualidad',
        about: 'Sobre el lugar',
        description:
          'Ubicado en la comunidad de Gameleira, el Santuario de la Madre Peregrina es un importante punto religioso de Nova Venécia. Ofrece un ambiente de paz, oración y reflexión espiritual.',
        gallery: 'Galería de Fotos',
        location: 'Cómo llegar',
        qr: 'Escanee el código QR para abrir Google Maps'
      }
  },

  RAvisionButton: 'Veja em 360°',
  RAvisionScreen: true,
  RAvisionlink: 'https://novavenecia360.com.br/',
})