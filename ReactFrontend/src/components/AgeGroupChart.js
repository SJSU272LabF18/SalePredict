import React, { Component } from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';

class AgeGroupChart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            chartData: {
                labels: ['Children 5-13', 'Teenager 13-18', 'Adult 18-50', 'Elderly 50+'],
                datasets: [{
                    label: 'Ratings',
                    data: [],
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
        var parsedValue = JSON.parse(value)
        var data1 = parsedValue.Graph_Installs_By_Age_Group[0].Children_5;
        var data2 = parsedValue.Graph_Installs_By_Age_Group[0].Teenager_13;
        var data3 = parsedValue.Graph_Installs_By_Age_Group[0].Adult_18;
        var data4 = parsedValue.Graph_Installs_By_Age_Group[0].Elderly_50;
        var arr = []
        arr.push(data1)
        arr.push(data2)
        arr.push(data3)
        arr.push(data4)
        console.log("arr" + arr)
        this.setState({
            ...this.state.chartData.datasets[0].data = arr
        })
        console.log("value " + JSON.stringify(value))
        console.log("this.state.chartData.datasets.data " + this.state.chartData.datasets.data)

        console.log(parsedValue.Graph_Users_By_Ratings[0].One)
        console.log(parsedValue.Predicted_Rating)
        console.log(parsedValue.Selling_Ability)
        console.log(parsedValue.Detected_Genre)

    }
    render() {
        return (
            <div className='container'>
                <Pie data={this.state.chartData}
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
                    }}></Pie>
                <br></br>
            </div>
        );
    }
}

export default AgeGroupChart;