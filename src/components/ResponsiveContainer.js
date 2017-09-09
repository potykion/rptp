import {connect} from "react-redux";
import * as React from "react";
import {computeContainerWidth} from "../actions";

class ResponsiveContainer extends React.Component {
    componentDidMount() {
        window.addEventListener("resize", () => {
            this.props.dispatch(computeContainerWidth());
        });
    }

    componentWillUnmount() {
        window.removeEventListener('resize');
    }

    render() {
        return (
            <div>
                {this.props.children}
            </div>
        );
    }
}

ResponsiveContainer = connect()(ResponsiveContainer);

export default ResponsiveContainer