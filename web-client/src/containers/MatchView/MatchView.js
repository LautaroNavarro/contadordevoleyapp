import React, { Component } from 'react';
import Layout from '../../components/Layout/Layout';
import './MatchView.css';


class MatchView extends Component {
    render (){
        return (
            <Layout>
                <div className="text-center">
                    <h2 className="pt-3">San Martin VS Regatas</h2>
                    <h5>
                        código: A1DV
                        <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24" className="clickeable">
                            <path d="M0 0h24v24H0V0z" fill="none"/>
                            <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92c0-1.61-1.31-2.92-2.92-2.92zM18 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM6 13c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm12 7.02c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/>
                        </svg>
                    </h5>
                    <div className="d-flex flex-row m-auto">
                        <div className="container">
                            <div className="d-flex flex-row pb-1">
                                <div className="flex pr-1">
                                    <div className="rounded-circle bg-dark border border-dark circles"></div>
                                </div>
                                <div className="flex pr-1">
                                    <div className="rounded-circle border border-dark circles"></div>
                                </div>
                                <div className="flex pr-1">
                                    <div className="rounded-circle border border-dark circles"></div>
                                </div>
                            </div>
                            <div className="flex-fill rounded" style={ {"background-color": "red" } }>
                                    <h1 className="mainTeamNumber">20</h1>
                            </div>
                            <div className="d-flex flex-row">
                                <div className="flex-fill pr-1">
                                    <button className="btn btn-block btn-secondary">-</button>
                                </div>
                                <div className="flex-fill pl-1">
                                    <button className="btn btn-block btn-dark">+</button>
                                </div>
                            </div>
                        </div>
                        <div className="container">
                            <div className="d-flex flex-row pb-1">
                                <div className="flex pr-1">
                                    <div className="rounded-circle border border-dark circles"></div>
                                </div>
                                <div className="flex pr-1">
                                    <div className="rounded-circle border border-dark circles"></div>
                                </div>
                                <div className="flex pr-1">
                                    <div className="rounded-circle border border-dark circles"></div>
                                </div>
                            </div>
                            <div className="flex-fill rounded" style={ { "background-color": "blue" } }>
                                    <h1 className="mainTeamNumber">12</h1>
                            </div>
                            <div className="d-flex flex-row">
                                <div className="flex-fill pr-1">
                                    <button className="btn btn-block btn-secondary">-</button>
                                </div>
                                <div className="flex-fill pl-1">
                                    <button className="btn btn-block btn-dark">+</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </Layout>
        );
    }
}

export default MatchView;