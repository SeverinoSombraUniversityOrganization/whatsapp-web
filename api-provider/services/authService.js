// api-provider/services/authService.js
class AuthService {
    constructor() {
      this.AUTH_TOKEN = 'your_auth_token';
    }
  
    /**
     * Verifica se o token de autorização é válido.
     * @param {string} authToken - O token de autorização fornecido na requisição.
     * @returns {boolean} - Retorna true se o token for válido, false caso contrário.
     */
    isValidAuthToken(authToken) {
      return authToken === this.AUTH_TOKEN;
    }
  }
  
  module.exports = new AuthService();
  