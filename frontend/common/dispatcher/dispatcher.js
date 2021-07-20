const ReactDispatcher = require('flux-react-dispatcher');

const Dispatcher = new ReactDispatcher();

const theDispatcher = Object.assign(Dispatcher, {
    handleViewAction(action) {
        const that = this;

        const payload = {
            source: 'VIEW_ACTION',
            action,
        };

        API.log(payload.action.actionType, payload.action);

        that.dispatch(payload);
    },

});

window.Dispatcher = Dispatcher;
module.exports = theDispatcher;
