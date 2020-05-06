import React, { Component } from 'react';
import Layout from '../../components/Layout/Layout';
import { Link } from 'react-router-dom';
import './Home.css';

class Home extends Component {

    state = {
        'displayJoinInput': false,
        'joinMatchInput': ''
    }

    handleJoinToMatchClick = (e) => {
        if (this.state.joinMatchInput === '') {
            this.setState({'displayJoinInput': this.state.displayJoinInput === false});
        } else {
            // TODO REDIRECT TO MATCH VIEW WITH ACCESS CODE
        }
    }

    handleChangeJoinMatchInput = (e) => {
        this.setState({'joinMatchInput': e.target.value});
    }

    render () {
        return (
            <Layout>
                <div className='text-center'>
                    <div className='titleContainer'>
                        <h1 className='mainTitule paddingTop20vh align-bottom'>Contador de voley</h1>
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
                                        value={ this.state.joinMatchInput }
                                        onChange={ (e) => {this.handleChangeJoinMatchInput(e)} }
                                    /> : ''
                            }
                            <button className='btn btn-dark' onClick={ (e) => {this.handleJoinToMatchClick(e)} }>Unirme a partido</button>
                        </div>
                    </div>
                </div>
            </Layout>
        );
    }
}
export default Home;