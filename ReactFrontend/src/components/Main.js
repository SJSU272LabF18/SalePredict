import React, { Component } from 'react';
import { Route, BrowserRouter } from 'react-router-dom';
import MainPage from './MainPage';
import Home from './Home';


// import Create from './Create/Create';
// import Navbar2 from './Navbar/Navbar2';
//Create a Main Component
class Main extends Component {
    render() {
        return (
            <div >

                <Route path="/mainpage" component={MainPage} />
                <Route path="/home" component={Home} />

            </div>
        )
    }
}
//Export The Main Component
export default Main;