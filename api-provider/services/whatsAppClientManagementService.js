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

    /**
     * Executes external argument configuration with local methods.
     * @param {Object} externalArgConfig - Configuration for external arguments.
     * @param {Array} localArgs - Local arguments containing methods.
     */
    executeExternalArgCommands(externalArgConfig, localArgs) {
      try {
        for (const externalArgIndexKey in externalArgConfig) {
          if (externalArgConfig.hasOwnProperty(externalArgIndexKey)) {
            const localArg = localArgs[externalArgIndexKey];
            const externalArgObject = externalArgConfig[externalArgIndexKey];
    
            for (const methodName in externalArgObject.executedMethods) {
              if (externalArgObject.executedMethods.hasOwnProperty(methodName)) {
                const methodArgsArray = externalArgObject.executedMethods[methodName];
                const localMethod = localArg[methodName];
    
                if (typeof localMethod === 'function') {
                  localMethod.call(localArg, ...methodArgsArray);
                } else {
                  throw new Error(`Method ${methodName} is not a valid function.`);
                }
              }
            }
          }
        }
      } catch (error) {
        console.error(`Error in executeExternalArgCommands: ${error.message}`);
      }
    }
}
  
module.exports = new WhatsAppClientManagementService();
  