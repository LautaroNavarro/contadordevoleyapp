import React, { Component } from 'react';
import Layout from '../../components/Layout/Layout';
import { Link } from 'react-router-dom';
import './CreateMatch.css';

class Home extends Component {

    state = {
        'sets_number': "5",
        'set_points_number': 25,
        'points_difference': 2,
        'tie_break_points': 15,
        'teams': [
            {
                'name': '',
                'color': '#ff0000',
            },
            {
                'name': '',
                'color': '#0000ff',
            }
        ]
    }

    handleChangeTeamOneName = (e) => {
        let stateCopy = {...this.state};
        stateCopy.teams[0].name = e.target.value;
        this.setState(stateCopy);
    }

    handleChangeTeamOneColor = (e) => {
        let stateCopy = {...this.state};
        stateCopy.teams[0].color = e.target.value;
        this.setState(stateCopy);
    }

    handleChangeTeamTwoName = (e) => {
        let stateCopy = {...this.state};
        stateCopy.teams[1].name = e.target.value;
        this.setState(stateCopy);
    }

    handleChangeTeamTwoColor = (e) => {
        let stateCopy = {...this.state};
        stateCopy.teams[1].color = e.target.value;
        this.setState(stateCopy);
    }

    handleChangeSetsNumberInput = (e) => {
        this.setState({'sets_number': e.target.value});
    }

    handleChangeSetPointsNumberInput = (e) => {
        this.setState({'set_points_number': parseInt(e.target.value)});
    }

    handleChangePointsDifferenceInput = (e) => {
        this.setState({'points_difference': parseInt(e.target.value)});
    }

    handleChangeTieBreakPointsInput = (e) => {
        this.setState({'tie_break_points': parseInt(e.target.value)});
    }

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
                                            <input
                                                type="text"
                                                className="form-control"
                                                placeholder="Equipo A"
                                                value={this.state.teams[0].name}
                                                onChange={ (e) => {this.handleChangeTeamOneName(e)} }
                                            />
                                        </div>
                                        <div className="form-group">
                                            <input
                                                type="color"
                                                className="form-control"
                                                value={ this.state.teams[0].color }
                                                onChange={ (e) => {this.handleChangeTeamOneColor(e)} }
                                            />
                                        </div>
                                    </div>
                                </div>
                                <div className="flex-fill">
                                    <div className="container pt-3">
                                        <div className="form-group">
                                            <input
                                                type="text"
                                                className="form-control"
                                                placeholder="Equipo B"
                                                value={this.state.teams[1].name}
                                                onChange={ (e) => {this.handleChangeTeamTwoName(e)} }
                                            />
                                        </div>
                                        <div className="form-group">
                                            <input
                                                type="color"
                                                className="form-control"
                                                value={ this.state.teams[1].color }
                                                onChange={ (e) => {this.handleChangeTeamTwoColor(e)} }
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <div className="form-group container" >
                                  <label htmlFor="sets">Al mejor de</label>
                                  <select className="form-control" value={ this.state.sets_number } onChange={ (e) => {this.handleChangeSetsNumberInput(e)} }>
                                    <option value="1">1</option>
                                    <option value="3">3</option>
                                    <option value="5">5</option>
                                  </select>
                                </div>
                            </div>
                            <div>
                                <div className="form-group container">
                                    <button className="btn-block btn btn-outline-secondary " type="button" data-toggle="collapse" data-target=" #advancedOptions" aria-controls="advancedOptions" >Opciones avanzadas</button>
                                    <div className="collapse pt-3" id="advancedOptions">
                                        <div className="form-group">
                                            <label htmlFor="sets">Puntos de set</label>
                                            <input
                                                type="number"
                                                className="form-control"
                                                value={this.state.set_points_number}
                                                onChange={ (e) => {this.handleChangeSetPointsNumberInput(e)} }
                                            />
                                        </div>
                                        <div className="form-group">
                                            <label htmlFor="sets">Puntos de tie break</label>
                                            <input
                                                type="number"
                                                className="form-control"
                                                value={this.state.tie_break_points}
                                                onChange={ (e) => {this.handleChangeTieBreakPointsInput(e)} }
                                            />
                                        </div>
                                        <div className="form-group">
                                            <label htmlFor="sets">Diferencia de dos puntos</label>
                                            <input
                                                type="number"
                                                className="form-control"
                                                value={this.state.points_difference}
                                                onChange={ (e) => {this.handleChangePointsDifferenceInput(e)} }
                                            />
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