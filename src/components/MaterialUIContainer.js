import {
    AppBar, Card, CardMedia, CardText, Dialog, Drawer, FlatButton, FloatingActionButton, FontIcon, GridList, IconButton,
    IconMenu,
    MenuItem,
    MuiThemeProvider, Paper,
    TextField
} from "material-ui";
import * as React from "react";
import videos from "../sample";
import SearchIcon from 'material-ui/svg-icons/action/search';
import CachedIcon from 'material-ui/svg-icons/action/cached';
import MoreVertIcon from 'material-ui/svg-icons/navigation/more-vert';

import {grey900, pinkA100, purpleA100, blueGrey800} from 'material-ui/styles/colors';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import {connect} from "react-redux";

const kittySet = true;

const muiTheme = getMuiTheme({
    palette: {
        primary1Color: kittySet ? purpleA100 : grey900,
    },
});

class MaterialUIContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            drawerOpen: false,
            settingsOpen: false
        };
    }

    render() {
        const {width} = this.props;
        return (
            <MuiThemeProvider muiTheme={muiTheme}>
                <div>
                    <AppBar
                        title={`rptp`}
                        onLeftIconButtonTouchTap={() => this.setState({drawerOpen: true})}
                        iconElementRight={<IconMenu
                            iconButtonElement={
                                <IconButton><MoreVertIcon/></IconButton>
                            }
                            targetOrigin={{horizontal: 'right', vertical: 'top'}}
                            anchorOrigin={{horizontal: 'right', vertical: 'top'}}
                        >
                            <MenuItem primaryText={`Settings`} onClick={() => this.setState({settingsOpen: true})}/>
                            <MenuItem primaryText="Sign out"/>
                        </IconMenu>}

                    />

                    <Paper className='mt-3' style={{width: width, margin: 'auto'}}>
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
                                            src={kittySet ? 'http://a.fod4.com/images/user_photos/1343865/335cd5249b648648fb0b086282cbaf32_original.jpg' : video.thumb}
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

                    <Drawer
                        open={this.state.drawerOpen}
                        docked={false}
                        onRequestChange={(open) => this.setState({drawerOpen: open})}

                    >
                        <AppBar title={`rptp`} showMenuIconButton={false}/>
                        <MenuItem leftIcon={<SearchIcon/>}>Search videos</MenuItem>
                        <MenuItem leftIcon={<CachedIcon/>}>Refresh actress</MenuItem>
                    </Drawer>

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

                    <Dialog
                        title="Dialog With Actions"
                        actions={[
                            <FlatButton
                                label="Cancel"
                                primary={true}
                                onClick={() => this.setState({settingsOpen: false})}
                            />,
                            <FlatButton
                                label="Submit"
                                primary={true}
                                keyboardFocused={true}
                                onClick={() => this.setState({settingsOpen: false})}
                            />,
                        ]}
                        modal={false}
                        open={this.state.settingsOpen}
                        onRequestClose={() => this.setState({settingsOpen: false})}


                    >
                        The actions in this window were passed in as an array of React objects.
                    </Dialog>
                </div>
            </MuiThemeProvider>

        );
    }
}

MaterialUIContainer = connect(state => ({width: state.width}))(MaterialUIContainer);

export default MaterialUIContainer;