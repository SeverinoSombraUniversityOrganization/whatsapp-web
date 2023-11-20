const clientWebhookConfig = {};

const registerClientWebhook = (req, res) => {
  const { url, events } = req.body;

  clientWebhookConfig[url] = { events };

  console.log(`Client Webhook registered for ${url} with events ${events}`);
  res.json({ message: 'Client Webhook successfully registered' });
};

module.exports = {
  registerClientWebhook,
};
