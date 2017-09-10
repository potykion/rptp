import {
    MuiThemeProvider, Paper
} from "material-ui";
import * as React from "react";

import darkBaseTheme from 'material-ui/styles/baseThemes/darkBaseTheme';

import {
    grey900, pinkA100, blueGrey100, black, orange600, orange300, blueGrey600,
    pink50, pink100
} from 'material-ui/styles/colors';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MainAppBar from "./MainAppBar";
import VideoView from "./VideoView";
import RefreshFloatingActionButton from "./RefreshFloatingActionButton";
import {connect} from "react-redux";


let MaterialUIContainer = ({kittySetting}) => {
    let muiTheme;

    if (kittySetting) {
        muiTheme = getMuiTheme({
            palette: {
                primary1Color: pinkA100
            }
        });
    }
    else {
      muiTheme = getMuiTheme({
            palette: {
                primary1Color: pink100
            }
        });

    }


    return (
        <MuiThemeProvider muiTheme={muiTheme}>
            <div>
                <MainAppBar/>
                <Paper>
                    <VideoView/>
                    <RefreshFloatingActionButton/>
                </Paper>
            </div>
        </MuiThemeProvider>
    );

};

MaterialUIContainer = connect((state) => ({
        kittySetting: state.gui.kittySetting
    })
)(MaterialUIContainer);


export default MaterialUIContainer;