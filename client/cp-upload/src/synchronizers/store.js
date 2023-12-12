import {
    configureStore,
} from "@reduxjs/toolkit";
import createSagaMiddleware from "redux-saga";

import { all, fork} from 'redux-saga/effects';

const reducer = {
    
};

let sagaMiddleware = createSagaMiddleware();
const middleware = [sagaMiddleware];

function* rootSaga() {
    yield all ([
        
    ]);
}

const store = configureStore({
    reducer,
    middleware
});
sagaMiddleware.run(rootSaga);

export default store;
