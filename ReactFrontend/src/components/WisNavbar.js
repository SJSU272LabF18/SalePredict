import React, { Component } from 'react';
import { Navbar, NavItem, MenuItem, NavDropdown, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import '../css/WisNavbar.css';

class WisNavbar extends Component {
    state = {}
    render() {
        return (
            <Navbar className='wisnavbar'>
                <Navbar.Header>
                    <Navbar.Brand>
                        <Link to="/home"><span className='glyphicon glyphicon-home wisnavbar-glyph' title='Home'></span></Link>
                    </Navbar.Brand>
                </Navbar.Header>
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
            </Navbar>
        );
    }
}

export default WisNavbar;