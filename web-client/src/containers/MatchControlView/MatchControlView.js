import React, { Component } from 'react';
import Layout from '../../components/Layout/Layout';
import './MatchControlView.css';
import GeneralContext from './../../components/Context/GeneralContext';
import axios from 'axios';


class MatchControlView extends Component {

    static contextType = GeneralContext;

    state = {
        'id': null,
        'sets_number': 5,
        'access_code': null,
        'status': null,
        'game_status': null,
        'set_points_number': null,
        'points_difference': null,
        'tie_break_points': null,
        'sets': [],
        'teams': [
            {
                'name': null,
                'color': null,
                'sets_won': 0
            },
            {
                'name': null,
                'color': null,
                'sets_won': 0
            }
        ],
        'winner_team': null,
    }

    async addPoint(team) {
        const response = await axios.post(
            `/api/matches/${this.props.match.params.id}/${team}/add?token=${sessionStorage.getItem('token')}`
        );
        this.setState(response.data.match);
    }

    async subPoint(team) {
        const response = await axios.post(
            `/api/matches/${this.props.match.params.id}/${team}/sub?token=${sessionStorage.getItem('token')}`
        );
        this.setState(response.data.match);
    }


    async getMatch() {
        const response = await axios.get(`/api/matches/${this.props.match.params.id}`);
        this.setState(response.data.match);
    }

    componentDidMount () {
        if (!sessionStorage.getItem('token')) {
            const {setRedirect} = this.context;
            setRedirect('/');
        } else {
            this.getMatch()
        }
    }

    getRenderedSets (team) {
        let renderedWon = team === 'team_one' ? this.state.teams[0].sets_won : this.state.teams[1].sets_won
        let renderedWonCount = 0;

        let render = [];
        for (let i = 0; i < Math.floor(((this.state.sets_number / 2) + 1)); i++) {
            if (renderedWonCount < renderedWon) {
                render.push(
                    <div className="flex pr-1">
                        <div className="rounded-circle bg-dark border border-dark circles"></div>
                    </div>
                );
            } else {
                render.push(
                    <div className="flex pr-1">
                        <div className="rounded-circle border border-dark circles"></div>
                    </div>
                );
            }
            renderedWonCount += 1;
        }
        return render;
    }

    render (){
        return (
            <div>
                <div className="text-center">
                    <h2 className="pt-3">{`${this.state.teams[0].name} VS ${this.state.teams[1].name}`}</h2>
                    <h5>
                        {`CODIGO ${this.state.access_code}`}
                        <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24" className="clickeable">
                            <path d="M0 0h24v24H0V0z" fill="none"/>
                            <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92c0-1.61-1.31-2.92-2.92-2.92zM18 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM6 13c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm12 7.02c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/>
                        </svg>
                    </h5>
                    <div className="d-flex flex-row m-auto">
                        <div className="container">
                            <div className="d-flex flex-row pb-1">
                                {
                                    this.getRenderedSets('team_one')
                                }
                            </div>
                            <div className="flex-fill rounded" style={ {"backgroundColor": this.state.teams[0].color } }>
                                    <h1 className="mainTeamNumber">{this.state.sets.length != 0 ? this.state.sets[this.state.sets.length - 1].team_one_points : 0}</h1>
                            </div>
                            <div className="d-flex flex-row">
                                <div className="flex-fill pr-1">
                                    <div
                                        className="btn btn-block btn-secondary"
                                        onClick={ () => {this.subPoint('team_one')}}
                                    >-</div>
                                </div>
                                <div className="flex-fill pl-1">
                                    <div
                                        className="btn btn-block btn-dark"
                                        onClick={ () => {this.addPoint('team_one')}}
                                    >+</div>
                                </div>
                            </div>
                        </div>
                        <div className="container">
                            <div className="d-flex flex-row pb-1">
                                {
                                    this.getRenderedSets('team_two')
                                }
                            </div>
                            <div className="flex-fill rounded" style={ {"backgroundColor": this.state.teams[1].color } }>
                                    <h1 className="mainTeamNumber">{this.state.sets.length != 0 ? this.state.sets[this.state.sets.length - 1].team_two_points : 0}</h1>
                            </div>
                            <div className="d-flex flex-row">
                                <div className="flex-fill pr-1">
                                    <div
                                        className="btn btn-block btn-secondary"
                                        onClick={ () => {this.subPoint('team_two')}}
                                    >-</div>
                                </div>
                                <div className="flex-fill pl-1">
                                    <div
                                        className="btn btn-block btn-dark"
                                        onClick={ () => {this.addPoint('team_two')}}
                                    >+</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default MatchControlView;