import React, { Component } from 'react';
import axios from 'axios';
import '../css/MainPage.css';



class MainPage extends Component {
    constructor() {
        super();
        this.state = {
        };
        this.submitDescription = this.submitDescription.bind(this);
        this.onChange = this.onChange.bind(this);

    }
    // componentDidMount() {

    // }
    onChange(e) {

        this.setState({
            [e.target.name]: e.target.value

        })
    }
    submitDescription() {
        axios.get(`http://localhost:5000/`)
            .then((response) => {
                console.log(" response.data" + response)

                console.log(" response.data" + response.data)

            })
    }
    render() {
        return (
            <div className='mainpage'>
                {/* //     <img className='bg-img' src='QiAMG0g.png'></img> */}

                <div>
                    <textarea placeholder="Enter You Description" className='mainpage-textarea' name='description' onChange={this.onChange}></textarea>
                    <button className='btn btn-primary mainpage-btn' onClick={this.submitDescription}>Submit</button>
                </div>

            </div>
        );
    }
}

export default MainPage;