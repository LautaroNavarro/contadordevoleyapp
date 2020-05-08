import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './Home.css';
import GeneralContext from './../../components/Context/GeneralContext';


class Home extends Component {

    static contextType = GeneralContext;

    state = {
        'displayJoinInput': false,
        'accessCodeInput': ''
    }

    handleJoinToMatchClick = (e) => {
        if (this.state.accessCodeInput === '') {
            this.setState({'displayJoinInput': this.state.displayJoinInput === false});
        } else {
            const {setRedirect} = this.context;
            setRedirect(`/matches/?access_code=${this.state.accessCodeInput}`);
        }
    }

    handleChangeJoinMatchInput = (e) => {
        this.setState({'accessCodeInput': e.target.value});
    }

    render () {
        return (
            <div>
                <div className='text-center'>
                    <div className='titleContainer'>
                        <div className='mainTitule paddingTop20vh align-bottom mb-5'>
                            <img src='/favicon.png' width='275' height='275' className='d-inline-block align-top mb-4' />
                            <h1 className="text-dark">Contador de voley</h1>
                        </div>
                    </div>
                    <div className='w-50 m-auto'>
                        <div className='d-flex flex-column'>
                            <Link to='/matches/new' className='btn btn-outline-dark mb-3'>Nuevo partido</Link>
                            {
                                this.state.displayJoinInput ?
                                    <input
                                        type='text'
                                        className='form-control mb-3'
                                        placeholder='1ZPOK'
                                        value={ this.state.accessCodeInput }
                                        onChange={ (e) => {this.handleChangeJoinMatchInput(e)} }
                                    /> : ''
                            }
                            <button className='btn btn-dark' onClick={ (e) => {this.handleJoinToMatchClick(e)} }>Unirme a partido</button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
export default Home;