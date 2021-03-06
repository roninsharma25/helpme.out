import React, { Component } from 'react';
import { signInWithGoogle } from './Firebase';
import Login from './Login';

export default class Example extends Component {
    constructor() {
        super();
        this.state = {
            test: 'test'
        }
    }

    componentDidMount() {
        fetch('/test?arg=4').then(res => res.json()).then(output => {
            this.setState({
                test: output.output
            });
        })
    }

    render() {

        return (
            <div className="Example">
                <p>Testing backed connection</p>
                <p>Backend output: {this.state.test}</p>
                <Login />

            </div>
        )
    }
}