import {AppBar, IconButton, IconMenu, MenuItem} from "material-ui";
import ActionDrawer from "./ActionDrawer";
import SettingsDialog from "./SettingsDialog";
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';
import * as React from "react";
import {connect} from "react-redux";
import {openActionDrawer, openSettingsDialog} from "../actions/index";

class MainAppBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            drawerOpen: false,
            settingsOpen: false
        };
    }

    render() {
        const {dispatch} = this.props;

        return (
            <div>
                <AppBar
                    title={`rptp`}
                    onLeftIconButtonTouchTap={() => {
                        dispatch(openActionDrawer());
                    }}
                    iconElementRight={<IconMenu
                        iconButtonElement={
                            <IconButton><MoreVertIcon/></IconButton>
                        }
                        targetOrigin={{horizontal: 'right', vertical: 'top'}}
                        anchorOrigin={{horizontal: 'right', vertical: 'top'}}
                    >
                        <MenuItem primaryText={`Settings`} onClick={() => {
                            dispatch(openSettingsDialog());
                        }}/>
                        <MenuItem primaryText="Sign out"/>
                    </IconMenu>}
                />

                <ActionDrawer/>

                <SettingsDialog/>
            </div>
        )
    }
}

MainAppBar = connect()(MainAppBar);

export default MainAppBar;