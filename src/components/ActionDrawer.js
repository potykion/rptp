import {AppBar, Drawer, MenuItem} from "material-ui";
import * as React from "react";
import {closeDrawer} from "../actions/index";
import {connect} from "react-redux";
import SearchIcon from 'material-ui/svg-icons/action/search';
import CachedIcon from 'material-ui/svg-icons/action/cached';

let ActionDrawer = ({open, dispatch}) => (
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
    </Drawer>

);

ActionDrawer = connect((state) => ({
    open: state.gui.actionDrawerOpen
}))(ActionDrawer);


export default ActionDrawer;