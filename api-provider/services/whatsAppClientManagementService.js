// api-provider/services/whatsAppClientManagementService.js
const { flaskAppBaseUrl } = require('../config/flaskAppConfig')

class WhatsAppClientManagementService {
    constructor() {
      this.clientWebhookConfig = {
        1: {
          url: `${flaskAppBaseUrl}/event-hub/1`,
          events: ['qr', 'message'],
          started: false,
        }
      };
      this.totalClients = Object.keys(this.clientWebhookConfig).length;
    }
  
    /**
     * Registers a client.
     * @param {string} identifier - The client identifier.
     * @param {string} url - The client URL.
     * @param {Object} events - The events associated with the client.
     */
    registerClient(identifier, url, events) {
      this.clientWebhookConfig[identifier] = { url, events };
    }
  
    /**
     * Gets the configuration for a registered client.
     * @param {string} identifier - The client identifier.
     * @returns {Object} - The configuration for the client.
     */
    getClientConfiguration(identifier) {
      return this.clientWebhookConfig[identifier];
    }
  
    /**
     * Gets the configurations for all registered clients.
     * @returns {Object} - The configurations for all clients.
     */
    getAllClientConfigurations() {
      return this.clientWebhookConfig;
    }
  
    /**
     * Gets the total number of registered clients.
     * @returns {number} - The total number of clients.
     */
    getTotalClients() {
      return this.totalClients;
    }
  }
  
module.exports = new WhatsAppClientManagementService();
  