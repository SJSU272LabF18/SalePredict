import React, { Component } from 'react';

class Predictions extends Component {
    constructor() {
        super();
        this.state = {
            Predicted_Rating: "",
            Selling_Ability: "",
            Detected_Genre: "",
            Total_Installs: "",
            Total_Users_That_Rated: "",
            Top_3_Similar_Apps1: "",
            Top_3_Similar_Apps2: "",
            Top_3_Similar_Apps3: "",


        };
    }
    componentDidMount() {
        console.log("In compoennt did mount")

        var value = localStorage.getItem("data");
        var parsedValue = JSON.parse(value)
        this.setState({
            Predicted_Rating: parsedValue.Predicted_Rating,
            Selling_Ability: parsedValue.Selling_Ability,
            Detected_Genre: parsedValue.Detected_Genre,
            Total_Installs: parsedValue.Total_Installs,
            Total_Users_That_Rated: parsedValue.Total_Users_That_Rated,
            Top_3_Similar_Apps1: parsedValue.Top_3_Similar_Apps[0].One1[0],
            Top_3_Similar_Apps2: parsedValue.Top_3_Similar_Apps[0].One2[0],
            Top_3_Similar_Apps3: parsedValue.Top_3_Similar_Apps[0].One3[0]
        })

    }
    render() {
        let app1 = Object.keys(this.state.Top_3_Similar_Apps1).map((app, i) => {
            return (
                <div>
                    <h>{this.state.Top_3_Similar_Apps1[app]}</h>
                </div>
            )
        })
        let app2 = Object.keys(this.state.Top_3_Similar_Apps2).map((app, i) => {
            return (
                <div>
                    <h>{this.state.Top_3_Similar_Apps2[app]}</h>
                </div>
            )
        })
        let app3 = Object.keys(this.state.Top_3_Similar_Apps3).map((app, i) => {
            return (
                <div>
                    <h>{this.state.Top_3_Similar_Apps3[app]}</h>
                </div>
            )
        })
        // let app1desc = Object.value(this.state.Top_3_Similar_Apps1).map((app, i) => {
        //     return (
        //         <div>
        //             <h>{this.state.Top_3_Similar_Apps1[app]}</h>
        //         </div>
        //     )
        // })
        return (
            <div>
                <table className='mainpage-table'>
                    <div className='col-md-4'>
                        <div class="card">
                            <div class="container container-for-card">
                                <h4><b>Predicted Rating</b></h4>
                                <p>{this.state.Predicted_Rating}</p>
                            </div>
                        </div>
                    </div>
                    <div className='col-md-4'>

                        <div class="card">
                            <div class="container container-for-card">
                                <h4><b>Selling Ability</b></h4>
                                <p>{this.state.Selling_Ability}</p>
                            </div>
                        </div>
                    </div>
                    <div className='col-md-4'>

                        <div class="card">
                            <div class="container container-for-card">
                                <h4><b>Detected Genre</b></h4>
                                <p>{this.state.Detected_Genre}</p>
                            </div>
                        </div>
                    </div>
                    <div className='col-md-4'>

                        <div class="card">
                            <div class="container container-for-card">
                                <h4><b>Total Installs</b></h4>
                                <p>{this.state.Total_Installs}</p>
                            </div>
                        </div>
                    </div>
                    <div className='col-md-4'>

                        <div class="card">
                            <div class="container container-for-card">
                                <h4><b>Total Users That Rated</b></h4>
                                <p>{this.state.Total_Users_That_Rated}</p>
                            </div>
                        </div>
                    </div>
                </table>

                <div className='row'>
                    <br></br>
                    <br></br>
                    <br></br>
                    <div className='col-md-offset-1'>

                        <h2>Top 3 Similar Apps</h2>
                        <div class="flip-card">
                            <div class="flip-card-inner">
                                <div class="flip-card-front">
                                    <h3> {this.state.Top_3_Similar_Apps1.Name} </h3>
                                </div>
                                <div class="flip-card-back">
                                    {app1}
                                </div>
                            </div>
                        </div>
                        <div class="flip-card">
                            <div class="flip-card-inner">
                                <div class="flip-card-front">
                                    <h3> {this.state.Top_3_Similar_Apps2.Name} </h3>
                                </div>
                                <div class="flip-card-back">
                                    {app2}
                                </div>
                            </div>
                        </div>
                        <div class="flip-card">
                            <div class="flip-card-inner">
                                <div class="flip-card-front">
                                    <h3> {this.state.Top_3_Similar_Apps3.Name} </h3>
                                </div>
                                <div class="flip-card-back">
                                    {app3}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        );
    }
}

export default Predictions;