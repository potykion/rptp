import {Dialog, FlatButton} from "material-ui";
import * as React from "react";
import {connect} from "react-redux";
import {closeSettingsDialog} from "../actions/index";

let SettingsDialog = ({open, dispatch}) => (
    <Dialog
        title="Dialog With Actions"
        actions={[
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={() => {
                    dispatch(closeSettingsDialog())
                }}
            />,
            <FlatButton
                label="Submit"
                primary={true}
                keyboardFocused={true}
                onClick={() => {
                    dispatch(closeSettingsDialog())
                }}
            />,
        ]}
        modal={false}
        open={open}
        onRequestClose={() => {
            dispatch(closeSettingsDialog())
        }}


    >
        The actions in this window were passed in as an array of React objects.
    </Dialog>
);
SettingsDialog = connect((state) => ({
    open: state.gui.settingsDialogOpen
}))(SettingsDialog);

export default SettingsDialog;
