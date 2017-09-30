import {KITTY_IMAGE} from "../sample";
import {Card, CardMedia, CardText, IconButton, Paper, TextField} from "material-ui";
import * as React from "react";
import {connect} from "react-redux";

import SearchIcon from 'material-ui/svg-icons/action/search';
import {findVideos} from "../actions/index";
import {Redirect, withRouter} from "react-router-dom";
import RefreshFloatingActionButton from "./RefreshFloatingActionButton";

class VideoView extends React.Component {
    constructor(props) {
        super(props);

        const {match, location} = this.props;

        this.state = {
            actressInput: match.params.actress,
        }
    }

    componentDidMount() {
        let {dispatch, match} = this.props;

        dispatch(findVideos(
            this.state.actressInput
        ));
    }

    render() {
        const {width, kittySetting, videos, dispatch} = this.props;

        return (
            <Paper style={{width: width, margin: 'auto'}}>
                <div style={{textAlign: 'center', paddingTop: 20}}>
                    <TextField
                        style={{width: width / 2, marginRight: 5}}
                        hintText="Hint Text"
                        value={this.state.actressInput}
                        onChange={(e) => {
                            this.setState({actressInput: e.target.value});
                        }}
                    />
                    <IconButton
                        onClick={() => {
                            dispatch(findVideos(this.state.actressInput))
                        }}

                    >
                        <SearchIcon/>
                    </IconButton>
                </div>


                <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center',}}>
                    {videos.map(video => (
                        <Card
                            key={video.url}
                            style={{margin: 10, width: width / 4}}>
                            <CardMedia>
                                <img
                                    src={kittySetting ? KITTY_IMAGE : video.preview}
                                    alt=""
                                    style={{cursor: 'pointer'}}
                                    onTouchTap={event => {
                                        window.location = video.url;
                                    }}
                                />

                            </CardMedia>

                            <CardText>
                                {video.title}
                            </CardText>
                        </Card>
                    ))}
                </div>

                <RefreshFloatingActionButton/>
            </Paper>

        );
    }

}


VideoView = withRouter(connect(state => ({
    width: state.gui.width,
    kittySetting: state.gui.kittySetting,
    ...state.video
}))(VideoView));


export default VideoView;