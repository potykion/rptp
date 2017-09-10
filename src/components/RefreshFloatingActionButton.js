import {FloatingActionButton} from "material-ui";
import * as React from "react";
import CachedIcon from 'material-ui/svg-icons/action/cached';

let RefreshFloatingActionButton = () => (
    <FloatingActionButton style={{
        margin: 0,
        top: 'auto',
        right: 20,
        bottom: 20,
        left: 'auto',
        position: 'fixed',
        zIndex: 1
    }}>
        <CachedIcon/>
    </FloatingActionButton>
);

export default RefreshFloatingActionButton;