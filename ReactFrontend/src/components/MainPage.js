import React, { Component } from 'react';
import axios from 'axios';
import '../css/MainPage.css';
import { Link } from 'react-router-dom';

import { Navbar, Nav, NavDropdown, MenuItem, FormGroup, FormControl, InputGroup, DropdownButton } from 'react-bootstrap';

import AgeGroupChart from './AgeGroupChart';
import RatingsChart from './RatingsChart';

class MainPage extends Component {
    constructor() {
        super();
        this.state = {
            description: "",
            loading: false,
            next: false

        };
        this.submitDescription = this.submitDescription.bind(this);
        this.onChange = this.onChange.bind(this);

    }

    onChange(e) {

        this.setState({
            [e.target.name]: e.target.value

        })
    }
    async submitDescription() {
        this.setState({ loading: true });
        var data = {
            description: this.state.description
        }

        // var newdata = bodyFormData.set('description', this.state.description);
        console.log('data ' + JSON.stringify(data))
        // axios.post(`http://localhost:5000/json_description`, querystring.stringify({ description: this.state.description }))
        const response = await axios.post(`http://localhost:5000/json_description`, data)


        console.log(" response.data" + response)

        console.log(" response.data" + JSON.stringify(response.data))
        localStorage.setItem("data", JSON.stringify(response.data))
        this.setState({ loading: false })
        this.setState({ next: true })


    }
    render() {
        const { loading } = this.state;
        const { next } = this.state;
        if (loading) {
            return (
                <div id="app" class="loader"></div>)
        }
        if (next) {
            return (
                <div class="wrapper">

                    <nav id="sidebar">
                        <div class="sidebar-header">
                            <h3>Will It Sell</h3>
                        </div>

                        <ul class="list-unstyled components">
                            <p> Insights</p>

                            <li>
                                <a href="#userratings" data-toggle="tab" >User Ratings</a>

                            </li>
                            <li>
                                <a href="#agegroup" data-toggle="tab" >Age Group</a>
                            </li>
                            <li>
                                <a href="#predictions" data-toggle="tab" >Predictions</a>
                            </li>
                        </ul>

                    </nav>

                    <div id="content">

                        <nav class="navbar navbar-default navbar-mainpage">
                            <div class="container-fluid">

                                <div class="navbar-header">
                                    <button type="button" id="sidebarCollapse" class="btn btn-info navbar-btn">
                                        <i class="glyphicon glyphicon-align-left"></i>
                                        <span>Insights</span>
                                    </button>
                                </div>
                            </div>
                        </nav>
                        <div class="tab-content">
                            <div id="userratings" class="tab-pane fade in active">
                                <h3>User Ratings</h3>
                                <RatingsChart />
                            </div>
                            <div id="agegroup" class="tab-pane fade">
                                <h3>Age Group </h3>
                                <AgeGroupChart />
                            </div>
                            <div id="predictions" class="tab-pane fade">
                                <h3>Predictions</h3>

                            </div>

                        </div>
                    </div>

                </div>


            );
        }
        return (

            <div>
                <Navbar inverse collapseOnSelect className='navbar-fixed-top navbarlinkedin-navbar'>
                    <Navbar.Header>
                        <Navbar.Brand>
                            <Link to="/home"><img alt="linkedin-logo" src="MainPage.jpeg" height="30" width="35"></img></Link>
                        </Navbar.Brand>
                        <Navbar.Toggle />
                    </Navbar.Header>
                    <Navbar.Collapse>

                    </Navbar.Collapse>
                </Navbar>
                <div className='col-md-4 left-color'>
                </div>
                <div className='col-md-4'>

                    <div className='container new-container'>
                        <h1 className='main-page-h1'>Will It Sell!</h1>
                        <textarea placeholder="Enter Description" className='mainpage-textarea' name='description' onChange={this.onChange}></textarea>
                        <div>
                            <button className='btn btn-primary mainpage-btn' onClick={this.submitDescription}>Submit</button>

                        </div>
                    </div>
                </div>
                <div className='col-md-4'>
                </div>


            </div>
        )
    }
}

export default MainPage;