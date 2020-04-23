import React, { Component } from 'react';
import './Layout.css';
import { Link } from 'react-router-dom';

class Layout extends Component {

    render () {
        return (
            <div>
                <nav className="navbar navbar-dark bg-dark">
                    <Link to="/" className="navbar-brand">Contador de voley</Link>
                </nav>
                <div className="container mainContainer">
                    {this.props.children}
                </div>
                <footer className="bg-dark mt-2">
                    <div className="footer-copyright text-center py-3 text-white">© 2020 Copyright:
                        <a href="https://mdbootstrap.com/">MDBootstrap.com</a>
                    </div>
                </footer>
            </div>
        );
    }
}

export default Layout;