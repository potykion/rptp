import React from 'react';
import ReactDOM from 'react-dom';
import Root from "./components/Root";

import injectTapEventPlugin from 'react-tap-event-plugin';
import configureStore from "./configureStore";

injectTapEventPlugin();

const store = configureStore();

ReactDOM.render(
    <Root store={store}/>,
    document.getElementById('root')
);
