// admin/auth.js
(function() {
    // Verifica se a chave de autenticação existe na sessão do navegador
    const isLogged = sessionStorage.getItem('admin_logged');
    
    // Se não estiver logado e não for a página de login, redireciona
    if (!isLogged && !window.location.pathname.includes('login.html')) {
        window.location.href = window.location.pathname.includes('/forms/') ? '../login.html' : 'login.html';
    }
})();

/**
 * Encerra a sessão administrativa
 */
function logout() {
    sessionStorage.removeItem('admin_logged');
    // Ajusta o caminho de retorno dependendo de onde o usuário está
    const loginPath = window.location.pathname.includes('/forms/') ? '../login.html' : 'login.html';
    window.location.href = loginPath;
}