import React, { Component } from 'react';
import './Layout.css';
import { Link, Redirect } from 'react-router-dom';
import GeneralContext from './../Context/GeneralContext';


class Layout extends Component {


    state = {
        redirect: false,
        redirectUrl: '/',
    }

    setRedirect = (redirectUrl) => {
      this.setState({
        redirectUrl,
        redirect: true,
      })
    }

    renderRedirect = () => {
      if (this.state.redirect) {
        return <Redirect to={this.state.redirectUrl} />
      }
    }

    render () {
        return (
            <GeneralContext.Provider value={
                {
                    setRedirect: this.setRedirect,
                }
            }>
            { this.renderRedirect() }
            <div>
                <nav className="navbar navbar-dark bg-dark">
                    <Link to="/" className="navbar-brand">Contador de voley</Link>
                </nav>
                <div className="container mainContainer">
                    {this.props.children}
                </div>
                <footer className="bg-dark mt-2">
                    <div className="footer-copyright text-center py-3 text-white">© 2020 Copyright:
                        <a href="https://contadordevoley.com/">contadordevoley.com</a>
                    </div>
                </footer>
            </div>
            </GeneralContext.Provider>
        );
    }
}

export default Layout;