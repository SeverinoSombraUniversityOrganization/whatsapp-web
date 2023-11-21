// api-provider/controllers/WhatsAppClientController.js
const { Client } = require('whatsapp-web.js');
const axios = require('axios');
const authService = require('../services/authService');
const WhatsAppClientManagementService = require('../services/whatsAppClientManagementService');
const { flaskAppBaseUrl } = require('../config/flaskAppConfig');

class WhatsAppClientController {
    /**
     * Verifica se o token de autorização na requisição é válido.
     * @param {Object} req - O objeto de requisição.
     * @param {Object} res - O objeto de resposta.
     * @returns {boolean} - Retorna true se o token for válido, false caso contrário.
     */
    checkAuthToken(req, res) {
        const authToken = req.headers.authorization;

        if (!authService.isAuthTokenValid(authToken)) {
            res.status(401).json({ error: 'Unauthorized - Invalid Token' });
            return false;
        }

        return true;
    }

    /**
     * Handles the registration of Client Webhooks.
     * @param {Object} req - The request object.
     * @param {Object} res - The response object.
     */
    registerClientWebhook(req, res) {
        this.checkAuthToken(req, res);
        const { clients } = req.body;

        if (!Array.isArray(clients)) {
            return res.status(400).json({ error: 'Bad Request - Clients must be an array' });
        }

        clients.forEach((client) => {
        const { identifier, url, events } = client;

        if (!identifier || !url || !events) {
            return res.status(400).json({ error: 'Bad Request - Each client must have identifier, url, and events' });
        }

        WhatsAppClientManagementService.registerClient(identifier, url, events);
        });

        console.log(`Client Webhooks registered: ${JSON.stringify(WhatsAppClientManagementService.getAllClientConfigurations())}`);
        res.json({ message: 'Clients Webhooks successfully registered' });
    }

    /**
     * Handles the initialization of a Client.
     * @param {Object} req - The request object.
     * @param {Object} res - The response object.
     */
    initializeClient(req, res) {
        const { identifier } = req.params;
        const clientConfig = WhatsAppClientManagementService.getClientConfiguration(identifier);

        if (!clientConfig) {
            return res.status(404).json({ error: 'Not Found - Client not registered'});
        }

        if (clientConfig.started === true) {
            return res.status(200).json({ message: `Client ${identifier} is already started` });
        }

        const client = new Client({    
            puppeteer: {
                args: ['--no-sandbox']
            }
        });

        for (const eventName of clientConfig.events) {
            client.on(eventName, async (...eventArgs) => {
                const resolvedEventArgs = await Promise.all(eventArgs);
                axios.post(`${flaskAppBaseUrl}/event-hub/1`, {
                    "event": "qr",
                    "arguments": eventArgs
                  }, {
                    headers: {
                      'Content-Type': 'application/json',
                    },
                  })
                    .then((externalRes) => {
                      console.log('Dados de resposta:', externalRes.data);
                      console.log('Status:', externalRes.status);
                    })
                    .catch((error) => {
                      console.error('Erro na solicitação:', error.message);
                      console.error('Resposta do servidor:', error.response.data);
                      console.error('Status do erro:', error.response.status);
                    }
                );   
            });
        };

        try {
            clientConfig.started = true;
            client.initialize();
    
            console.log(`WhatsAppClient ${identifier} initialized`);
            return res.json({ message: `WhatsAppClient ${identifier} initialized successfully` });
        } catch (error) {
            console.error(`Error initializing WhatsAppClient ${identifier}:`, error.message);
            return res.status(500).json({ error: `Internal Server Error - Failed to initialize WhatsAppClient ${identifier}` });
        }
    }

    /**
     * Executes external argument configuration with local methods.
     * @param {Object} externalArgConfig - Configuration for external arguments.
     * @param {Array} localEventArgs - Local arguments containing methods.
     */
    executeExternalArgConfig(externalArgConfig, localEventArgs) {
        for (const externalArgEventName in externalArgConfig) {
            const argEventConfig = externalArgConfig[externalArgEventName];
            const localArg = localEventArgs[argEventConfig.index];

            for (const methodName in argEventConfig.methods) {
                const methodArgsArray = argEventConfig.methods[methodName];
                const localMethod = localArg[methodName];

                localMethod(...methodArgsArray);
            }
        }
    }

    /**
     * Handles the execution of external argument configurations.
     * @param {Object} clientConfig - Configuration for the WhatsApp client.
     * @param {string} eventName - Name of the triggered event.
     * @param {Array} eventArgs - Arguments of the triggered event.
     */
    async handleExternalExecution(clientConfig, eventName, eventArgs) {
        try {
            const externalRes = await axios.post(clientConfig.url, {
                event: eventName,
                arguments: eventArgs,
            });

            const externalData = externalRes.data;
            const externalArgConfig = externalData.toExecute;

            this.executeExternalArgConfig(externalArgConfig, eventArgs);

        } catch (error) {
            console.error('Error while sending request:', error.message);
        }
    }

}

module.exports = new WhatsAppClientController();
