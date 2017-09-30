import gui from "./gui";
import {combineReducers} from "redux";
import video from "./video";
import { routerReducer } from 'react-router-redux'


const rptp = combineReducers({
    gui,
    video
});

export default rptp;