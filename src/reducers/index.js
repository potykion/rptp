const rptp = (state = {}, action) => {
    switch (action.type) {
        case 'CHANGE_CONTAINER_WIDTH':
            return {
                ...state,
                width: action.width
            };
        default:
            return state;
    }
};

export default rptp;