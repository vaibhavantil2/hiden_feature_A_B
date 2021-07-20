module.exports = global.Project = {
    api: 'https://api.flagsmith.com/api/v1/',
    flagsmithClientAPI: 'https://api.flagsmith.com/api/v1/',
    flagsmith: '4vfqhypYjcPoGGu8ByrBaj', // This is our Bullet Train API key - Bullet Train runs on Bullet Train!
    env: 'prod', // This is used for Sentry tracking
    sentry: 'https://2f6eb58a3987406aaeee38d5f0c38005@o486744.ingest.sentry.io/5666694',
    maintenance: false, // trigger maintenance mode
    cookieDomain: '.flagsmith.com',
    excludeAnalytics: 'nightwatch@solidstategroup.com',
    delighted: true, // determines whether to shw delighted feedback widget
    demoAccount: {
        email: 'kyle+bullet-train@solidstategroup.com',
        password: 'demo_account',
    },
    chargebee: {
        site: 'flagsmith',
    },
    assetUrl: 'https://cdn.flagsmith.com', // Location of the static files from build/, should contain a directory called static/
};
