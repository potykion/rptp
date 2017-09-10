import {AppBar, Drawer, MenuItem, Toggle} from "material-ui";
import * as React from "react";
import {closeDrawer, toggleKittySetting} from "../actions";
import {connect} from "react-redux";
import SearchIcon from 'material-ui/svg-icons/action/search';
import CachedIcon from 'material-ui/svg-icons/action/cached';

let ActionDrawer = ({open, kittySetting, dispatch}) => (
    <Drawer
        open={open}
        docked={false}
        onRequestChange={() => {
            dispatch(closeDrawer());
        }}

    >
        <AppBar title={`rptp`} showMenuIconButton={false}/>
        <MenuItem leftIcon={<SearchIcon/>}>Search videos</MenuItem>
        <MenuItem leftIcon={<CachedIcon/>}>Refresh actress</MenuItem>

        <MenuItem>

            <Toggle
                style={{paddingTop: 14}}
                label="Kitties"
                toggled={kittySetting}
                onToggle={() => {
                    dispatch(toggleKittySetting());
                }}
            />
        </MenuItem>

    </Drawer>

);

ActionDrawer = connect((state) => ({
    open: state.gui.actionDrawerOpen,
    kittySetting: state.gui.kittySetting
}))(ActionDrawer);


export default ActionDrawer;