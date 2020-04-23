import React, { Component } from 'react';
import Layout from '../../components/Layout/Layout';
import { Link } from 'react-router-dom';
import './Home.css';

class Home extends Component {
    render () {
        return (
            <Layout>
                <div className="text-center">
                    <div className="titleContainer">
                        <h1 className="mainTitule paddingTop20vh align-bottom">Contador de voley</h1>
                    </div>
                    <div className="w-50 m-auto">
                        <div className="d-flex flex-column">
                            <Link to="/matches/new" className="btn btn-outline-dark mb-3">Nuevo partido</Link>
                            <div className="collapse form-group" id="collapseExample">
                                <input type="text" className="form-control" placeholder="1ZPOK" />
                            </div>
                            <a href="./matches-client.html" className="btn btn-dark" type="button" data-toggle="collapse" data-target="#collapseExample" aria-controls="collapseExample" >Unirme a partido</a>
                        </div>
                    </div>
                </div>
            </Layout>
        );
    }
}

export default Home;