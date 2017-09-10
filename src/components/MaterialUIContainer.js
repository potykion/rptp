import {
    MuiThemeProvider
} from "material-ui";
import * as React from "react";

import {grey900, pinkA100} from 'material-ui/styles/colors';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MainAppBar from "./MainAppBar";
import VideoView from "./VideoView";
import RefreshFloatingActionButton from "./RefreshFloatingActionButton";
import {connect} from "react-redux";


let MaterialUIContainer = ({kittySet}) => {
    const muiTheme = getMuiTheme({
        palette: {
            primary1Color: kittySet ? pinkA100 : grey900,
        },
    });

    return (
        <MuiThemeProvider muiTheme={muiTheme}>
            <div>
                <MainAppBar/>
                <VideoView/>
                <RefreshFloatingActionButton/>
            </div>
        </MuiThemeProvider>
    );

};

MaterialUIContainer = connect((state) => ({
        kittySet: state.gui.kittySet
    })
)(MaterialUIContainer);


export default MaterialUIContainer;