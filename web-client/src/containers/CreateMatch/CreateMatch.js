import React, { Component } from 'react';
import Layout from '../../components/Layout/Layout';
import { Link } from 'react-router-dom';
import './CreateMatch.css';

class Home extends Component {
    render () {
        return (
            <Layout>
                <div className="text-center">
                    <h1 className="pt-3 pb-3">Crear nuevo partido</h1>
                        <form>
                            <div className="d-flex flex-row m-auto">
                                <div className="flex-fill">
                                    <div className="container pt-3">
                                        <div className="form-group">
                                            <input type="text" className="form-control" placeholder="Equipo A" />
                                        </div>
                                        <div className="form-group">
                                            <input type="color" className="form-control" value="#ff0000" />
                                        </div>
                                    </div>
                                </div>
                                <div className="flex-fill">
                                    <div className="container pt-3">
                                        <div className="form-group">
                                            <input type="text" className="form-control" placeholder="Equipo B" />
                                        </div>
                                        <div className="form-group">
                                            <input type="color" className="form-control" value="#0000ff" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <div className="form-group container">
                                  <label for="sets">Al mejor de</label>
                                  <select className="form-control" id="sets">
                                    <option>1</option>
                                    <option>3</option>
                                    <option selected>5</option>
                                  </select>
                                </div>
                            </div>
                            <div>
                                <div className="form-group container">
                                    <button className="btn-block btn btn-outline-secondary " type="button" data-toggle="collapse" data-target=" #advancedOptions" aria-controls="advancedOptions" >Opciones avanzadas</button>
                                    <div className="collapse pt-3" id="advancedOptions">
                                        <div className="form-group">
                                            <label for="sets">Puntos de set</label>
                                            <input type="number" className="form-control" value="25" />
                                        </div>
                                        <div className="form-group">
                                            <label for="sets">Puntos de tie break</label>
                                            <input type="number" className="form-control" value="15" />
                                        </div>
                                        <div className="form-group">
                                            <label for="sets">Diferencia de dos puntos</label>
                                            <input type="number" className="form-control" value="2"/>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        <div className="container">
                            <Link to="/matches/1" className="btn btn-block btn-dark mb-3">Crear partido</Link>
                        </div>
                        </form>
                </div>
            </Layout>
        );
    }
}

export default Home;