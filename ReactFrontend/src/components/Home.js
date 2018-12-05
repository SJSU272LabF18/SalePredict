import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, NavDropdown, MenuItem, FormGroup, FormControl, InputGroup, DropdownButton } from 'react-bootstrap';
import axios from 'axios';
import '../css/MainPage.css';



class Home extends Component {
    constructor() {
        super();
        this.state = {
        };
        this.submitDescription = this.submitDescription.bind(this);
        this.onChange = this.onChange.bind(this);
        this.getRatings = this.getRatings.bind(this);

    }
    // componentDidMount() {

    // }
    getRatings() {
        this.props.history.push("/ratingschart");
    }
    onChange(e) {

        this.setState({
            [e.target.name]: e.target.value

        })
    }
    submitDescription() {
        var data = {
            description: this.state.description
        }

        // var newdata = bodyFormData.set('description', this.state.description);
        console.log('data ' + JSON.stringify(data))
        // axios.post(`http://localhost:5000/json_description`, querystring.stringify({ description: this.state.description }))
        axios.post(`http://localhost:5000/json_description`, data)

            .then((response) => {
                console.log(" response.data" + response)

                console.log(" response.data" + JSON.stringify(response.data))
                localStorage.setItem("data", JSON.stringify(response.data))

            })
    }
    render() {
        return (<div>
            <Navbar inverse collapseOnSelect className='navbar-fixed-top navbarlinkedin-navbar'>
                <Navbar.Header>
                    <Navbar.Brand>
                        <Link to="/home"><img alt="linkedin-logo" src="MainPage.jpeg" height="30" width="35"></img></Link>
                    </Navbar.Brand>
                    <Navbar.Toggle />
                </Navbar.Header>
                <Navbar.Collapse>
                    <Nav pullRight>
                        {/* <NavItem eventKey={1} href="#">
                        Link</NavItem>
                    <NavItem eventKey={2} href="#">
                        Link</NavItem> */}
                        <NavDropdown eventKey={3} title="Account" id="basic-nav-dropdown" >
                            <MenuItem eventKey={3.1}><Link to="/login"><span className='glyphicon glyphicon-log-in'></span>    Login</Link></MenuItem>
                            <MenuItem eventKey={3.2}><Link to='#'><span className='glyphicon glyphicon-user'></span>    Profile </Link></MenuItem>
                            <MenuItem eventKey={3.3}><Link to="/mainpage"><span className='glyphicon glyphicon-signal'></span>   Check your App's Success</Link></MenuItem>
                            <MenuItem divider />
                            <MenuItem eventKey={3.4}><Link to="/home"><span className='glyphicon glyphicon-home'></span>   Home</Link></MenuItem>
                        </NavDropdown>
                    </Nav>
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


        </div>);
    }
}

export default Home;