// api-provider/controllers/WhatsAppClientController.js
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
            return res.status(404).json({ error: 'Not Found - Client not registered' });
        }

        const client = new Client();

        Object.keys(clientConfig.events).forEach((eventName) => {
            client.on(eventName, async (...eventArgs) => {
                const resolvedEventArgs = await Promise.all(eventArgs);
                this.handleExternalExecution(clientConfig, eventName, resolvedEventArgs);
            });
        });

        console.log(`Client ${identifier} initialized`);
        res.json({ message: `Client ${identifier} initialized successfully` });
    }

    /**
     * Executes external argument configuration with local methods.
     * @param {Object} externalArgConfig - Configuration for external arguments.
     * @param {Array} localEventArgs - Local arguments containing methods.
     */
    async executeExternalArgConfig(externalArgConfig, localEventArgs) {
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

            executeExternalArgConfig(externalArgConfig);

        } catch (error) {
            console.error('Error while sending request:', error.message);
        }
    }

}

module.exports = new WhatsAppClientController();
