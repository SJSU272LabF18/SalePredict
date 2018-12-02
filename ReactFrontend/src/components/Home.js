import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Home extends Component {
    state = {}
    render() {
        return (<div>

            <Link to='/mainpage'><img src='MainPage.jpeg'></img></Link>

        </div>);
    }
}

export default Home;