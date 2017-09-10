import {KITTY_IMAGE, videos} from "../sample";
import {Card, CardMedia, CardText, IconButton, Paper, TextField} from "material-ui";
import * as React from "react";
import {connect} from "react-redux";

import SearchIcon from 'material-ui/svg-icons/action/search';

let VideoView = ({width, kittySetting}) => (
    <Paper style={{width: width, margin: 'auto'}}>
        <div style={{textAlign: 'center', paddingTop: 20}}>
            <TextField
                style={{width: width / 2, marginRight: 5}}
                hintText="Hint Text"
            />
            <IconButton
                href="https://github.com/callemall/material-ui"
                target="_blank"

            >
                <SearchIcon/>
            </IconButton>
        </div>


        <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center',}}>
            {videos.map(video => (
                <Card style={{margin: 10, width: width / 4}}>
                    <CardMedia>
                        <img
                            src={kittySetting ? KITTY_IMAGE : video.thumb}
                            alt="" style={{cursor: 'pointer'}} onClick={() => {
                            alert('op')
                        }}/>
                    </CardMedia>

                    <CardText>
                        {video.title}
                    </CardText>
                </Card>
            ))}
        </div>
    </Paper>

);

VideoView = connect(state => ({
    width: state.gui.width,
    kittySetting: state.gui.kittySetting
}))(VideoView);


export default VideoView;