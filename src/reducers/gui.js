const gui = (state = {
    actionDrawerOpen: false,
    settingsDialogOpen: false,
    kittySetting: true
}, action) => {
    switch (action.type) {
        case 'OPEN_ACTION_DRAWER':
            return {...state, actionDrawerOpen: true};
        case 'CLOSE_ACTION_DRAWER':
            return {...state, actionDrawerOpen: false};
        case 'OPEN_SETTINGS_DIALOG':
            return {...state, settingsDialogOpen: true};
        case 'CLOSE_SETTINGS_DIALOG':
            return {...state, settingsDialogOpen: false};
        case 'CHANGE_CONTAINER_WIDTH':
            return {...state, width: action.width};
        case 'TOGGLE_KITTY_SETTING':
            return {...state, kittySetting: !state.kittySetting};
        default:
            return state;
    }
};

export default gui;