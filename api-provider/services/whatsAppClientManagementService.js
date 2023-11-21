// api-provider/services/whatsAppClientManagementService.js
class WhatsAppClientManagementService {
    constructor() {
      this.clientWebhookConfig = {};
      this.totalClients = 0;
    }
  
    /**
     * Registers a client.
     * @param {string} identifier - The client identifier.
     * @param {string} url - The client URL.
     * @param {Object} events - The events associated with the client.
     */
    registerClient(identifier, url, events) {
      this.clientWebhookConfig[identifier] = { url, events };
      this.totalClients += 1;
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
  