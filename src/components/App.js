import React, {Component} from 'react';
import {connect} from "react-redux";
import {computeContainerWidth} from "../actions";

class App extends Component {

    componentDidMount() {
        window.addEventListener("resize", this.onResize);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.onResize);
    }

    onResize = () => {
        this.props.dispatch(computeContainerWidth());
    };

    render() {
        return (
            <h1>{this.props.width}</h1>
        );
    }
}

App = connect(
    (state) => ({
        ...state
    })
)(App);

export default App;
