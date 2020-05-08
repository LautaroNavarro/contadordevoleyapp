import React, { Component } from 'react';
import { Link } from 'react-router-dom';


class MatchSummary extends Component {

    getLosserTeam () {
        for (var i = 0; i < this.props.match.teams.length; i++) {
            if (this.props.match.teams[i].id !== this.props.match.winner_team.id) {
                return this.props.match.teams[i];
            }
        }
    }

    getSortedSets () {
        return this.props.match.sets.sort(function(a, b) {
            return a.set_number - b.set_number;
        })
    }

    getSetsRendered () {
        let setsRendered = [];
        let sortSets = this.getSortedSets();
        for (var i = 0; i < this.props.match.sets.length; i++) {
            setsRendered.push(
                <tr key={`set-${i}`}>
                    <th scope='row'>{sortSets[i].set_number}</th>
                    <td>{sortSets[i].team_one_points}</td>
                    <td>{sortSets[i].team_two_points}</td>
                </tr>
            )
        }
        return setsRendered;
    }

    render () {
        if (this.props.match.winner_team){
            return (
                <div className='bg-white rounded-lg'>
                    <div className='card text-center'>
                        <div className='card-header'>
                            <h1 className='text-dark'>
                                {`${this.props.match.winner_team.name} le ganó a ${this.getLosserTeam().name} `}
                                <svg className='bi bi-flag-fill' width='1em' height='1em' viewBox='0 0 16 16' fill={this.props.match.winner_team.color}  xmlns='http://www.w3.org/2000/svg'>
                                  <path fillRule='evenodd' d='M3.5 1a.5.5 0 01.5.5v13a.5.5 0 01-1 0v-13a.5.5 0 01.5-.5z' clipRule='evenodd'/>
                                  <path fillRule='evenodd' d='M3.762 2.558C4.735 1.909 5.348 1.5 6.5 1.5c.653 0 1.139.325 1.495.562l.032.022c.391.26.646.416.973.416.168 0 .356-.042.587-.126a8.89 8.89 0 00.593-.25c.058-.027.117-.053.18-.08.57-.255 1.278-.544 2.14-.544a.5.5 0 01.5.5v6a.5.5 0 01-.5.5c-.638 0-1.18.21-1.734.457l-.159.07c-.22.1-.453.205-.678.287A2.719 2.719 0 019 9.5c-.653 0-1.139-.325-1.495-.562l-.032-.022c-.391-.26-.646-.416-.973-.416-.833 0-1.218.246-2.223.916A.5.5 0 013.5 9V3a.5.5 0 01.223-.416l.04-.026z' clipRule='evenodd'/>
                                </svg>
                            </h1>
                            <h1 className='text-dark'>{`${this.props.match.winner_team.sets_won} a ${this.getLosserTeam().sets_won}`}</h1>
                        </div>
                    <div className='card-body'>
                        <h5 className='card-title'>Detalles de sets</h5>
                        <table className='table'>
                          <thead>
                            <tr>
                              <th scope='col'>#</th>
                              <th scope='col'>{`${this.props.match.teams[0].name}`}</th>
                              <th scope='col'>{`${this.props.match.teams[1].name}`}</th>
                            </tr>
                          </thead>
                          <tbody>
                            { this.getSetsRendered() }
                          </tbody>
                        </table>
                    </div>
                    <div className='card-footer text-muted'>
                        <Link to='/'>Ver otro partido</Link>
                    </div>
                    </div>
                </div>
            );
        } else {
            return '';
        }
    }
}

export default MatchSummary;
