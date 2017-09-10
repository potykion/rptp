export const computeContainerWidth = () => {
    const width = (window.innerWidth > 1064)
        ? 1064
        : window.innerWidth * 0.95;
    return {
        type: 'CHANGE_CONTAINER_WIDTH',
        width
    }
};

export const openActionDrawer = () => ({
    type: 'OPEN_ACTION_DRAWER'
});

export const closeDrawer = () => ({
    type: 'CLOSE_ACTION_DRAWER'
});

export const openSettingsDialog = () => ({
    type: 'OPEN_SETTINGS_DIALOG'
});

export const closeSettingsDialog = () => ({
    type: 'CLOSE_SETTINGS_DIALOG'
});

export const toggleKittySetting = () => ({
    type: 'TOGGLE_KITTY_SETTING'
});