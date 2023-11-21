// api-provider/controllers/WhatsAppClientController.js
const { Client } = require('whatsapp-web.js');
const axios = require('axios');
const authService = require('../services/authService');
const WhatsAppClientManagementService = require('../services/whatsAppClientManagementService');

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
                const eventResponse = await axios.post(clientConfig.url, {
                    "event": eventName,
                    "arguments": resolvedEventArgs
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });    
                const externalEventData = eventResponse.data;
                const externalArgConfig = externalEventData.argConfig;
                WhatsAppClientManagementService.executeExternalArgCommands(externalArgConfig, resolvedEventArgs);
            })
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

}

module.exports = new WhatsAppClientController();
