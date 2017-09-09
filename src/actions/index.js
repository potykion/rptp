export const computeContainerWidth = () => {
    const width = (window.innerWidth > 1064)
        ? 1064
        : window.innerWidth * 0.95;
    return {
        type: 'CHANGE_CONTAINER_WIDTH',
        width
    }
};
