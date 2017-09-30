import React from 'react';


import {Provider} from "react-redux";
import {BrowserRouter as Router} from "react-router-dom";
import MaterialUIContainer from "./MaterialUIContainer";
import ResponsiveContainer from "./ResponsiveContainer";



const Root = ({store}) => (
    <Provider store={store}>
        <Router>
            <ResponsiveContainer>
                <MaterialUIContainer/>
            </ResponsiveContainer>
        </Router>
    </Provider>
);

export default Root;