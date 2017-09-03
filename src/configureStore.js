import {createStore, applyMiddleware} from 'redux';
import {throttle} from "lodash";
import thunk from 'redux-thunk'
import rptp from "./reducers";
import {loadState, saveState} from "./utils";
import {computeContainerWidth} from "./actions";


const configureStore = () => {
    const persistedState = loadState();
    const middlewares = [thunk];

    const store = createStore(rptp, persistedState, applyMiddleware(...middlewares));

    store.subscribe(throttle(() => {
        saveState(store.getState());
    }, 1000));

    store.dispatch(computeContainerWidth());

    return store;
};

export default configureStore;