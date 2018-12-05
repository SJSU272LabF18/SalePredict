import React, { Component } from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';

class RatingsChart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            chartData: {
                labels: ['1.0', '2.0', '3.0', '4.0', '5.0'],
                datasets: [{
                    label: 'Ratings',
                    data: [
                        617594,
                        181045,
                        153060,
                        106519,
                        105162,
                        95072
                    ],
                    backgroundColor: [
                        // 'rgba(255, 99, 132, 0.6)',
                        'rgba(128,0,0,0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)',
                        'rgba(255, 99, 132, 0.6)'
                    ],
                }]
            }
        }
    }
    componentDidMount() {
        console.log("In compoennt did mount")

        var value = localStorage.getItem("data");
        // var parsedValue = JSON.parse(value)
        console.log("value " + value)
        console.log(value.Graph_Users_By_Ratings)
    }
    render() {
        return (
            <div>
                <Bar data={this.state.chartData}
                    options={{
                        maintainAspectRatio: true,
                        title: {
                            display: true,
                            text: 'Graph by User Ratings',
                            fontSize: 25
                        },

                        legend: {
                            display: true,
                            position: 'right',
                            labels: {
                                fontColor: '#000'
                            }
                        },

                        layout: {
                            padding: {
                                left: 50,
                                right: 0,
                                bottom: 0,
                                top: 0
                            }
                        },
                        tooltips: {
                            enabled: true
                        }
                    }}></Bar>
                <br></br>
                <Line data={this.state.chartData}
                    options={{
                        maintainAspectRatio: true,
                        title: {
                            display: true,
                            text: 'Largest Cities In Massachusetts',
                            fontSize: 25
                        },

                        legend: {
                            display: true,
                            position: 'right',
                            labels: {
                                fontColor: '#000'
                            }
                        },

                        layout: {
                            padding: {
                                left: 50,
                                right: 0,
                                bottom: 0,
                                top: 0
                            }
                        },
                        tooltips: {
                            enabled: true
                        }
                    }}></Line>
                <br></br>
                <Pie data={this.state.chartData}
                    options={{
                        maintainAspectRatio: true,
                        title: {
                            display: true,
                            text: 'Largest Cities In Massachusetts',
                            fontSize: 25
                        },

                        legend: {
                            display: true,
                            position: 'right',
                            labels: {
                                fontColor: '#000'
                            }
                        },

                        layout: {
                            padding: {
                                left: 50,
                                right: 0,
                                bottom: 0,
                                top: 0
                            }
                        },
                        tooltips: {
                            enabled: true
                        }
                    }}></Pie>
            </div>
        );
    }
}

export default RatingsChart;