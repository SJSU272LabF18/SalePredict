import React, { Component } from 'react';
import axios from 'axios';
import '../css/MainPage.css';
import WisNavbar from './WisNavbar';
//var bodyFormData = new FormData();
var querystring = require('querystring');


class MainPage extends Component {
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
        return (
            <div>
                <div className='mainpage'>
                    <WisNavbar />
                    <img className='bg-img' src='appstoreicon (1).png'  ></img>

                    <div className='main-desc'>
                        <textarea placeholder="Enter Description" className='mainpage-textarea' name='description' onChange={this.onChange}></textarea>
                        <button className='btn btn-primary mainpage-btn' onClick={this.submitDescription}>Submit</button>
                    </div>
                    <div>
                        <button className='btn btn-primary mainpage-btn' onClick={this.getRatings}>Check Ratings</button>

                    </div>
                </div>
            </div>
        );
    }
}

export default MainPage;