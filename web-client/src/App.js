import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Home from './containers/Home/Home';
import CreateMatch from './containers/CreateMatch/CreateMatch';
import MatchView from './containers/MatchView/MatchView';
import MatchControlView from './containers/MatchControlView/MatchControlView';
import Layout from './components/Layout/Layout';


function App() {
  return (
    <Router>
        <Layout>
            <div>
                <Route exact path='/' component={Home} />
                <Route exact path='/matches/new' component={CreateMatch} />
                <Route exact path='/matches/:id(\d+)' component={MatchControlView} />
                <Route exact path='/matches/' component={MatchView} />
            </div>
        </Layout>
    </Router>
  );
}

export default App;
