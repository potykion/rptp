const video = (state = {videos: [], offset: 0}, action) => {
    switch (action.type) {
        case 'FIND_VIDEOS':
            return {
                ...state,
                videos: action.videos,
                offset: action.offset
            };
        default:
            return state;
    }
};

export default video;