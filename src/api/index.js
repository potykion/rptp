import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api';
const FAKE_TOKEN = '84ffd0451745f0b14dafcc68283abdeeb90b958dd88128025c67275cec33cdcfe49aecfe4025e6d9a3df2';

const toQueryString = (paramsObject) => {
    return Object
        .keys(paramsObject)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(paramsObject[key])}`)
        .join('&');
};

const apiRequest = (method, params) => {
    const url = `${API_URL}/${method}?${toQueryString({
        ...params,
        access_token: FAKE_TOKEN
    })}`;
    return axios.get(url);
};


export const requestVideos = (q, offset = 0) =>
    apiRequest('video/search', {q, offset}).then(
        (response) => ({
            videos: response.data.videos,
            offset: response.data.offset
        })
    );